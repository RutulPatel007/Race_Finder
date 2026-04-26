"""
Configuration for the LLM Verifier pipeline.
Manages Gemini API keys, model settings, and prompt templates for all SRC stages.
"""
import os

# ─── Gemini Configuration ───
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

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

# ─── Rate Limiting ───
RATE_LIMIT_DELAY = 4.0  # Seconds between LLM calls (free tier ~15 RPM)
RATE_LIMIT_RETRY_BASE = 5.0  # Base seconds for exponential backoff on 429
RATE_LIMIT_MAX_RETRIES = 5

# ─── SRC Pipeline Stage Prompts ───

# Stage 1: Evidence Extraction — Chain-of-Thought fact extraction
EVIDENCE_SYSTEM_PROMPT = """You are a meticulous code analyst specializing in Java/Spring microservice architectures.
Your ONLY job is to extract observable facts from code. You do NOT make judgments about races or bugs.
Think step by step about what each endpoint does to the database."""

EVIDENCE_EXTRACTION_PROMPT = """Analyze these two endpoints and extract ONLY observable structural facts.
Do NOT judge whether a race exists. Only report what the code actually does.

## Shared Entity: {entity_name}

## Endpoint 1: {ep1_name} ({ep1_http})
```java
{ep1_code}
```

## Endpoint 2: {ep2_name} ({ep2_http})
```java
{ep2_code}
```

## Additional Context
- Protection Status (from static analysis): {protection_status}
- Race Type: {race_type}
{state_machine_context}

Think step by step:
1. What database operation does Endpoint 1 perform? (INSERT/UPDATE/DELETE/SELECT/UPSERT)
2. Does Endpoint 1 receive or look up by a specific entity ID, or does it create a new one?
3. Does Endpoint 1 check any state/status before writing?
4. What state/status does Endpoint 1 set after writing?
5. Repeat steps 1-4 for Endpoint 2.
6. Are both endpoints in the same microservice (same package/module)?
7. Do they modify the same fields of the entity?

Respond with ONLY a JSON object matching this schema — no extra text:
{{
  "ep1_db_operation": "INSERT|UPDATE|DELETE|SELECT|UPSERT|NONE",
  "ep1_uses_id_param": true/false,
  "ep1_creates_new_record": true/false,
  "ep1_state_precondition": "<state checked before write, or null>",
  "ep1_state_transition": "<state set after write, or null>",
  "ep2_db_operation": "INSERT|UPDATE|DELETE|SELECT|UPSERT|NONE",
  "ep2_uses_id_param": true/false,
  "ep2_creates_new_record": true/false,
  "ep2_state_precondition": "<state checked before write, or null>",
  "ep2_state_transition": "<state set after write, or null>",
  "shared_field_access": true/false,
  "same_service": true/false,
  "notes": "<any other structural observation>"
}}"""

# Few-shot example for evidence extraction
EVIDENCE_FEW_SHOT_EXAMPLE = """
Example — for endpoints createOrder(POST) and payOrder(PUT) on entity Order:
{{
  "ep1_db_operation": "INSERT",
  "ep1_uses_id_param": false,
  "ep1_creates_new_record": true,
  "ep1_state_precondition": null,
  "ep1_state_transition": "NOTPAID",
  "ep2_db_operation": "UPDATE",
  "ep2_uses_id_param": true,
  "ep2_creates_new_record": false,
  "ep2_state_precondition": "NOTPAID",
  "ep2_state_transition": "PAID",
  "shared_field_access": false,
  "same_service": true,
  "notes": "EP1 creates a new Order with a fresh UUID. EP2 looks up an existing Order by orderId parameter. They operate on different record instances at any given time."
}}
"""

# Stage 3: Adversarial Debate — Prosecutor
PROSECUTOR_SYSTEM_PROMPT = """You are a security researcher and concurrency expert.
Your job is to construct the STRONGEST POSSIBLE argument that a data race exists.
Be specific about exact interleaving scenarios. Do not be vague.
Think step by step about how concurrent requests could cause data corruption."""

PROSECUTOR_PROMPT = """Given these verified facts about two endpoints accessing entity "{entity_name}":

## Evidence (verified facts):
{evidence_json}

## Endpoint 1: {ep1_name} ({ep1_http})
```java
{ep1_code}
```

## Endpoint 2: {ep2_name} ({ep2_http})
```java
{ep2_code}
```

Think step by step:
1. Can both endpoints operate on the SAME record instance at the same time?
2. If yes, what exact sequence of steps (interleaving) causes data corruption?
3. How likely is this interleaving in production traffic (not just theory)?
4. What specific data inconsistency would result?

Construct your STRONGEST argument that this is a real, exploitable race condition.
If you honestly cannot find a convincing argument, say so — do not fabricate one.

Respond with ONLY JSON:
{{
  "argument": "<your strongest argument for the race existing>",
  "specific_interleaving": "<step-by-step interleaving: T1 does X, T2 does Y, ...>",
  "production_likelihood": "LOW|MEDIUM|HIGH",
  "key_evidence": "<the most important fact supporting your argument>"
}}"""

# Stage 3: Adversarial Debate — Defense
DEFENSE_SYSTEM_PROMPT = """You are a senior developer defending your code in a security review.
Your job is to construct the STRONGEST POSSIBLE argument that NO harmful race exists,
or that the reported race is a false positive.
Think step by step about why this code is actually safe."""

DEFENSE_PROMPT = """Given these verified facts about two endpoints accessing entity "{entity_name}":

## Evidence (verified facts):
{evidence_json}

## Endpoint 1: {ep1_name} ({ep1_http})
```java
{ep1_code}
```

## Endpoint 2: {ep2_name} ({ep2_http})
```java
{ep2_code}
```

Think step by step:
1. Do both endpoints even operate on the SAME record instance? Or different instances?
2. Are there state machine guards that prevent harmful interleavings?
3. Are there DB-level constraints (unique keys, foreign keys) that catch conflicts?
4. Is the write idempotent or self-correcting?
5. Is one endpoint admin-only or rarely called concurrently?
6. Are they in different microservices with separate databases?

Construct your STRONGEST defense that this is NOT a real race condition.
If you honestly cannot find a defense, say so — do not fabricate one.

Respond with ONLY JSON:
{{
  "argument": "<your strongest argument against the race>",
  "specific_interleaving": "<why the alleged interleaving cannot happen, or is harmless>",
  "production_likelihood": "LOW|MEDIUM|HIGH",
  "key_evidence": "<the most important fact supporting your defense>"
}}"""

# Stage 4: Judge Arbitration — Chain-of-Thought verdict
JUDGE_SYSTEM_PROMPT = """You are an experienced concurrency judge arbitrating a security review dispute.
You have seen the evidence, the prosecutor's argument, and the defense's argument.
You must issue a fair, well-reasoned final verdict.
Think step by step, weighing both arguments against the evidence."""

JUDGE_PROMPT = """You are judging whether a data race exists on entity "{entity_name}".

## Verified Evidence (Stage 1 — objective facts):
{evidence_json}

## Prosecutor's Argument (race EXISTS):
{prosecutor_json}

## Defense's Argument (race does NOT exist):
{defense_json}

Think step by step:
1. Does the evidence confirm that both endpoints can operate on the SAME record instance?
   - If EP1 creates new records and EP2 looks up by ID → they target different instances → defense wins.
2. If same-instance access is possible, does the prosecutor's interleaving scenario actually hold?
3. Does the defense identify protections (state guards, DB constraints, separate DBs) that block the interleaving?
4. What is your honest assessment of production likelihood?

Verdict rules:
- If endpoints CANNOT operate on the same record instance → FALSE_POSITIVE (confidence >= 0.8)
- If they CAN, and a specific harmful interleaving exists with MEDIUM/HIGH likelihood → TRUE_POSITIVE
- If they CAN, but the interleaving is LOW likelihood or unlikely in practice → NEEDS_REVIEW
- If evidence is ambiguous → NEEDS_REVIEW (confidence 0.3-0.5)

Respond with ONLY JSON:
{{
  "verdict": "TRUE_POSITIVE|FALSE_POSITIVE|NEEDS_REVIEW",
  "confidence": <float 0.0-1.0>,
  "winning_side": "prosecutor|defense|neither",
  "key_fact_used": "<specific evidence fact that decided this>",
  "reasoning": "<full reasoning trace>",
  "race_pattern": "<pattern name if TRUE_POSITIVE, e.g., 'Lost Update', 'Check-Then-Act'>",
  "mitigation_suggestion": "<suggested fix if TRUE_POSITIVE>"
}}"""


# ─── Legacy Prompt Templates (kept for static-only mode) ───

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
