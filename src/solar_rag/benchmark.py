from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

from .corpus import load_jsonl
from .models import QuestionRecord


class BenchmarkValidationError(ValueError):
    """Raised when benchmark rows are incomplete, ambiguous, or duplicated."""


ANSWERABILITY = {
    "answerable_from_corpus",
    "unsupported_by_corpus",
    "insufficient_or_indeterminate",
    "invalid",
}
SPLITS = {"development", "test", "pilot"}


def question_from_mapping(data: dict[str, object]) -> QuestionRecord:
    question_id = str(data.get("question_id", "")).strip()
    text = str(data.get("question", "")).strip()
    if not question_id or not text:
        raise BenchmarkValidationError("question_id and question are required.")
    answerability = str(data.get("answerability", "OPEN"))
    if answerability not in ANSWERABILITY:
        raise BenchmarkValidationError(
            f"Question {question_id}: invalid or unresolved answerability label."
        )
    split = str(data.get("split", "OPEN"))
    if split not in SPLITS:
        raise BenchmarkValidationError(
            f"Question {question_id}: split must be one of {sorted(SPLITS)}."
        )
    categories = data.get("category", [])
    groups = data.get("required_evidence_groups", [])
    claims = data.get("required_claims", [])
    if not isinstance(categories, list) or not all(
        isinstance(item, str) for item in categories
    ):
        raise BenchmarkValidationError("category must be an array of strings.")
    if not isinstance(groups, list) or not all(
        isinstance(group, list)
        and group
        and all(isinstance(item, str) and item for item in group)
        for group in groups
    ):
        raise BenchmarkValidationError(
            "required_evidence_groups must be an array of non-empty string arrays."
        )
    if not isinstance(claims, list) or not all(
        isinstance(item, str) for item in claims
    ):
        raise BenchmarkValidationError("required_claims must be an array of strings.")
    if answerability == "answerable_from_corpus" and not groups:
        raise BenchmarkValidationError(
            f"Question {question_id}: answerable questions require evidence groups."
        )
    if answerability != "answerable_from_corpus" and groups:
        raise BenchmarkValidationError(
            f"Question {question_id}: unanswerable/invalid questions cannot have "
            "required retrieval evidence groups."
        )
    metadata = data.get("validation_metadata", {})
    if not isinstance(metadata, dict):
        raise BenchmarkValidationError("validation_metadata must be an object.")
    return QuestionRecord(
        question_id=question_id,
        question=text,
        category=tuple(categories),
        answerability=answerability,
        split=split,
        required_evidence_groups=tuple(frozenset(group) for group in groups),
        reference_answer=(
            str(data["reference_answer"]) if data.get("reference_answer") else None
        ),
        required_claims=tuple(claims),
        validation_metadata=metadata,
    )


def load_benchmark(path: str | Path) -> list[QuestionRecord]:
    questions = [question_from_mapping(row) for row in load_jsonl(path)]
    ids = [question.question_id for question in questions]
    if len(ids) != len(set(ids)):
        raise BenchmarkValidationError("Duplicate question_id values are not allowed.")
    normalized = [_normalize(question.question) for question in questions]
    if len(normalized) != len(set(normalized)):
        raise BenchmarkValidationError("Duplicate question text is not allowed.")
    return questions


def _normalize(value: str) -> str:
    return " ".join(re.sub(r"\W+", " ", value.casefold()).split())


def iter_split(
    questions: list[QuestionRecord], split: str
) -> Iterator[QuestionRecord]:
    if split not in SPLITS:
        raise BenchmarkValidationError(f"Unknown split: {split}")
    yield from (question for question in questions if question.split == split)
