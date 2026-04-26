

import json
import re
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from sarif_parser import get_code_snippet, severity, TRANSACTIONAL_ENTITIES, ADMIN_CONFIG_ENTITIES

GITHUB_API = "https://models.github.ai/inference/chat/completions"

PREFERRED_MODELS = [
    "Meta-Llama-3.1-8B-Instruct",
    "Phi-4",
    "Phi-3.5-mini-instruct",
    "Phi-3-mini-4k-instruct",
]

# ── System prompt: much richer, covers READ_WRITE patterns explicitly ────────
SYSTEM_PROMPT = """\
You are a distributed-systems security analyst reviewing race condition reports from a static analyser on the Train-Ticket Java Spring Boot microservice benchmark. The analyser reports pairs of HTTP endpoints that access the same database entity without locking.

Your job: for each candidate, decide whether it is a REAL race, a FALSE_POSITIVE, or UNCERTAIN — and explain why in 2-3 sentences covering: (a) what both endpoints do, (b) whether they can genuinely run concurrently on the SAME record, and (c) what bad outcome would occur if they did.

=== CLASSIFICATION RULES ===

FALSE_POSITIVE — filter these out:
  FP1. Both endpoints are GET + read-only method (getById, findBy*, query*, calculate*, check*).
       Reads never corrupt state, so read-read is always safe.
  FP2. READ_WRITE pair where the reader is a simple lookup (getOrderById, findByAccountId)
       that does NOT gate a downstream write. Plain reads on stale data are benign.
  FP3. Both endpoints are admin-only paths (/admin) on a config entity (Station, Route,
       TrainType, PriceConfig, SecurityConfig). Admin endpoints are rarely called
       concurrently; these are ops/management paths, not user traffic.
  FP4. The two endpoints belong to DIFFERENT microservices operating on separate data
       partitions (e.g. ts-order-service vs ts-order-other-service both have Order entities
       but they are stored in separate MongoDB collections — no sharing).
  FP5. calculateSoldTicket, securityInfoCheck, getOrderPrice — these are read-aggregation
       endpoints; the "write" the analyser sees is a transient computation, not a DB write.

REAL — confirm these:
  R1. Two WRITE endpoints (POST/PUT/DELETE or save*/update*/delete*/pay*/modify*) on a
      TRANSACTIONAL entity (Order, Payment, Money, User, ConsignRecord, FoodOrder,
      WaitListOrder, FoodDeliveryOrder) with no lock. Lost-update or double-insert risk.
  R2. createNewOrder + addcreateNewOrder — both POST to the same Order collection.
      Concurrent calls with the same payload can create duplicate orders.
  R3. payOrder (GET but writes status) + any other writer on Order — payOrder modifies
      Order.status to PAID; a concurrent createNewOrder or deleteOrder causes inconsistency.
  R4. modifyOrder (GET but writes status field) + createNewOrder/deleteOrder on Order —
      status update races with creation or deletion.
  R5. INSERT + DELETE on same transactional entity — delete can remove a just-created record.
  R6. UPDATE + DELETE on same entity — classic lost-update: update applies to a deleted row.
  R7. Two concurrent INSERT paths (createNewOrder + addcreateNewOrder) — potential
      duplicate key or double-booking.
  R8. foodservice: createFoodOrder + updateFoodOrder + deleteFoodOrder all write FoodOrder
      — any pair is a real race.

UNCERTAIN:
  U1. READ_WRITE where the read is a check-then-act (e.g. securityInfoCheck reads a
      threshold then upstream code decides to write) — need runtime info to confirm.
  U2. Endpoints on PARTIALLY shared entities where partitioning is unclear.
  U3. Any pair involving RabbitMQ async handlers — timing depends on message ordering.

=== OUTPUT FORMAT ===
Respond ONLY with a valid JSON array. No markdown fences, no preamble.
Each object must have:
  "index"         : integer (0-based, matching input order)
  "verdict"       : "REAL" | "FALSE_POSITIVE" | "UNCERTAIN"
  "confidence"    : "HIGH" | "MEDIUM" | "LOW"
  "risk_score"    : integer 1-10
  "what_happens"  : one sentence — concrete bad outcome if this race fires
  "why_verdict"   : one sentence — the specific rule (R1-R8 / FP1-FP5 / U1-U3) that applies
  "fix"           : one sentence — the recommended fix (optimistic lock / distributed lock / DB constraint / N/A)
"""


@dataclass
class RaceResult:
    race: dict
    verdict: str          # REAL | FALSE_POSITIVE | UNCERTAIN
    confidence: str       # HIGH | MEDIUM | LOW
    risk_score: int       # 1-10
    what_happens: str     # concrete bad outcome
    why_verdict: str      # which rule fired
    fix: str              # recommended fix


def _build_prompt(entity: str, batch: list[dict], source_root: str | None) -> str:
    is_transactional = entity in TRANSACTIONAL_ENTITIES
    is_config        = entity in ADMIN_CONFIG_ENTITIES

    header = [
        f'Entity: "{entity}"',
        f'Class: {"TRANSACTIONAL (high-traffic user data)" if is_transactional else "ADMIN CONFIG (low-traffic)" if is_config else "OTHER"}',
        f'Candidates: {len(batch)}\n',
    ]

    items = []
    for i, r in enumerate(batch):
        ep1, ep2 = r["endpoint1"], r["endpoint2"]
        h1,  h2  = r.get("http1","?"), r.get("http2","?")
        m1,  m2  = r.get("method1","?"), r.get("method2","?")

        # Build a compact but information-dense description
        block = [
            f"[{i}] {r['race_type']}",
            f"  EP1: {h1} {ep1.split('(')[0].strip()} → method={m1}",
            f"  EP2: {h2} {ep2.split('(')[0].strip()} → method={m2}",
        ]

        # Add EP admin flags
        flags = []
        if "/admin" in ep1.lower(): flags.append("EP1=admin-path")
        if "/admin" in ep2.lower(): flags.append("EP2=admin-path")
        if r.get("is_transactional"): flags.append("entity=transactional")
        if r.get("is_admin_config"):  flags.append("entity=admin-config")
        if flags:
            block.append(f"  flags: {', '.join(flags)}")

        # Optional code snippet (very tight budget)
        if source_root:
            snip = get_code_snippet(source_root, r["file1"], r["line1"], ctx=4)
            if snip:
                block.append(f"  code:\n{snip[:250]}")

        items.append("\n".join(block))

    schema = (
        f'\nReturn JSON array with exactly {len(batch)} objects:\n'
        '[{"index":0,"verdict":"REAL|FALSE_POSITIVE|UNCERTAIN","confidence":"HIGH|MEDIUM|LOW",'
        '"risk_score":1-10,"what_happens":"...","why_verdict":"...","fix":"..."}]'
    )

    return "\n".join(header) + "\n".join(items) + schema


def _parse_response(text: str, n: int) -> list[dict]:
    text = text.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()
    s, e = text.find("["), text.rfind("]") + 1
    if s >= 0 and e > s:
        try:
            parsed = json.loads(text[s:e])
            if isinstance(parsed, list):
                # Re-index if needed
                for j, item in enumerate(parsed):
                    item.setdefault("index", j)
                return parsed[:n] if len(parsed) >= n else parsed
        except json.JSONDecodeError:
            # Try to fix trailing commas
            try:
                fixed = re.sub(r',\s*([}\]])', r'\1', text[s:e])
                parsed = json.loads(fixed)
                if isinstance(parsed, list):
                    return parsed[:n]
            except Exception:
                pass
    return [{"index": j, "verdict": "UNCERTAIN", "confidence": "LOW", "risk_score": 5,
             "what_happens": "parse error", "why_verdict": "LLM output malformed", "fix": "manual review"}
            for j in range(n)]


def _http_post(token: str, payload: dict, retries: int = 3) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        GITHUB_API, data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 65 * (attempt + 1)
                print(f"  ⚠ Rate limited — waiting {wait}s...")
                time.sleep(wait)
            elif e.code in (500, 502, 503):
                time.sleep(8 * (attempt + 1))
            else:
                raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection error: {e}") from e
    raise RuntimeError("Max retries exceeded")


class GitHubModelsClient:
    def __init__(self, token: str, model: str = PREFERRED_MODELS[0]):
        self.token = token
        self.model = model
        self._last_call = 0.0
        self._min_gap = 5.0   # 15 rpm → one call every 5s (with buffer)

    def _throttle(self):
        elapsed = time.time() - self._last_call
        if elapsed < self._min_gap:
            time.sleep(self._min_gap - elapsed)
        self._last_call = time.time()

    def analyse_batch(self, entity: str, races: list[dict],
                      source_root: str | None = None) -> list[RaceResult]:
        """Send one batch (max 10 races) to the LLM and return RaceResult list."""
        assert len(races) <= 10

        prompt = _build_prompt(entity, races, source_root)
        self._throttle()

        try:
            resp = _http_post(self.token, {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                "temperature": 0.05,
                "max_tokens": 120 * len(races),  # 120 tokens/race = room for 2-3 sentences
                "top_p": 0.9,
            })
            raw = resp["choices"][0]["message"]["content"]
        except RuntimeError as e:
            print(f"    ✗ API error: {e}")
            raw = "[]"

        parsed = _parse_response(raw, len(races))

        results = []
        for i, race in enumerate(races):
            item = next((p for p in parsed if p.get("index") == i), None)
            if item is None and i < len(parsed):
                item = parsed[i]
            if item is None:
                item = {"verdict": "UNCERTAIN", "confidence": "LOW", "risk_score": 5,
                        "what_happens": "no response", "why_verdict": "", "fix": ""}

            r = RaceResult(
                race=race,
                verdict=item.get("verdict", "UNCERTAIN"),
                confidence=item.get("confidence", "LOW"),
                risk_score=int(item.get("risk_score", 5)),
                what_happens=item.get("what_happens", ""),
                why_verdict=item.get("why_verdict", ""),
                fix=item.get("fix", ""),
            )
            results.append(r)

            icon  = {"REAL": "🔴", "FALSE_POSITIVE": "✅", "UNCERTAIN": "🟡"}.get(r.verdict, "?")
            m1    = race.get("method1", "?")
            m2    = race.get("method2", "?")
            print(f"    {icon} [{r.verdict:14s}] {m1} ↔ {m2}  risk={r.risk_score}")
            if r.what_happens:
                print(f"         what: {r.what_happens[:90]}")
            if r.why_verdict:
                print(f"         rule: {r.why_verdict[:90]}")

        return results