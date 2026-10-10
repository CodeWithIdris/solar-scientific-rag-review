from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ResultStoreError(ValueError):
    """Raised when a result row violates append-only paired-run constraints."""


REQUIRED_FIELDS = {
    "run_id",
    "question_id",
    "condition",
    "status",
    "retrieval_hits",
    "context_evidence_ids",
    "answer",
    "judgments",
}
CONDITIONS = {"bm25", "dense", "hybrid"}
RESULT_STATUSES = {
    "completed",
    "retrieval_failure",
    "empty_retrieval",
    "no_relevant_evidence",
    "generator_failure",
    "timeout",
    "malformed_output",
    "invalid_citation",
    "evaluator_failure",
    "infrastructure_error",
    "partial_arm_failure",
    "generation_exception",
}


def validate_result_row(row: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS.difference(row)
    if missing:
        raise ResultStoreError("Missing fields: " + ", ".join(sorted(missing)))
    if not row["run_id"] or not row["question_id"]:
        raise ResultStoreError("run_id and question_id must be non-empty.")
    if row["condition"] not in CONDITIONS:
        raise ResultStoreError("condition must be bm25, dense, or hybrid.")
    if row["status"] not in RESULT_STATUSES:
        raise ResultStoreError("status is not a recognized machine-readable result state.")
    if not isinstance(row["retrieval_hits"], list):
        raise ResultStoreError("retrieval_hits must be an array.")
    if not isinstance(row["context_evidence_ids"], list):
        raise ResultStoreError("context_evidence_ids must be an array.")


def append_result(path: str | Path, row: dict[str, Any]) -> None:
    validate_result_row(row)
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def validate_paired_rows(rows: list[dict[str, Any]]) -> None:
    observed: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        validate_result_row(row)
        key = (row["run_id"], row["question_id"])
        conditions = observed.setdefault(key, set())
        if row["condition"] in conditions:
            raise ResultStoreError(
                f"Duplicate condition {row['condition']} for question {row['question_id']}."
            )
        conditions.add(row["condition"])
    incomplete = {
        key: conditions
        for key, conditions in observed.items()
        if conditions != CONDITIONS
    }
    if incomplete:
        raise ResultStoreError(
            f"Paired results are incomplete for {len(incomplete)} run/question pairs."
        )
