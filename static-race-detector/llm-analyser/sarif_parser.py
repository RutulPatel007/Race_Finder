import json
import re
from pathlib import Path
from dataclasses import dataclass, field

# ── Semantic method-name signals ────────────────────────────────────────────

# Methods that ONLY read — never mutate state
READ_ONLY_VERBS = {
    "get", "find", "query", "fetch", "list", "search", "retrieve",
    "check", "calculate", "count", "exists", "load", "read",
    "queryall", "findall", "getall", "queryorders", "calculateSoldTicket",
    "securityinfocheck", "getorderbyid", "getorderprice",
}

# Methods that definitely WRITE
WRITE_VERBS = {
    "create", "save", "insert", "update", "delete", "modify", "add",
    "put", "post", "remove", "register", "pay", "cancel", "change",
    "createNewOrder", "addcreateNewOrder", "payOrder", "modifyOrder",
    "saveOrderInfo", "updateOrder", "deleteOrder",
}

# Entities that are pure admin config — rarely called concurrently in prod
ADMIN_CONFIG_ENTITIES = {
    "Station", "TrainType", "Route", "PriceConfig", "ConsignPrice",
    "SecurityConfig", "Config",
}

# Entities that are high-traffic transactional — highest real-race risk
TRANSACTIONAL_ENTITIES = {
    "Order", "Payment", "Money", "User", "ConsignRecord",
    "FoodOrder", "WaitListOrder", "FoodDeliveryOrder",
}


def _method_from_ep(ep: str) -> str:
    """Extract the Java method name from endpoint string."""
    m = re.search(r'\((\w+)\.(\w+)\)', ep)
    return m.group(2).lower() if m else ""


def _http_verb(ep: str) -> str:
    """Extract HTTP verb (GET/POST/PUT/DELETE/PATCH)."""
    m = re.match(r'^\s*(GET|POST|PUT|DELETE|PATCH)', ep.upper())
    return m.group(1) if m else ""


def _path_from_ep(ep: str) -> str:
    """Extract URL path."""
    m = re.search(r'((?:GET|POST|PUT|DELETE|PATCH)\s+)(.+?)\s*\(', ep.upper())
    return m.group(2) if m else ""


def _is_readonly_method(method_name: str) -> bool:
    name = method_name.lower()
    return any(name.startswith(v) or name == v for v in READ_ONLY_VERBS)


def _is_write_method(method_name: str) -> bool:
    name = method_name.lower()
    return any(name.startswith(v) or name == v for v in WRITE_VERBS)


def _path_has_id_param(path: str) -> bool:
    """Does the URL path contain an ID path parameter like /orderId /userId?"""
    return bool(re.search(r'/(order|user|account|consign|assurance|station|train|trip|food|price|security|config)[Ii][Dd]', path))


def _are_same_service(ep1: str, ep2: str) -> bool:
    """Both endpoints in the same microservice (same controller class)?"""
    cls1 = re.search(r'\((\w+)\.\w+\)', ep1)
    cls2 = re.search(r'\((\w+)\.\w+\)', ep2)
    if cls1 and cls2:
        return cls1.group(1) == cls2.group(1)
    return False


def _is_admin_endpoint(ep: str) -> bool:
    return "/admin" in ep.lower()


# ── Pre-filter heuristics (no LLM needed) ───────────────────────────────────

@dataclass
class PreFilterResult:
    verdict: str          # REAL | FALSE_POSITIVE | UNCERTAIN | NEEDS_LLM
    confidence: str
    risk_score: int
    reason: str           # short explanation of why pre-filter fired


def pre_filter(race: dict) -> PreFilterResult:
    """
    Apply deterministic heuristics before the LLM.
    Returns NEEDS_LLM when we can't be sure without deeper reasoning.
    """
    ep1, ep2    = race["endpoint1"], race["endpoint2"]
    h1, h2      = _http_verb(ep1), _http_verb(ep2)
    m1, m2      = _method_from_ep(ep1), _method_from_ep(ep2)
    p1, p2      = _path_from_ep(ep1), _path_from_ep(ep2)
    entity      = race["entity"]
    race_type   = race["race_type"]

    ro1 = _is_readonly_method(m1) or h1 == "GET"
    ro2 = _is_readonly_method(m2) or h2 == "GET"
    w1  = _is_write_method(m1) or h1 in ("POST","PUT","DELETE","PATCH")
    w2  = _is_write_method(m2) or h2 in ("POST","PUT","DELETE","PATCH")

    # ── Hard FALSE_POSITIVE rules ─────────────────────────────────

    # 1. Both endpoints are pure GET + read-only method name → read-read, safe
    if h1 == "GET" and h2 == "GET" and _is_readonly_method(m1) and _is_readonly_method(m2):
        return PreFilterResult("FALSE_POSITIVE", "HIGH", 1,
            f"Both {m1} and {m2} are GET read-only; concurrent reads never cause data races.")

    # 2. READ_WRITE where the reader is a simple GET by ID (not a check-then-act)
    if race_type == "READ_WRITE":
        if h1 == "GET" and _is_readonly_method(m1) and not m1.startswith("check"):
            return PreFilterResult("FALSE_POSITIVE", "MEDIUM", 2,
                f"{m1} is a plain read (GET); reading stale data is benign unless it gates a write decision.")

    # 3. Admin endpoint vs admin endpoint on config entity — both rare, serialised by ops
    if _is_admin_endpoint(ep1) and _is_admin_endpoint(ep2) and entity in ADMIN_CONFIG_ENTITIES:
        return PreFilterResult("FALSE_POSITIVE", "MEDIUM", 2,
            f"Both endpoints are admin-only paths on config entity {entity}; "
            f"admin operations are serialised by deployment convention, not concurrent user traffic.")

    # 4. Endpoints with different scoping ID params in path (partitioned data)
    if _path_has_id_param(p1) and _path_has_id_param(p2):
        # Both scoped to a specific record — only race if same ID, which is unlikely
        # but NOT a guaranteed FP (two users could hit the same order), so → UNCERTAIN
        pass   # fall through to LLM

    # ── Hard REAL rules ──────────────────────────────────────────

    # 5. Both endpoints write to a transactional entity (Order/Payment) → high risk
    if w1 and w2 and entity in TRANSACTIONAL_ENTITIES and race_type == "WRITE_WRITE":
        return PreFilterResult("REAL", "HIGH", 9,
            f"Both {m1} (HTTP {h1}) and {m2} (HTTP {h2}) mutate the {entity} entity; "
            f"concurrent calls with no distributed lock cause lost updates or double-processing.")

    # 6. payOrder / modifyOrder together with createNewOrder — classic TOCTOU
    if entity in TRANSACTIONAL_ENTITIES and (
        ("pay" in m1 or "pay" in m2) or ("modif" in m1 or "modif" in m2)
    ) and ("create" in m1 or "create" in m2):
        return PreFilterResult("REAL", "HIGH", 9,
            f"createOrder + {m2 if 'create' in m1 else m1} on {entity}: "
            f"a payment or status change can race with order creation causing inconsistent state.")

    # 7. Two non-admin WRITE endpoints on same config entity
    if w1 and w2 and entity in ADMIN_CONFIG_ENTITIES and not (_is_admin_endpoint(ep1) and _is_admin_endpoint(ep2)):
        return PreFilterResult("REAL", "MEDIUM", 6,
            f"{m1} and {m2} both write {entity}; while config changes are infrequent, "
            f"concurrent writes without optimistic locking can cause lost updates.")

    # ── Needs LLM for nuanced reasoning ─────────────────────────
    return PreFilterResult("NEEDS_LLM", "LOW", 5, "")


# ── SARIF parsing ────────────────────────────────────────────────────────────

def parse_sarif(sarif_path: str) -> list[dict]:
    path = Path(sarif_path)
    if not path.exists():
        raise FileNotFoundError(f"SARIF file not found: {sarif_path}")

    with open(path) as f:
        sarif = json.load(f)

    races = []
    for run in sarif.get("runs", []):
        for result in run.get("results", []):
            props = result.get("properties", {})

            locs = result.get("locations", [{}])
            phys = locs[0].get("physicalLocation", {}) if locs else {}
            uri  = phys.get("artifactLocation", {}).get("uri", "")
            line = phys.get("region", {}).get("startLine", 0)

            rel_locs = result.get("relatedLocations", [])
            rel_uri, rel_line = uri, line
            if rel_locs:
                rp = rel_locs[0].get("physicalLocation", {})
                rel_uri  = rp.get("artifactLocation", {}).get("uri", uri)
                rel_line = rp.get("region", {}).get("startLine", line)

            race = {
                "rule_id":    result.get("ruleId", ""),
                "level":      result.get("level", "warning"),
                "message":    result.get("message", {}).get("text", ""),
                "entity":     props.get("entity", ""),
                "race_type":  props.get("raceType", ""),
                "protection": props.get("protectionStatus", "UNPROTECTED"),
                "endpoint1":  props.get("endpoint1", ""),
                "endpoint2":  props.get("endpoint2", ""),
                "file1":      uri,
                "line1":      line,
                "file2":      rel_uri,
                "line2":      rel_line,
                # Enrichment
                "http1":      _http_verb(props.get("endpoint1", "")),
                "http2":      _http_verb(props.get("endpoint2", "")),
                "method1":    _method_from_ep(props.get("endpoint1", "")),
                "method2":    _method_from_ep(props.get("endpoint2", "")),
                "is_transactional": props.get("entity", "") in TRANSACTIONAL_ENTITIES,
                "is_admin_config":  props.get("entity", "") in ADMIN_CONFIG_ENTITIES,
            }
            races.append(race)

    return races


def get_code_snippet(source_root: str, file_uri: str, line: int, ctx: int = 6) -> str:
    if not source_root or not file_uri:
        return ""
    clean = file_uri.lstrip("./").lstrip("/")
    candidates = [
        Path(source_root) / clean,
        Path(source_root) / Path(clean).name,
    ]
    for p in candidates:
        if p.exists():
            try:
                lines_list = p.read_text(errors="replace").splitlines()
                s = max(0, line - ctx - 1)
                e = min(len(lines_list), line + ctx)
                return "\n".join(f"{s+i+1}: {l}" for i, l in enumerate(lines_list[s:e]))
            except Exception:
                pass
    return ""


def group_by_entity(races: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list] = {}
    for r in races:
        groups.setdefault(r["entity"], []).append(r)
    return groups


def severity(race: dict) -> str:
    return "CRITICAL" if race["level"] == "error" else "HIGH"