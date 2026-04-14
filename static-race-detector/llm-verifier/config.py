"""
Configuration for the LLM Verifier pipeline.
Manages Gemini API keys, model settings, and prompt templates.
"""
import os

# ─── Gemini Configuration ───
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")

# Generation settings
GENERATION_CONFIG = {
    "temperature": 0.3,        # Low temperature for consistency in single-pass mode
    "top_p": 0.95,
    "max_output_tokens": 2048,
}

# Higher temperature for self-consistency voting (need diversity)
SELF_CONSISTENCY_GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "max_output_tokens": 2048,
}

# Self-consistency voting
SELF_CONSISTENCY_PASSES = 3  # Number of independent LLM passes per candidate
SELF_CONSISTENCY_PASS_DELAY = 2.0  # Seconds to wait between passes (avoids rate limiting)

# ─── Confidence Thresholds ───
CONFIDENCE_THRESHOLD_TRUE_POSITIVE = 0.7   # >= this → confirmed race
CONFIDENCE_THRESHOLD_NEEDS_REVIEW = 0.4    # >= this but < TP → needs human review
# Below NEEDS_REVIEW → suppressed as false positive

# Score weights for combining static and LLM signals
STATIC_WEIGHT = 0.4
LLM_WEIGHT = 0.6

# ─── Prompt Templates ───

SYSTEM_PROMPT = """You are a senior distributed systems architect and concurrency auditor. 
Your task is to analyze potential data race conditions in microservice architectures.

You will receive two code slices from different REST API endpoints or async handlers 
that both access the same database entity. At least one of them performs a WRITE operation.

Your job is to determine whether this represents a TRUE data race or a FALSE POSITIVE 
that is already handled by the application logic.

Consider the following when making your determination:

TRUE_POSITIVE indicators:
- No distributed locking mechanism protects the shared entity
- Check-Then-Act (TOCTOU) patterns without atomic operations
- Read-Modify-Write sequences without isolation guarantees
- No @Transactional annotation with appropriate isolation level
- No optimistic locking (@Version) on the entity
- Multiple services can invoke these endpoints concurrently in production

FALSE_POSITIVE indicators:
- Entity access is protected by distributed locks (Redis, Zookeeper, etc.)
- @Transactional with SERIALIZABLE or REPEATABLE_READ isolation
- Entity uses @Version for optimistic locking
- The operations are idempotent and safe to repeat
- The "write" is actually an upsert that handles conflicts
- The operations are sequenced by a saga orchestrator
- One endpoint is admin-only and not called concurrently in practice

Respond ONLY with valid JSON matching this exact schema:
{
    "verdict": "TRUE_POSITIVE" or "FALSE_POSITIVE",
    "confidence": <float between 0.0 and 1.0>,
    "reasoning": "<concise explanation of your determination>",
    "race_pattern": "<pattern name if TRUE_POSITIVE, e.g. 'Check-Then-Act', 'Read-Modify-Write', 'Lost Update'>",
    "mitigation_suggestion": "<suggested fix if TRUE_POSITIVE>"
}"""

VERIFICATION_PROMPT_TEMPLATE = """Analyze this potential {race_type} data race:

## Shared Entity: {entity_name}

## Endpoint 1: {endpoint1_name}
HTTP: {endpoint1_http}
```java
{endpoint1_code}
```

## Endpoint 2: {endpoint2_name}
HTTP: {endpoint2_http}
```java
{endpoint2_code}
```

## Additional Context
- Protection Status (from static analysis): {protection_status}
- Race Type: {race_type}

Determine if this is a TRUE_POSITIVE (real race) or FALSE_POSITIVE (already protected).
Respond with JSON only."""
