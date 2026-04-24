"""
github_client.py — Calls GitHub Models API (free, OpenAI-compatible).

Endpoint : https://models.github.ai/inference/chat/completions
Auth     : Bearer $GITHUB_TOKEN  (PAT with models:read)
Models   : Meta-Llama-3.1-8B-Instruct  (fast, tiny, free low-tier)
           Phi-4  (slightly smarter, still low-tier)
           Phi-3-mini-4k-instruct  (smallest)

Rate limits (free tier, no Copilot subscription):
  Low-tier  : 15 req/min, 150 req/day
  High-tier : 10 req/min,  50 req/day
→ We use low-tier (Llama-8B) and batch aggressively so we stay well under.

Token budget per call:
  System prompt : ~120 tokens
  User batch    : ~40 tokens * N races  (we cap N=12 per call)
  Response      : ~30 tokens * N races
  Total per call: well under 1500 tokens
"""

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from sarif_parser import get_code_snippet, severity

GITHUB_API = "https://models.github.ai/inference/chat/completions"

# Ordered preference — all low-rate-limit tier (150 req/day free)
PREFERRED_MODELS = [
    "Meta-Llama-3.1-8B-Instruct",
    "Phi-4",
    "Phi-3-mini-4k-instruct",
    "Phi-3.5-mini-instruct",
]

SYSTEM_PROMPT = """\
You are a concise distributed-systems expert. Analyse race condition candidates found by static analysis in a Java Spring Boot microservice system.

For EACH candidate decide:
  REAL            — genuine concurrent write conflict, can cause data corruption/lost updates
  FALSE_POSITIVE  — not a real race (read-only endpoints, partitioned by ID, idempotent, admin-only config rarely called concurrently)
  UNCERTAIN       — not enough info to decide

Key heuristics:
1. Two WRITE endpoints on same entity with no lock → REAL (Write-Write)
2. Read-check before Write (TOCTOU) on same entity → REAL
3. Both endpoints are GET/read-only on same entity → FALSE_POSITIVE (reads don't race)
4. Endpoints partitioned by different user/orderId path param → FALSE_POSITIVE
5. Admin config endpoints (station, train-type, price config) rarely called concurrently → UNCERTAIN
6. createNewOrder + payOrder on Order entity → REAL (high severity)

Respond ONLY with a JSON array, no markdown, no extra text."""


@dataclass
class RaceResult:
    race: dict
    verdict: str        # REAL | FALSE_POSITIVE | UNCERTAIN
    confidence: str     # HIGH | MEDIUM | LOW
    risk_score: int     # 1-10
    justification: str


def _http_post(token: str, payload: dict, retries: int = 3) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        GITHUB_API,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"  ⚠ Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif e.code in (500, 502, 503):
                time.sleep(5 * (attempt + 1))
            else:
                body_text = e.read().decode(errors="replace")
                raise RuntimeError(f"HTTP {e.code}: {body_text}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection error: {e}") from e
    raise RuntimeError("Max retries exceeded")


def _build_user_prompt(entity: str, batch: list[dict], source_root: str | None) -> str:
    lines = [f'Entity: "{entity}" — {len(batch)} race candidates\n']
    for i, r in enumerate(batch):
        # Parse out HTTP verb + path vs class.method
        def split_ep(ep: str):
            if "(" in ep:
                http_part = ep[:ep.index("(")].strip()
                method_part = ep[ep.index("(")+1:].rstrip(")")
            else:
                http_part, method_part = ep, ""
            return http_part, method_part

        h1, m1 = split_ep(r["endpoint1"])
        h2, m2 = split_ep(r["endpoint2"])

        lines.append(f"[{i}] {r['race_type']} | sev={severity(r)}")
        lines.append(f"  EP1: {h1}  [{m1}]")
        lines.append(f"  EP2: {h2}  [{m2}]")

        # Optionally add a tiny snippet (max 300 chars) to help the model
        if source_root:
            snip = get_code_snippet(source_root, r["file1"], r["line1"], ctx=4)
            if snip:
                lines.append(f"  CODE:\n{snip[:300]}")
        lines.append("")

    lines.append(
        f'Return JSON array with exactly {len(batch)} objects:\n'
        '[{"index":0,"verdict":"REAL|FALSE_POSITIVE|UNCERTAIN","confidence":"HIGH|MEDIUM|LOW",'
        '"risk_score":1-10,"justification":"one sentence"}]'
    )
    return "\n".join(lines)


def _parse_response(text: str, n: int) -> list[dict]:
    """Robustly extract JSON array from model output."""
    text = text.strip()
    # Strip markdown fences
    if "```" in text:
        import re
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()
    # Find array bounds
    s, e = text.find("["), text.rfind("]") + 1
    if s >= 0 and e > s:
        try:
            parsed = json.loads(text[s:e])
            if isinstance(parsed, list) and len(parsed) == n:
                return parsed
            # Reindex if model forgot the index field
            if isinstance(parsed, list):
                for j, item in enumerate(parsed):
                    item.setdefault("index", j)
                return parsed[:n]
        except json.JSONDecodeError:
            pass
    # Fallback
    return [{"index": j, "verdict": "UNCERTAIN", "confidence": "LOW",
             "risk_score": 5, "justification": "parse error"} for j in range(n)]


class GitHubModelsClient:
    def __init__(self, token: str, model: str = PREFERRED_MODELS[0]):
        self.token = token
        self.model = model
        self._last_call = 0.0
        self._min_gap = 4.5   # 15 rpm → ~4s between calls (with buffer)

    def _throttle(self):
        elapsed = time.time() - self._last_call
        if elapsed < self._min_gap:
            time.sleep(self._min_gap - elapsed)
        self._last_call = time.time()

    def analyse_batch(self, entity: str, races: list[dict],
                      source_root: str | None = None) -> list[RaceResult]:
        """Analyse a batch of races (max 12) for one entity in one API call."""
        assert len(races) <= 12, "Max 12 races per call"

        prompt = _build_user_prompt(entity, races, source_root)
        self._throttle()

        try:
            resp = _http_post(self.token, {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                "temperature": 0.05,
                "max_tokens": 60 * len(races),   # ~60 tokens per verdict
                "top_p": 0.9,
            })
            raw_text = resp["choices"][0]["message"]["content"]
        except RuntimeError as e:
            print(f"    ✗ API error: {e}")
            raw_text = "[]"

        parsed = _parse_response(raw_text, len(races))

        results = []
        for i, race in enumerate(races):
            item = next((p for p in parsed if p.get("index") == i), None)
            if item is None and i < len(parsed):
                item = parsed[i]
            if item is None:
                item = {"verdict": "UNCERTAIN", "confidence": "LOW",
                        "risk_score": 5, "justification": "no response"}

            r = RaceResult(
                race=race,
                verdict=item.get("verdict", "UNCERTAIN"),
                confidence=item.get("confidence", "LOW"),
                risk_score=int(item.get("risk_score", 5)),
                justification=item.get("justification", ""),
            )
            results.append(r)

            icon = {"REAL": "🔴", "FALSE_POSITIVE": "✅", "UNCERTAIN": "🟡"}.get(r.verdict, "?")
            ep1 = race["endpoint1"].split("(")[-1].rstrip(")")
            ep2 = race["endpoint2"].split("(")[-1].rstrip(")")
            jus = r.justification[:70] if r.justification else ""
            print(f"    {icon} [{r.verdict}] {ep1} ↔ {ep2} | {jus}")

        return results
