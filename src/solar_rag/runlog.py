from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

from .config import canonical_config_hash, unresolved_decisions
from .models import FailureRecord


FAILURE_STATUSES = {
    "retrieval_failure",
    "empty_retrieval",
    "no_relevant_evidence",
    "generator_failure",
    "generation_exception",
    "timeout",
    "malformed_output",
    "invalid_citation",
    "evaluator_failure",
    "infrastructure_error",
    "retry_exhaustion",
    "partial_arm_failure",
    "context_assembly_failure",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def current_git_commit(cwd: str | Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def create_run_manifest(
    *,
    run_id: str,
    config: dict[str, Any],
    corpus_version: str | None,
    benchmark_version: str | None,
    retrieval_condition: str | None,
    prompt_version: str | None,
    cwd: str | Path,
    hardware: dict[str, str] | None = None,
    software_versions: dict[str, str] | None = None,
) -> dict[str, Any]:
    if not run_id.strip():
        raise ValueError("run_id must be explicit.")
    return {
        "run_id": run_id,
        "timestamp_utc": utc_now(),
        "git_commit": current_git_commit(cwd),
        "config_sha256": canonical_config_hash(config),
        "corpus_version": corpus_version,
        "benchmark_version": benchmark_version,
        "retrieval_condition": retrieval_condition,
        "embedding_model": config.get("decisions", {})
        .get("dense_model_and_encoding", {})
        .get("value"),
        "generator_model": config.get("shared_controls", {})
        .get("generator"),
        "prompt_version": prompt_version,
        "random_seed": config.get("shared_controls", {}).get("random_seed"),
        "software": {
            "python": sys.version,
            "platform": platform.platform(),
            "solar_rag": "0.1.0",
            "additional_versions": software_versions or {},
        },
        "hardware": hardware,
        "reproducibility_status": (
            "configuration_incomplete"
            if unresolved_decisions(config)
            else "recorded"
        ),
    }


def write_json_new(path: str | Path, value: object) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def build_failure_record(
    *,
    run_id: str,
    question_id: str | None,
    condition: str | None,
    stage: str,
    status: str,
    message: str,
    retryable: bool = False,
    details: dict[str, Any] | None = None,
) -> FailureRecord:
    if status not in FAILURE_STATUSES:
        raise ValueError(f"Unknown machine-readable failure status: {status}")
    if stage not in {
        "ingestion", "extraction", "preprocessing", "retrieval",
        "context_assembly", "generation", "evaluation", "infrastructure",
    }:
        raise ValueError(f"Unknown failure stage: {stage}")
    return FailureRecord(
        run_id=run_id,
        question_id=question_id,
        condition=condition,
        stage=stage,
        status=status,
        message=message,
        timestamp_utc=utc_now(),
        retryable=retryable,
        details=details or {},
    )


def append_failure(path: str | Path, record: FailureRecord) -> None:
    if record.status not in FAILURE_STATUSES:
        raise ValueError(f"Unknown machine-readable failure status: {record.status}")
    if record.stage not in {
        "ingestion", "extraction", "preprocessing", "retrieval",
        "context_assembly", "generation", "evaluation", "infrastructure",
    }:
        raise ValueError(f"Unknown failure stage: {record.stage}")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


class TimingCollector:
    REQUIRED_STAGES = {
        "retrieval",
        "context_assembly",
        "generation",
        "total_pipeline",
    }

    def __init__(self) -> None:
        self._durations: dict[str, list[float]] = {}

    @contextmanager
    def measure(self, stage: str) -> Generator[None, None, None]:
        if stage not in self.REQUIRED_STAGES:
            raise ValueError(f"Unknown latency stage: {stage}")
        started = time.perf_counter_ns()
        try:
            yield
        finally:
            elapsed = (time.perf_counter_ns() - started) / 1_000_000
            self._durations.setdefault(stage, []).append(elapsed)

    def summary(self, *, require_complete: bool = True) -> dict[str, list[float]]:
        missing = self.REQUIRED_STAGES.difference(self._durations)
        if require_complete and missing:
            raise ValueError("Missing timing stages: " + ", ".join(sorted(missing)))
        return {stage: list(values) for stage, values in sorted(self._durations.items())}
