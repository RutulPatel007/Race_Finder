"""
Layer 2: LLM Self-Consistency Voting

Instead of relying on a single LLM call, run N independent passes
with higher temperature and take the majority vote. This provides:
- Natural calibrated confidence (agreement ratio)
- Robustness against hallucination
- No labeled data required
"""
import time
from typing import List, Tuple
from models import RaceVerificationRequest, RaceVerificationResponse, Verdict
import config


def self_consistency_vote(model, request: RaceVerificationRequest,
                           n_passes: int = None) -> Tuple[Verdict, float, List[RaceVerificationResponse]]:
    """
    Run N independent LLM passes with diverse sampling and take majority vote.
    
    Args:
        model: Configured Gemini model
        request: The verification request with code slices
        n_passes: Number of passes (default from config)
    
    Returns:
        majority_verdict: The winning verdict
        agreement_score: Agreement ratio (0.0-1.0)
        responses: All individual responses
    """
    from llm_verifier import verify_race

    if n_passes is None:
        n_passes = config.SELF_CONSISTENCY_PASSES

    responses: List[RaceVerificationResponse] = []

    for i in range(n_passes):
        response = verify_race(
            model, request,
            generation_config=config.SELF_CONSISTENCY_GENERATION_CONFIG
        )
        if response is not None:
            responses.append(response)
        # Delay between passes to avoid bursting the rate limit
        if i < n_passes - 1:
            time.sleep(getattr(config, 'SELF_CONSISTENCY_PASS_DELAY', 2.0))

    if not responses:
        # All passes failed — default to TRUE_POSITIVE (conservative)
        return Verdict.TRUE_POSITIVE, 0.0, []

    # Count votes
    tp_votes = sum(1 for r in responses if r.verdict == Verdict.TRUE_POSITIVE)
    fp_votes = sum(1 for r in responses if r.verdict == Verdict.FALSE_POSITIVE)
    total = len(responses)

    # Majority vote
    if tp_votes > fp_votes:
        majority = Verdict.TRUE_POSITIVE
        agreement = tp_votes / total
    elif fp_votes > tp_votes:
        majority = Verdict.FALSE_POSITIVE
        agreement = fp_votes / total
    else:
        # Tie — default to TRUE_POSITIVE (conservative, prefer not to miss bugs)
        majority = Verdict.TRUE_POSITIVE
        agreement = 0.5

    return majority, agreement, responses
