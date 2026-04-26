"""
Pydantic models for structured LLM input/output.
Includes pipeline state for LangGraph and all stage I/O types.
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


# ─── New models for LangGraph SRC Pipeline ───

class EvidenceRecord(BaseModel):
    """Stage 1 output: Structured facts extracted from code (no judgment)."""
    ep1_db_operation: str = Field(description="INSERT|UPDATE|DELETE|SELECT|UPSERT|NONE")
    ep1_uses_id_param: bool = Field(description="Does EP1 look up by a specific entity ID?")
    ep1_creates_new_record: bool = Field(description="Does EP1 create a new record?")
    ep1_state_precondition: Optional[str] = Field(default=None, description="State check before write, e.g., 'NOTPAID'")
    ep1_state_transition: Optional[str] = Field(default=None, description="State set after write, e.g., 'PAID'")
    ep2_db_operation: str = Field(description="INSERT|UPDATE|DELETE|SELECT|UPSERT|NONE")
    ep2_uses_id_param: bool = Field(description="Does EP2 look up by a specific entity ID?")
    ep2_creates_new_record: bool = Field(description="Does EP2 create a new record?")
    ep2_state_precondition: Optional[str] = Field(default=None, description="State check before write, e.g., 'NOTPAID'")
    ep2_state_transition: Optional[str] = Field(default=None, description="State set after write, e.g., 'PAID'")
    shared_field_access: bool = Field(default=True, description="Do both endpoints modify the same fields?")
    same_service: bool = Field(default=True, description="Are both endpoints in the same microservice?")
    notes: str = Field(default="", description="Any other structural observation")


class DebateArgument(BaseModel):
    """Stage 3 output: One side of the adversarial debate."""
    argument: str = Field(description="Core argument for or against race existing")
    specific_interleaving: Optional[str] = Field(default=None, description="Exact step-by-step interleaving scenario")
    production_likelihood: str = Field(default="MEDIUM", description="LOW|MEDIUM|HIGH")
    key_evidence: str = Field(default="", description="Most important fact supporting this argument")


class JudgeVerdict(BaseModel):
    """Stage 4 output: Final arbitrated verdict."""
    verdict: str = Field(description="TRUE_POSITIVE|FALSE_POSITIVE|NEEDS_REVIEW")
    confidence: float = Field(ge=0.0, le=1.0)
    winning_side: str = Field(description="prosecutor|defense|neither")
    key_fact_used: str = Field(description="The specific Stage 1 fact that decided this")
    reasoning: str = Field(description="Full reasoning trace")
    race_pattern: Optional[str] = Field(default=None, description="e.g., Check-Then-Act, Lost Update")
    mitigation_suggestion: Optional[str] = None


class OpPairKey(BaseModel):
    """Unique key for operation pair deduplication."""
    entity: str
    ep1_class: str
    ep1_method: str
    ep2_class: str
    ep2_method: str
    ep1_http_verb: str
    ep2_http_verb: str
    service1: str = ""
    service2: str = ""

    def to_tuple(self):
        return (self.entity, self.ep1_class, self.ep1_method,
                self.ep2_class, self.ep2_method)

    def display_name(self):
        return f"{self.entity}: {self.ep1_class}.{self.ep1_method} × {self.ep2_class}.{self.ep2_method}"
