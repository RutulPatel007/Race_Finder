import sys
import json
from collections import Counter
from sarif_parser import parse_sarif, group_by_entity, severity


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_parser.py race-report.sarif")
        sys.exit(1)

    sarif_path = sys.argv[1]
    print(f"Parsing {sarif_path}...")
    races = parse_sarif(sarif_path)
    print(f"✓ Parsed {len(races)} races\n")

    # Stats
    entity_counts = Counter(r["entity"] for r in races)
    type_counts   = Counter(r["race_type"] for r in races)
    sev_counts    = Counter(severity(r) for r in races)

    print(f"Severities : {dict(sev_counts)}")
    print(f"Race types : {dict(type_counts)}")
    print(f"\nTop 10 entities by race count:")
    for ent, cnt in entity_counts.most_common(10):
        print(f"  {ent:25s} : {cnt} races")

    groups = group_by_entity(races)
    from filter_races import BATCH_SIZE, estimate_calls
    est_calls = estimate_calls(races)
    print(f"\nAPI call estimate  : {est_calls} calls")
    print(f"Daily limit (free) : 150 calls")
    print(f"Margin             : {150 - est_calls} calls remaining\n")

    print("Sample race #0:")
    print(json.dumps(races[0], indent=2))

    print("\n✓ Parser OK. Now run:")
    print(f"  export GITHUB_TOKEN=ghp_xxxx")
    print(f"  python filter_races.py {sarif_path}")


if __name__ == "__main__":
    main()
