"""
Pydantic models for structured LLM input/output.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum


class Verdict(str, Enum):
    TRUE_POSITIVE = "TRUE_POSITIVE"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class RaceType(str, Enum):
    WRITE_WRITE = "WRITE_WRITE"
    READ_WRITE = "READ_WRITE"


class ProtectionStatus(str, Enum):
    UNPROTECTED = "UNPROTECTED"
    PARTIALLY_PROTECTED = "PARTIALLY_PROTECTED"
    FULLY_PROTECTED = "FULLY_PROTECTED"


class CodeSlice(BaseModel):
    """Extracted code from a Java source file."""
    class_name: str
    method_name: str
    method_source: str
    class_fields: str = ""
    file_path: str = ""
    line_number: int = 0


class RaceCandidate(BaseModel):
    """A potential race from Phase 1 SARIF output."""
    entity: str
    endpoint1_name: str
    endpoint2_name: str
    endpoint1_http: str = ""
    endpoint2_http: str = ""
    race_type: RaceType
    severity: str
    protection_status: ProtectionStatus = ProtectionStatus.UNPROTECTED
    source_file_1: str = ""
    source_file_2: str = ""
    line_number_1: int = 0
    line_number_2: int = 0
    description: str = ""


class RaceVerificationRequest(BaseModel):
    """Input to the LLM verifier."""
    entity: str
    endpoint1_name: str
    endpoint1_http: str
    endpoint1_code: str
    endpoint2_name: str
    endpoint2_http: str
    endpoint2_code: str
    race_type: str
    protection_status: str


class RaceVerificationResponse(BaseModel):
    """Structured LLM output."""
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    race_pattern: Optional[str] = None
    mitigation_suggestion: Optional[str] = None


class PruningResult(BaseModel):
    """Final result after all pruning layers."""
    candidate: RaceCandidate
    static_score: float = Field(ge=0.0, le=1.0, description="Score from static heuristic pruning")
    llm_agreement_score: float = Field(ge=0.0, le=1.0, description="Agreement ratio from self-consistency")
    final_score: float = Field(ge=0.0, le=1.0, description="Weighted combination of static and LLM scores")
    final_verdict: Verdict
    reasoning: str = ""
    race_pattern: Optional[str] = None
    mitigation_suggestion: Optional[str] = None
    llm_responses: list[RaceVerificationResponse] = Field(default_factory=list)
    static_flags: list[str] = Field(default_factory=list, description="Static pruning rules that fired")
