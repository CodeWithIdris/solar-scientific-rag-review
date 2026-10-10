from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .models import Chunk, DocumentRecord, QuestionRecord


@dataclass(frozen=True, slots=True)
class QualityFinding:
    check: str
    status: str
    severity: str
    record_ids: tuple[str, ...]
    detail: str


def validate_arm_fairness(
    arm_manifests: Mapping[str, Mapping[str, object]],
) -> list[QualityFinding]:
    required_arms = {"bm25", "dense", "hybrid"}
    if set(arm_manifests) != required_arms:
        return [
            QualityFinding(
                "arm_set",
                "fail",
                "blocking",
                tuple(sorted(arm_manifests)),
                f"Expected exactly {sorted(required_arms)}.",
            )
        ]
    shared_fields = (
        "corpus_version",
        "document_ids_sha256",
        "preprocessing_version",
        "chunking_version",
        "chunk_ids_sha256",
        "question_ids_sha256",
        "evidence_annotations_version",
        "retrieval_evaluation_version",
        "context_budget",
        "context_assembly_version",
        "generator_model",
        "prompt_version",
        "generation_parameters",
        "decoding_settings",
        "answer_evaluation_version",
    )
    findings: list[QualityFinding] = []
    for field in shared_fields:
        values = {repr(arm_manifests[arm].get(field)) for arm in required_arms}
        if len(values) != 1:
            findings.append(
                QualityFinding(
                    f"fairness:{field}",
                    "fail",
                    "blocking",
                    tuple(sorted(required_arms)),
                    f"Shared control differs across arms: {field}.",
                )
            )
        elif arm_manifests["bm25"].get(field) is None:
            findings.append(
                QualityFinding(
                    f"fairness:{field}",
                    "not_assessed",
                    "blocking",
                    tuple(sorted(required_arms)),
                    f"Shared control {field} is unset.",
                )
            )
    return findings


def run_leakage_checks(
    *,
    documents: Sequence[DocumentRecord],
    chunks: Sequence[Chunk],
    questions: Sequence[QuestionRecord],
    full_text_by_document: Mapping[str, str],
    publication_cutoff: int | None,
) -> list[QualityFinding]:
    findings: list[QualityFinding] = []
    doi_index: dict[str, list[str]] = defaultdict(list)
    title_index: dict[str, list[str]] = defaultdict(list)
    for document in documents:
        if document.doi:
            doi_index[document.doi.casefold().strip()].append(document.document_id)
        title_index[_normalize(document.title)].append(document.document_id)
        text = full_text_by_document.get(document.document_id)
        if text is not None:
            normalized_text = _normalize(text)
            for question in questions:
                normalized_question = _normalize(question.question)
                if normalized_question and normalized_question in normalized_text:
                    findings.append(
                        QualityFinding(
                            "question_in_source_text",
                            "flag",
                            "review",
                            (question.question_id, document.document_id),
                            "Question text occurs verbatim in source text.",
                        )
                    )
                if question.reference_answer:
                    normalized_answer = _normalize(question.reference_answer)
                    if len(normalized_answer) >= 20 and normalized_answer in normalized_text:
                        findings.append(
                            QualityFinding(
                                "reference_answer_in_source_text",
                                "flag",
                                "review",
                                (question.question_id, document.document_id),
                                "Reference answer occurs verbatim in source text.",
                            )
                        )
    for check, index in (("duplicate_doi", doi_index), ("duplicate_title", title_index)):
        for record_ids in index.values():
            if len(record_ids) > 1:
                findings.append(
                    QualityFinding(
                        check,
                        "flag",
                        "review",
                        tuple(sorted(record_ids)),
                        "Potential duplicate documents require version adjudication.",
                    )
                )
    chunk_index: dict[str, list[str]] = defaultdict(list)
    for chunk in chunks:
        chunk_index[_normalize(chunk.text)].append(chunk.chunk_id)
    for chunk_ids in chunk_index.values():
        if len(chunk_ids) > 1:
            findings.append(
                QualityFinding(
                    "duplicate_chunk_text",
                    "flag",
                    "review",
                    tuple(sorted(chunk_ids)),
                    "Exact duplicate chunk text detected.",
                )
            )
    normalized_questions: dict[str, list[QuestionRecord]] = defaultdict(list)
    for question in questions:
        normalized_questions[_normalize(question.question)].append(question)
    for same_questions in normalized_questions.values():
        if len(same_questions) > 1:
            findings.append(
                QualityFinding(
                    "duplicate_question",
                    "fail",
                    "blocking",
                    tuple(sorted(question.question_id for question in same_questions)),
                    "Duplicate normalized benchmark question text.",
                )
            )
        splits = {question.split for question in same_questions}
        if len(splits) > 1:
            findings.append(
                QualityFinding(
                    "development_test_contamination",
                    "fail",
                    "blocking",
                    tuple(sorted(question.question_id for question in same_questions)),
                    "Duplicate question text occurs across splits.",
                )
            )
    if publication_cutoff is None:
        findings.append(
            QualityFinding(
                "post_publication_material",
                "not_assessed",
                "blocking",
                (),
                "Publication cutoff is OPEN; no temporal contamination conclusion can be drawn.",
            )
        )
    else:
        for document in documents:
            if (
                document.publication_year is not None
                and document.publication_year > publication_cutoff
            ):
                findings.append(
                    QualityFinding(
                        "post_publication_material",
                        "flag",
                        "review",
                        (document.document_id,),
                        f"Document year exceeds configured cutoff {publication_cutoff}.",
                    )
                )
    return findings


def _normalize(value: str) -> str:
    return " ".join(re.sub(r"\W+", " ", value.casefold()).split())
