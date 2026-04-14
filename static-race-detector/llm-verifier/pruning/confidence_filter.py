"""
Layer 3: Confidence-Weighted Filtering

Combines static heuristic scores with LLM self-consistency agreement
into a final confidence score, then filters based on configurable thresholds.

Formula: final_score = (STATIC_WEIGHT × static_score) + (LLM_WEIGHT × llm_agreement_score)

Thresholds:
- final_score >= 0.7  → TRUE_POSITIVE  (confirmed race)
- 0.4 <= final_score  → NEEDS_REVIEW   (requires human review)
- final_score < 0.4   → FALSE_POSITIVE (suppressed)
"""
from typing import List
from models import PruningResult, RaceCandidate, Verdict, RaceVerificationResponse
import config


def apply_confidence_filter(
    candidate: RaceCandidate,
    static_score: float,
    static_flags: List[str],
    llm_agreement_score: float,
    llm_verdict: Verdict,
    llm_responses: List[RaceVerificationResponse]
) -> PruningResult:
    """
    Combine static and LLM signals into a final verdict.
    """
    # Compute weighted final score
    final_score = (config.STATIC_WEIGHT * static_score) + (config.LLM_WEIGHT * llm_agreement_score)

    # If LLM majority says FALSE_POSITIVE, invert the LLM contribution
    if llm_verdict == Verdict.FALSE_POSITIVE:
        # LLM thinks it's safe — adjust score downward
        final_score = (config.STATIC_WEIGHT * static_score) + (config.LLM_WEIGHT * (1.0 - llm_agreement_score))

    # Apply thresholds
    if final_score >= config.CONFIDENCE_THRESHOLD_TRUE_POSITIVE:
        final_verdict = Verdict.TRUE_POSITIVE
    elif final_score >= config.CONFIDENCE_THRESHOLD_NEEDS_REVIEW:
        final_verdict = Verdict.NEEDS_REVIEW
    else:
        final_verdict = Verdict.FALSE_POSITIVE

    # Collect reasoning from the strongest LLM response
    reasoning = ""
    race_pattern = None
    mitigation = None
    if llm_responses:
        # Pick the response that matches the majority verdict with highest confidence
        matching = [r for r in llm_responses if r.verdict == llm_verdict]
        if matching:
            best = max(matching, key=lambda r: r.confidence)
            reasoning = best.reasoning
            race_pattern = best.race_pattern
            mitigation = best.mitigation_suggestion
        else:
            best = max(llm_responses, key=lambda r: r.confidence)
            reasoning = best.reasoning
            race_pattern = best.race_pattern
            mitigation = best.mitigation_suggestion

    return PruningResult(
        candidate=candidate,
        static_score=static_score,
        llm_agreement_score=llm_agreement_score,
        final_score=round(final_score, 3),
        final_verdict=final_verdict,
        reasoning=reasoning,
        race_pattern=race_pattern,
        mitigation_suggestion=mitigation,
        llm_responses=llm_responses,
        static_flags=static_flags
    )


def apply_static_only_filter(
    candidate: RaceCandidate,
    static_score: float,
    static_flags: List[str]
) -> PruningResult:
    """
    Static-only filtering — used when LLM is not available (no API key).
    Uses only the static score with adjusted thresholds.
    """
    if static_score >= 0.8:
        final_verdict = Verdict.TRUE_POSITIVE
    elif static_score >= 0.5:
        final_verdict = Verdict.NEEDS_REVIEW
    else:
        final_verdict = Verdict.FALSE_POSITIVE

    return PruningResult(
        candidate=candidate,
        static_score=static_score,
        llm_agreement_score=0.0,
        final_score=static_score,
        final_verdict=final_verdict,
        reasoning=f"Static analysis only. Flags: {', '.join(static_flags) if static_flags else 'None'}",
        static_flags=static_flags
    )
