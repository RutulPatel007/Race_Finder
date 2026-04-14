#!/usr/bin/env python3
"""
Race Finder — Phase 2: LLM Verification & Multi-Strategy Pruning Pipeline

Usage:
    # Full pipeline with Gemini Pro verification:
    python main.py --sarif ../race-report.sarif --source ../train-ticket

    # Static pruning only (no API key needed):
    python main.py --sarif ../race-report.sarif --source ../train-ticket --static-only

    # Custom thresholds:
    python main.py --sarif ../race-report.sarif --source ../train-ticket --tp-threshold 0.8 --review-threshold 0.5
"""
import sys
import os
import json
import time
import click
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from models import RaceCandidate, RaceVerificationRequest, PruningResult, Verdict
from sarif_parser import parse_sarif
from code_slicer import extract_code_slice, find_source_file
from pruning.static_pruner import apply_static_pruning
from pruning.confidence_filter import apply_confidence_filter, apply_static_only_filter

console = Console()


@click.command()
@click.option('--sarif', required=True, help='Path to Phase 1 SARIF report')
@click.option('--source', required=True, help='Path to microservices source root')
@click.option('--output', default='verified-report.sarif', help='Output SARIF file path')
@click.option('--static-only', is_flag=True, help='Skip LLM verification, use static pruning only')
@click.option('--tp-threshold', type=float, default=None, help='TRUE_POSITIVE confidence threshold (default: 0.7)')
@click.option('--review-threshold', type=float, default=None, help='NEEDS_REVIEW confidence threshold (default: 0.4)')
@click.option('--passes', type=int, default=None, help='Number of self-consistency passes (default: 3)')
@click.option('--max-candidates', type=int, default=None, help='Maximum candidates to verify (for cost control)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(sarif, source, output, static_only, tp_threshold, review_threshold, 
         passes, max_candidates, verbose):
    """Phase 2: LLM Verification & Pruning Pipeline for Race Finder."""
    
    import config
    
    # Apply custom thresholds if provided
    if tp_threshold is not None:
        config.CONFIDENCE_THRESHOLD_TRUE_POSITIVE = tp_threshold
    if review_threshold is not None:
        config.CONFIDENCE_THRESHOLD_NEEDS_REVIEW = review_threshold
    if passes is not None:
        config.SELF_CONSISTENCY_PASSES = passes

    console.print(Panel.fit(
        "[bold cyan]Race Finder — Phase 2: LLM Verification & Pruning[/bold cyan]\n"
        f"SARIF Input: {sarif}\n"
        f"Source Root: {source}\n"
        f"Mode: {'Static Only' if static_only else 'Full Pipeline (Gemini Pro)'}",
        title="🏁 Race Finder v2.0"
    ))

    # ─── Step 1: Parse SARIF ───
    console.print("\n[bold]Step 1/4: Parsing SARIF report...[/bold]")
    candidates = parse_sarif(sarif)
    console.print(f"  Found [bold]{len(candidates)}[/bold] race candidates from Phase 1")

    if not candidates:
        console.print("[yellow]No candidates to verify. Exiting.[/yellow]")
        return

    if max_candidates:
        candidates = candidates[:max_candidates]
        console.print(f"  Limited to first [bold]{max_candidates}[/bold] candidates")

    # ─── Step 2: Static Pruning (Layer 1) ───
    console.print("\n[bold]Step 2/4: Applying static heuristic pruning...[/bold]")
    static_results = []
    for candidate in candidates:
        score, flags = apply_static_pruning(candidate, source)
        static_results.append((candidate, score, flags))

    suppressed_by_static = sum(1 for _, score, _ in static_results if score < 0.3)
    console.print(f"  Static pruning suppressed [bold]{suppressed_by_static}[/bold] candidates")
    console.print(f"  Remaining for LLM verification: [bold]{len(candidates) - suppressed_by_static}[/bold]")

    # ─── Step 3: LLM Verification (Layer 2 + 3) ───
    results: list[PruningResult] = []

    if static_only or not config.GOOGLE_API_KEY:
        if not static_only and not config.GOOGLE_API_KEY:
            console.print("\n[yellow]⚠ GOOGLE_API_KEY not set. Falling back to static-only mode.[/yellow]")
            console.print("[yellow]  Set it with: export GOOGLE_API_KEY='your-key'[/yellow]")

        console.print("\n[bold]Step 3/4: Static-only filtering...[/bold]")
        for candidate, score, flags in static_results:
            result = apply_static_only_filter(candidate, score, flags)
            results.append(result)
    else:
        console.print(f"\n[bold]Step 3/4: LLM verification with Gemini Pro ({config.SELF_CONSISTENCY_PASSES} passes each)...[/bold]")
        
        from llm_verifier import create_client
        from pruning.self_consistency import self_consistency_vote

        try:
            model = create_client()
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            return

        # ── Entity-level deduplication ──────────────────────────────────────────
        # Group candidates by entity. Verify only ONE representative per entity
        # (chosen by severity + race type), then propagate the verdict to all
        # duplicates.  This reduces 604 candidates → ≤17 LLM calls.
        from collections import defaultdict
        entity_groups: dict = defaultdict(list)
        for item in static_results:
            entity_groups[item[0].entity].append(item)

        # Pick the "best" representative: prefer WRITE_WRITE, then CRITICAL severity
        def _representative_key(item):
            candidate, score, _ = item
            ww_bonus = 0 if candidate.race_type.value == "WRITE_WRITE" else 1
            sev_bonus = 0 if candidate.severity == "CRITICAL" else 1
            return (ww_bonus, sev_bonus, -score)

        representatives = {}  # entity → (candidate, static_score, static_flags)
        for entity, group in entity_groups.items():
            group.sort(key=_representative_key)
            representatives[entity] = group[0]

        console.print(f"  [dim]Entity deduplication: {len(static_results)} pairs → "
                      f"{len(representatives)} unique entities to verify[/dim]")

        entity_verdicts: dict = {}  # entity → (llm_verdict, agreement, llm_responses)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("Verifying...", total=len(representatives))

            for entity, (rep_candidate, rep_score, rep_flags) in representatives.items():
                progress.update(task, description=f"Verifying entity: {entity}...")

                # Skip candidates already suppressed by static analysis
                if rep_score < 0.2:
                    entity_verdicts[entity] = None  # will use static-only
                    progress.advance(task)
                    continue

                # Build verification request with code slices
                request = _build_verification_request(rep_candidate, source)

                if request is None:
                    entity_verdicts[entity] = None  # no source, use static-only
                    progress.advance(task)
                    continue

                # Self-consistency voting (N passes with delay between them)
                llm_verdict, agreement, llm_responses = self_consistency_vote(model, request)
                entity_verdicts[entity] = (llm_verdict, agreement, llm_responses)
                progress.advance(task)

                # Delay between entities to stay within rate limits
                time.sleep(0.5)

        # ── Apply verdicts to all candidates in each group ──────────────────────
        for candidate, static_score, static_flags in static_results:
            verdict_data = entity_verdicts.get(candidate.entity)
            if verdict_data is None:
                result = apply_static_only_filter(candidate, static_score, static_flags)
            else:
                llm_verdict, agreement, llm_responses = verdict_data
                result = apply_confidence_filter(
                    candidate, static_score, static_flags,
                    agreement, llm_verdict, llm_responses
                )
            results.append(result)

    # ─── Step 4: Generate Output ───
    console.print("\n[bold]Step 4/4: Generating verified report...[/bold]")

    tp_count = sum(1 for r in results if r.final_verdict == Verdict.TRUE_POSITIVE)
    nr_count = sum(1 for r in results if r.final_verdict == Verdict.NEEDS_REVIEW)
    fp_count = sum(1 for r in results if r.final_verdict == Verdict.FALSE_POSITIVE)

    # Print summary table
    table = Table(title="Verification Summary", show_header=True, header_style="bold cyan")
    table.add_column("Category", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Status", justify="center")
    table.add_row("TRUE POSITIVE", str(tp_count), "🔴 Confirmed Races")
    table.add_row("NEEDS REVIEW", str(nr_count), "🟡 Requires Human Review")
    table.add_row("FALSE POSITIVE", str(fp_count), "🟢 Suppressed")
    table.add_row("─" * 15, "─" * 5, "─" * 25)
    table.add_row("Total", str(len(results)), "")
    console.print(table)

    # Show top confirmed races
    if verbose:
        confirmed = [r for r in results if r.final_verdict == Verdict.TRUE_POSITIVE]
        if confirmed:
            console.print(f"\n[bold]Top Confirmed Races ({min(10, len(confirmed))}):[/bold]")
            for i, r in enumerate(confirmed[:10]):
                console.print(f"  [{i+1}] [red]{r.candidate.severity}[/red] | "
                             f"Entity: [bold]{r.candidate.entity}[/bold] | "
                             f"Score: {r.final_score:.2f}")
                console.print(f"      EP1: {r.candidate.endpoint1_name} ({r.candidate.endpoint1_http})")
                console.print(f"      EP2: {r.candidate.endpoint2_name} ({r.candidate.endpoint2_http})")
                if r.race_pattern:
                    console.print(f"      Pattern: [yellow]{r.race_pattern}[/yellow]")
                if r.reasoning:
                    console.print(f"      Reasoning: {r.reasoning[:120]}...")

    # Generate enhanced SARIF
    _generate_verified_sarif(results, output)
    console.print(f"\n[green]✓ Verified report written to: {output}[/green]")

    # Reduction statistics
    reduction = ((fp_count + nr_count) / len(results) * 100) if results else 0
    console.print(f"[bold green]Reduction: {reduction:.1f}% of candidates pruned from Phase 1[/bold green]")


def _build_verification_request(candidate: RaceCandidate, source_root: str):
    """Build a verification request with code slices for both endpoints."""
    # Extract class names
    ep1_parts = candidate.endpoint1_name.split(".")
    ep2_parts = candidate.endpoint2_name.split(".")

    ep1_class = ep1_parts[0] if ep1_parts else ""
    ep1_method = ep1_parts[1] if len(ep1_parts) > 1 else ""
    ep2_class = ep2_parts[0] if ep2_parts else ""
    ep2_method = ep2_parts[1] if len(ep2_parts) > 1 else ""

    # Try to get code slices
    code1 = "// Source not available"
    code2 = "// Source not available"

    # Try from SARIF source file paths first
    if candidate.source_file_1:
        slice1 = extract_code_slice(candidate.source_file_1, ep1_class, ep1_method, candidate.line_number_1)
        if slice1:
            code1 = f"// Fields:\n{slice1.class_fields}\n\n// Method:\n{slice1.method_source}"

    if candidate.source_file_2:
        slice2 = extract_code_slice(candidate.source_file_2, ep2_class, ep2_method, candidate.line_number_2)
        if slice2:
            code2 = f"// Fields:\n{slice2.class_fields}\n\n// Method:\n{slice2.method_source}"

    # If code not found from SARIF paths, search by class name
    if code1 == "// Source not available" and ep1_class:
        file_path = find_source_file(source_root, ep1_class)
        if file_path:
            slice1 = extract_code_slice(file_path, ep1_class, ep1_method)
            if slice1:
                code1 = f"// Fields:\n{slice1.class_fields}\n\n// Method:\n{slice1.method_source}"

    if code2 == "// Source not available" and ep2_class:
        file_path = find_source_file(source_root, ep2_class)
        if file_path:
            slice2 = extract_code_slice(file_path, ep2_class, ep2_method)
            if slice2:
                code2 = f"// Fields:\n{slice2.class_fields}\n\n// Method:\n{slice2.method_source}"

    # Both must have some code for meaningful verification
    if code1 == "// Source not available" and code2 == "// Source not available":
        return None

    return RaceVerificationRequest(
        entity=candidate.entity,
        endpoint1_name=candidate.endpoint1_name,
        endpoint1_http=candidate.endpoint1_http,
        endpoint1_code=code1,
        endpoint2_name=candidate.endpoint2_name,
        endpoint2_http=candidate.endpoint2_http,
        endpoint2_code=code2,
        race_type=candidate.race_type.value,
        protection_status=candidate.protection_status.value
    )


def _generate_verified_sarif(results: list, output_path: str):
    """Generate a SARIF report with verification verdicts."""
    sarif = {
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "RaceFinder-Verifier",
                    "version": "2.0.0",
                    "informationUri": "https://github.com/RutulPatel007/Race_Finder"
                }
            },
            "results": []
        }]
    }

    for r in results:
        # Only include TRUE_POSITIVE and NEEDS_REVIEW in the output
        if r.final_verdict == Verdict.FALSE_POSITIVE:
            continue

        level = "error" if r.final_verdict == Verdict.TRUE_POSITIVE else "note"
        rule_id = "VERIFIED-RACE" if r.final_verdict == Verdict.TRUE_POSITIVE else "REVIEW-RACE"

        result = {
            "ruleId": rule_id,
            "level": level,
            "message": {
                "text": (f"[{r.final_verdict.value}] {r.candidate.description}\n"
                        f"Confidence: {r.final_score:.2f} | "
                        f"Static: {r.static_score:.2f} | "
                        f"LLM Agreement: {r.llm_agreement_score:.2f}")
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": r.candidate.source_file_1 or "unknown"
                    }
                }
            }],
            "properties": {
                "entity": r.candidate.entity,
                "verdict": r.final_verdict.value,
                "confidence": r.final_score,
                "static_score": r.static_score,
                "llm_agreement": r.llm_agreement_score,
                "race_type": r.candidate.race_type.value,
                "endpoint1": r.candidate.endpoint1_name,
                "endpoint2": r.candidate.endpoint2_name,
                "reasoning": r.reasoning,
                "race_pattern": r.race_pattern,
                "mitigation": r.mitigation_suggestion,
                "static_flags": r.static_flags
            }
        }
        sarif["runs"][0]["results"].append(result)

    with open(output_path, 'w') as f:
        json.dump(sarif, f, indent=2, default=str)


if __name__ == "__main__":
    main()
