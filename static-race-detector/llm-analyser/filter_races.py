import os
import sys
import argparse
import time
from collections import defaultdict

from sarif_parser import parse_sarif, group_by_entity, severity
from github_client import GitHubModelsClient, PREFERRED_MODELS
from report_writer import write_all

BATCH_SIZE = 10   # races per API call — keeps prompts tiny


def pick_model(args_model: str | None) -> str:
    if args_model:
        return args_model
    return PREFERRED_MODELS[0]


def estimate_calls(races: list[dict]) -> int:
    groups = group_by_entity(races)
    total = 0
    for entity_races in groups.values():
        total += -(-len(entity_races) // BATCH_SIZE)   # ceiling division
    return total


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Models LLM filter for static race detector SARIF output"
    )
    parser.add_argument("sarif", help="Path to race-report.sarif")
    parser.add_argument("--token", default=None,
                        help="GitHub PAT (or set GITHUB_TOKEN env var)")
    parser.add_argument("--model", default=None,
                        help=f"Model to use (default: {PREFERRED_MODELS[0]}). "
                             f"Options: {', '.join(PREFERRED_MODELS)}")
    parser.add_argument("--source-root", default=None,
                        help="Source root for code snippets (optional, improves accuracy)")
    parser.add_argument("--severity", default="ALL",
                        choices=["ALL", "CRITICAL", "HIGH"],
                        help="Pre-filter by severity before LLM analysis")
    parser.add_argument("--top-n", type=int, default=None,
                        help="Analyse only first N races (good for testing)")
    parser.add_argument("--output", default="filtered-races.json")
    parser.add_argument("--report", default="race-analysis-report.md")
    args = parser.parse_args()

    print("╔═════════════════════════════════════════════════════════════╗")
    print("║    LLM Race Filter  —  Parsing the races in sarif           ║")
    print("╚═════════════════════════════════════════════════════════════╝\n")

    # --- Auth ---
    token = args.token or os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("✗  No GitHub token found.")
        print("   Set GITHUB_TOKEN env var or pass --token ghp_xxx")
        print("   Get one at: https://github.com/settings/tokens")
        print("   Required permission: models:read")
        sys.exit(1)

    model = pick_model(args.model)
    print(f"✓ Model   : {model}")
    print(f"✓ Token   : {token[:8]}{'*' * (len(token)-8)}\n")

    # --- Parse SARIF ---
    print(f"→ Parsing {args.sarif} ...")
    races = parse_sarif(args.sarif)
    print(f"  Total races in SARIF : {len(races)}")

    # Pre-filter severity
    if args.severity != "ALL":
        level_filter = "error" if args.severity == "CRITICAL" else "warning"
        races = [r for r in races if r["level"] == level_filter]
        print(f"  After {args.severity} filter  : {len(races)}")

    # Top-N for testing
    if args.top_n:
        races = races[:args.top_n]
        print(f"  Limited to top-N     : {len(races)}")

    est = estimate_calls(races)


    if est > 140:
        print("⚠  Warning: This may approach the daily limit.")
        print("   Consider --severity CRITICAL or --top-n to reduce calls.\n")

    # --- Run analysis ---
    client = GitHubModelsClient(token=token, model=model)
    all_results = []
    groups = group_by_entity(races)

    total_groups = len(groups)
    for g_idx, (entity, entity_races) in enumerate(groups.items(), 1):
        print(f"[{g_idx}/{total_groups}] Entity: {entity}  ({len(entity_races)} races)")

        # Chunk into batches of BATCH_SIZE
        for b_start in range(0, len(entity_races), BATCH_SIZE):
            chunk = entity_races[b_start:b_start + BATCH_SIZE]
            b_num = b_start // BATCH_SIZE + 1
            b_total = -(-len(entity_races) // BATCH_SIZE)
            if b_total > 1:
                print(f"  Batch {b_num}/{b_total} ({len(chunk)} races)")

            results = client.analyse_batch(entity, chunk, args.source_root)
            all_results.extend(results)

        print()

    # --- Summary ---
    real = [r for r in all_results if r.verdict == "REAL"]
    fp   = [r for r in all_results if r.verdict == "FALSE_POSITIVE"]
    unc  = [r for r in all_results if r.verdict == "UNCERTAIN"]

    print("=" * 58)
    print(f"  🔴 REAL races      : {len(real)}")
    print(f"  ✅ False Positives : {len(fp)}")
    print(f"  🟡 Uncertain       : {len(unc)}")
    print(f"  Total analysed     : {len(all_results)}")
    print("=" * 58)

    # Top 10 highest-risk
    top = sorted(real, key=lambda x: -x.risk_score)[:10]
    if top:
        print("\nTop 10 highest-risk REAL races:")
        for i, r in enumerate(top, 1):
            sev = severity(r.race)
            ep1 = r.race["endpoint1"].split("(")[-1].rstrip(")")
            ep2 = r.race["endpoint2"].split("(")[-1].rstrip(")")
            print(f"  {i:2}. [{sev}] {r.race['entity']}  risk={r.risk_score}/10")
            print(f"      {ep1} ↔ {ep2}")
            print(f"      → {getattr(r, 'justification', 'No justification provided')[:80]}")

    # --- Write outputs ---
    write_all(all_results, args.output, args.report)
    print(f"\n✓ JSON  → {args.output}")
    print(f"✓ MD    → {args.report}")


if __name__ == "__main__":
    main()
