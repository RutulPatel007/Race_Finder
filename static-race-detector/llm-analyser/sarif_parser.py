"""
sarif_parser.py — Parse race-report.sarif into clean race dicts.
"""
import json
from pathlib import Path


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

            # Primary location
            locs = result.get("locations", [{}])
            phys = locs[0].get("physicalLocation", {}) if locs else {}
            uri  = phys.get("artifactLocation", {}).get("uri", "")
            line = phys.get("region", {}).get("startLine", 0)

            # Related location (second endpoint)
            rel_locs = result.get("relatedLocations", [])
            rel_uri, rel_line = uri, line
            if rel_locs:
                rp = rel_locs[0].get("physicalLocation", {})
                rel_uri  = rp.get("artifactLocation", {}).get("uri", uri)
                rel_line = rp.get("region", {}).get("startLine", line)

            race = {
                "rule_id":    result.get("ruleId", ""),
                "level":      result.get("level", "warning"),   # error=CRITICAL, warning=HIGH
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
            }
            races.append(race)

    return races


def get_code_snippet(source_root: str, file_uri: str, line: int, ctx: int = 6) -> str:
    """Read a small code window around a line number."""
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
                lines = p.read_text(errors="replace").splitlines()
                s = max(0, line - ctx - 1)
                e = min(len(lines), line + ctx)
                return "\n".join(f"{s+i+1}: {l}" for i, l in enumerate(lines[s:e]))
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
