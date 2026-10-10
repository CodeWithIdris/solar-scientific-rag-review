from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    document_id: str
    title: str
    authors: tuple[str, ...] = ()
    publication_year: int | None = None
    doi: str | None = None
    source_url: str | None = None
    document_type: str = "OPEN"
    topics: tuple[str, ...] = ()
    eligibility_status: str = "not_assessed"
    peer_review_status: str = "not_checked"
    full_text_provenance: str = "OPEN"
    extraction_status: str = "not_started"
    version: str = "OPEN"
    retraction_status: str = "not_checked"
    text_path: str | None = None
    text_sha256: str | None = None
    duplicate_of: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    start_char: int
    end_char: int
    section: str | None = None
    page: int | None = None
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class QuestionRecord:
    question_id: str
    question: str
    category: tuple[str, ...] = ()
    answerability: str = "OPEN"
    split: str = "OPEN"
    required_evidence_groups: tuple[frozenset[str], ...] = ()
    reference_answer: str | None = None
    required_claims: tuple[str, ...] = ()
    validation_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RetrievalHit:
    rank: int
    document_id: str
    chunk_id: str
    score: float
    condition: str
    source_metadata: dict[str, Any] = field(default_factory=dict)
    component_ranks: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RetrievalMetrics:
    recall_at_k: float | None
    reciprocal_rank: float | None
    ndcg_at_k: float | None
    status: str


@dataclass(frozen=True, slots=True)
class ClaimJudgment:
    claim_id: str
    text: str
    support_status: str
    cited_evidence_ids: tuple[str, ...] = ()
    valid_supporting_evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AnswerJudgment:
    question_id: str
    condition: str
    correctness: str
    relevance: str
    completeness: float | None
    faithfulness: float | None
    abstention_status: str
    claims: tuple[ClaimJudgment, ...] = ()


@dataclass(frozen=True, slots=True)
class FailureRecord:
    run_id: str
    question_id: str | None
    condition: str | None
    stage: str
    status: str
    message: str
    timestamp_utc: str
    retryable: bool = False
    details: dict[str, Any] = field(default_factory=dict)
