"""
Layer 1: Static Heuristic Pruning

Rule-based elimination of false positives using code pattern analysis.
No LLM needed — purely deterministic static rules.
"""
import re
import os
from typing import List, Tuple
from models import RaceCandidate, ProtectionStatus


# Each rule returns (should_suppress: bool, score_adjustment: float, rule_name: str)
# score_adjustment: 0.0 = fully protected (suppress), 1.0 = fully unprotected (keep)


def apply_static_pruning(candidate: RaceCandidate, source_root: str) -> Tuple[float, List[str]]:
    """
    Apply all static pruning rules to a race candidate.
    
    Returns:
        static_score: float 0.0-1.0 (0 = fully protected, 1 = fully unprotected)
        fired_rules: list of rule names that fired
    """
    score = 1.0  # Start fully unprotected
    fired_rules = []

    # Load source code for both endpoints
    source1 = _load_source(candidate.source_file_1, source_root)
    source2 = _load_source(candidate.source_file_2, source_root)

    rules = [
        _rule_protection_status,
        _rule_idempotent_reads,
        _rule_optimistic_locking,
        _rule_serializable_transaction,
        _rule_synchronized_access,
        _rule_distributed_lock_pattern,
        _rule_same_controller_internal,
        _rule_event_sourced_pattern,
    ]

    for rule in rules:
        adjustment, rule_name = rule(candidate, source1, source2)
        if adjustment < 1.0:
            score = min(score, adjustment)
            fired_rules.append(rule_name)

    return score, fired_rules


def _load_source(file_path: str, source_root: str) -> str:
    """Load source code from file, trying multiple path resolutions."""
    if not file_path:
        return ""

    candidates_to_try = [file_path]

    # SARIF URIs often include a leading project-folder prefix like
    # "train-ticket/ts-price-service/src/...".  Strip the first component
    # so we can resolve relative to source_root.
    parts = file_path.replace("\\", "/").split("/")
    if len(parts) > 1:
        candidates_to_try.append("/".join(parts[1:]))  # strip first segment

    for path in candidates_to_try:
        # Try absolute
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except Exception:
                pass

        # Try relative to source root
        joined = os.path.join(source_root, path)
        if os.path.exists(joined):
            try:
                with open(joined, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except Exception:
                pass

    return ""


def _rule_protection_status(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """Use the protection status already computed by Phase 1."""
    if candidate.protection_status == ProtectionStatus.FULLY_PROTECTED:
        return 0.0, "FULLY_PROTECTED_BY_PHASE1"
    elif candidate.protection_status == ProtectionStatus.PARTIALLY_PROTECTED:
        return 0.3, "PARTIALLY_PROTECTED_BY_PHASE1"
    return 1.0, ""


def _rule_idempotent_reads(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """
    If the race is READ_WRITE, check if the read side is truly idempotent.
    Pure findBy/getBy queries with no side effects are safe to run concurrently.
    """
    if candidate.race_type.value != "READ_WRITE":
        return 1.0, ""

    # Check if description reveals this is a simple finder vs. a write
    desc_lower = candidate.description.lower()
    read_patterns = ["findall", "findby", "getby", "queryall", "retrieve", "getall", "list"]
    
    # If one endpoint is a pure GET with simple finder, it's less dangerous
    if candidate.endpoint1_http.startswith("GET") or candidate.endpoint2_http.startswith("GET"):
        for pattern in read_patterns:
            if pattern in candidate.endpoint1_name.lower() or pattern in candidate.endpoint2_name.lower():
                return 0.6, "IDEMPOTENT_READ_ENDPOINT"

    return 1.0, ""


def _rule_optimistic_locking(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """
    Check if the entity class uses @Version annotation for optimistic locking.
    Search source files for @Version near the entity name.
    """
    entity = candidate.entity
    for source in [s1, s2]:
        if not source:
            continue
        # Check for @Version annotation in the same file or entity-related imports
        if "@Version" in source:
            return 0.1, f"OPTIMISTIC_LOCKING_@Version({entity})"

    return 1.0, ""


def _rule_serializable_transaction(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """Check if methods are wrapped in SERIALIZABLE transactions."""
    for source in [s1, s2]:
        if not source:
            continue
        if "SERIALIZABLE" in source and "@Transactional" in source:
            return 0.1, "SERIALIZABLE_TRANSACTION"
        if "REPEATABLE_READ" in source and "@Transactional" in source:
            return 0.2, "REPEATABLE_READ_TRANSACTION"

    return 1.0, ""


def _rule_synchronized_access(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """Check for synchronized blocks/methods around entity access."""
    for source in [s1, s2]:
        if not source:
            continue
        if re.search(r'synchronized\s*[\({]', source):
            return 0.2, "SYNCHRONIZED_ACCESS"

    return 1.0, ""


def _rule_distributed_lock_pattern(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """Check for distributed lock patterns (Redisson, Spring LockRegistry, etc.)."""
    lock_patterns = [
        r'\.tryLock\s*\(',
        r'\.lock\s*\(',
        r'LockRegistry',
        r'RedissonClient',
        r'RLock\s+',
        r'DistributedLock',
        r'@DistributedLock',
    ]
    for source in [s1, s2]:
        if not source:
            continue
        for pattern in lock_patterns:
            if re.search(pattern, source):
                return 0.1, "DISTRIBUTED_LOCK_DETECTED"

    return 1.0, ""


def _rule_same_controller_internal(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """
    If both endpoints are in the same controller and one calls the other internally,
    they're likely sequenced and not truly concurrent.
    """
    ep1_parts = candidate.endpoint1_name.split(".")
    ep2_parts = candidate.endpoint2_name.split(".")

    if len(ep1_parts) >= 2 and len(ep2_parts) >= 2:
        if ep1_parts[0] == ep2_parts[0]:  # Same class
            # Check if one method calls the other
            method1 = ep1_parts[-1] if len(ep1_parts) > 1 else ""
            method2 = ep2_parts[-1] if len(ep2_parts) > 1 else ""
            
            for source in [s1, s2]:
                if not source:
                    continue
                if method1 and method2:
                    if f"{method1}(" in source and f"{method2}(" in source:
                        return 0.5, "SAME_CONTROLLER_INTERNAL_CALL"

    return 1.0, ""


def _rule_event_sourced_pattern(candidate: RaceCandidate, s1: str, s2: str) -> Tuple[float, str]:
    """Check for event sourcing / CQRS patterns that handle ordering."""
    event_patterns = [
        "@Aggregate",
        "EventSourcingHandler",
        "CommandHandler",
        "AggregateLifecycle",
        "@EventHandler",
        "EventStore",
    ]
    for source in [s1, s2]:
        if not source:
            continue
        for pattern in event_patterns:
            if pattern in source:
                return 0.1, f"EVENT_SOURCED_PATTERN({pattern})"

    return 1.0, ""
