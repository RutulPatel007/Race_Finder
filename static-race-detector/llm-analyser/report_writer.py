"""
report_writer.py — Writes filtered-races.json and race-report.md
"""
import json
from pathlib import Path
from datetime import datetime
from sarif_parser import severity


def write_all(results: list, json_out: str, md_out: str):
    _write_json(results, json_out)
    _write_md(results, md_out)


def _write_json(results: list, path: str):
    out = []
    for r in results:
        out.append({
            "verdict":       r.verdict,
            "confidence":    r.confidence,
            "risk_score":    r.risk_score,
            "justification": r.justification,
            "severity":      severity(r.race),
            "entity":        r.race["entity"],
            "race_type":     r.race["race_type"],
            "endpoint1":     r.race["endpoint1"],
            "endpoint2":     r.race["endpoint2"],
            "file":          r.race["file1"],
            "line":          r.race["line1"],
        })
    Path(path).write_text(json.dumps(out, indent=2))


def _write_md(results: list, path: str):
    real = sorted([r for r in results if r.verdict == "REAL"], key=lambda x: -x.risk_score)
    fp   = [r for r in results if r.verdict == "FALSE_POSITIVE"]
    unc  = [r for r in results if r.verdict == "UNCERTAIN"]

    lines = [
        "# Race Condition Filter — LLM Analysis Report",
        f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Model: GitHub Models*\n",
        "## Summary",
        "| Verdict | Count |",
        "|---------|-------|",
        f"| 🔴 REAL races | **{len(real)}** |",
        f"| ✅ False Positives | {len(fp)} |",
        f"| 🟡 Uncertain | {len(unc)} |",
        f"| Total analysed | {len(results)} |",
        "",
        "---",
        "## 🔴 Real Races — sorted by risk score",
        "",
    ]

    if real:
        for i, r in enumerate(real, 1):
            sev = severity(r.race)
            lines += [
                f"### {i}. `{r.race['entity']}` — {sev} | risk {r.risk_score}/10",
                f"- **Type:** {r.race['race_type']}",
                f"- **Confidence:** {r.confidence}",
                f"- **Endpoint 1:** `{r.race['endpoint1']}`",
                f"- **Endpoint 2:** `{r.race['endpoint2']}`",
                f"- **File:** `{r.race['file1']}` line {r.race['line1']}",
                f"- **Why it's real:** {r.justification}",
                "",
            ]
    else:
        lines.append("*None found.*\n")

    lines += ["---", "## 🟡 Uncertain — needs manual review", ""]
    for r in unc:
        sev = severity(r.race)
        ep1 = r.race["endpoint1"].split("(")[-1].rstrip(")")
        ep2 = r.race["endpoint2"].split("(")[-1].rstrip(")")
        lines.append(f"- `{r.race['entity']}` [{sev}] `{ep1}` ↔ `{ep2}` — *{r.justification}*")
    if not unc:
        lines.append("*None.*")

    lines += ["", "---", "## ✅ False Positives — filtered out", ""]
    for r in fp:
        ep1 = r.race["endpoint1"].split("(")[-1].rstrip(")")
        ep2 = r.race["endpoint2"].split("(")[-1].rstrip(")")
        lines.append(f"- ~~`{r.race['entity']}`~~ `{ep1}` ↔ `{ep2}` — *{r.justification}*")
    if not fp:
        lines.append("*None.*")

    lines += [
        "",
        "---",
        "## Fix Recommendations",
        "",
        "| Race Type | Recommended Fix |",
        "|-----------|----------------|",
        "| WRITE_WRITE on Order/Payment | Optimistic locking (`@Version`) + retry |",
        "| WRITE_WRITE on config entities | Pessimistic lock or admin serialisation |",
        "| READ_WRITE (TOCTOU) | Atomic compare-and-swap or DB constraint |",
        "| Any unprotected critical path | Redis distributed lock (Redisson) |",
    ]

    Path(path).write_text("\n".join(lines))
