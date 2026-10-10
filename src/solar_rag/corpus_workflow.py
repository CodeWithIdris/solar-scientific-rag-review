from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .corpus import normalize_doi, normalize_title, stable_document_id

SCREENING_STATUS_VALUES = {
    "not_assessed",
    "include_core",
    "include_context",
    "potentially_relevant",
    "exclude",
}

OVERLAP_LEVEL_VALUES = {"none", "low", "moderate", "high", "critical"}
CONFIDENCE_VALUES = {"low", "medium", "high"}
PEER_REVIEW_STATUS_VALUES = {
    "not_checked",
    "peer_reviewed",
    "not_peer_reviewed",
    "unclear",
}
FULL_TEXT_STATUS_VALUES = {
    "not_checked",
    "not_found",
    "open_access",
    "subscriber_only",
    "partial_text",
    "extracted",
    "not_applicable",
}
EXTRACTION_STATUS_VALUES = {
    "not_started",
    "successful",
    "partial",
    "failed",
    "not_required",
}
RETRACTION_STATUS_VALUES = {
    "not_checked",
    "not_retracted",
    "retracted",
    "correction_pending",
    "corrected",
    "review_required",
}
LICENSE_STATUS_VALUES = {
    "not_recorded",
    "cc_by",
    "cc_by_sa",
    "other",
    "rights_unclear",
    "no_license_info",
}
RELEVANCE_DECISION_VALUES = {
    "not_assessed",
    "include_core",
    "include_context",
    "potentially_relevant",
    "exclude",
}


@dataclass(frozen=True, slots=True)
class CorpusCandidate:
    record_id: str
    title: str
    source_name: str
    search_query: str
    search_date: str
    source_url: str | None = None
    doi: str | None = None
    publication_year: int | None = None
    screening_status: str = "not_assessed"
    overlap_level: str = "none"
    relevance_decision: str = "potentially_relevant"
    confidence: str = "low"
    peer_review_status: str = "not_checked"
    full_text_status: str = "not_checked"
    extraction_status: str = "not_started"
    extraction_note: str | None = None
    retraction_status: str = "not_checked"
    correction_status: str = "not_checked"
    license_status: str = "not_recorded"
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_doi(self) -> str | None:
        return normalize_doi(self.doi) or None if self.doi else None

    def normalized_title(self) -> str:
        return normalize_title(self.title)


def _as_candidate(value: CorpusCandidate | Mapping[str, Any]) -> CorpusCandidate:
    if isinstance(value, CorpusCandidate):
        return value
    if not isinstance(value, Mapping):
        raise TypeError("Candidate must be a CorpusCandidate or mapping.")
    required = {
        "record_id",
        "title",
        "source_name",
        "search_query",
        "search_date",
    }
    missing = sorted(required.difference(value))
    if missing:
        raise ValueError(f"Candidate missing required fields: {', '.join(missing)}")
    return CorpusCandidate(
        record_id=str(value["record_id"]).strip(),
        title=str(value["title"]).strip(),
        source_name=str(value["source_name"]).strip(),
        search_query=str(value["search_query"]).strip(),
        search_date=str(value["search_date"]).strip(),
        source_url=(str(value["source_url"]).strip() if value.get("source_url") else None),
        doi=(str(value["doi"]).strip() if value.get("doi") else None),
        publication_year=_coerce_year(value.get("publication_year")),
        screening_status=str(value.get("screening_status", "not_assessed")).lower(),
        overlap_level=str(value.get("overlap_level", "none")).lower(),
        relevance_decision=str(value.get("relevance_decision", "potentially_relevant")).lower(),
        confidence=str(value.get("confidence", "low")).lower(),
        peer_review_status=str(value.get("peer_review_status", "not_checked")).lower(),
        full_text_status=str(value.get("full_text_status", "not_checked")).lower(),
        extraction_status=str(value.get("extraction_status", "not_started")).lower(),
        extraction_note=(
            str(value["extraction_note"]).strip() if value.get("extraction_note") else None
        ),
        retraction_status=str(value.get("retraction_status", "not_checked")).lower(),
        correction_status=str(value.get("correction_status", "not_checked")).lower(),
        license_status=str(value.get("license_status", "not_recorded")).lower(),
        metadata=dict(value.get("metadata") or {}),
    )


def _coerce_year(value: Any) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        raise ValueError("publication_year must not be a boolean.")
    if isinstance(value, int):
        year = value
    elif isinstance(value, str):
        try:
            year = int(value.strip())
        except ValueError as exc:
            raise ValueError(
                f"publication_year string must be an integer: {value!r}"
            ) from exc
    else:
        raise ValueError("publication_year must be an integer or an integer-like string.")
    if not 1000 <= year <= 2200:
        raise ValueError(f"Invalid publication year: {year}")
    return year


def validate_candidate_metadata(candidate: CorpusCandidate | Mapping[str, Any]) -> CorpusCandidate:
    candidate = _as_candidate(candidate)
    if not candidate.record_id.strip():
        raise ValueError("Candidate record_id is required.")
    if not candidate.title.strip():
        raise ValueError("Candidate title is required.")
    if not candidate.source_name.strip():
        raise ValueError("Candidate source_name is required.")
    if not candidate.search_query.strip():
        raise ValueError("Candidate search_query is required.")
    if not candidate.search_date.strip():
        raise ValueError("Candidate search_date is required.")
    if candidate.screening_status not in SCREENING_STATUS_VALUES:
        raise ValueError(
            f"Invalid screening_status: {candidate.screening_status!r}. "
            f"Allowed values: {sorted(SCREENING_STATUS_VALUES)}."
        )
    if candidate.overlap_level not in OVERLAP_LEVEL_VALUES:
        raise ValueError(
            f"Invalid overlap_level: {candidate.overlap_level!r}. "
            f"Allowed values: {sorted(OVERLAP_LEVEL_VALUES)}."
        )
    if candidate.relevance_decision not in RELEVANCE_DECISION_VALUES:
        raise ValueError(
            f"Invalid relevance_decision: {candidate.relevance_decision!r}. "
            f"Allowed values: {sorted(RELEVANCE_DECISION_VALUES)}."
        )
    if candidate.confidence not in CONFIDENCE_VALUES:
        raise ValueError(
            f"Invalid confidence: {candidate.confidence!r}. "
            f"Allowed values: {sorted(CONFIDENCE_VALUES)}."
        )
    if candidate.peer_review_status not in PEER_REVIEW_STATUS_VALUES:
        raise ValueError(
            f"Invalid peer_review_status: {candidate.peer_review_status!r}. "
            f"Allowed values: {sorted(PEER_REVIEW_STATUS_VALUES)}."
        )
    if candidate.full_text_status not in FULL_TEXT_STATUS_VALUES:
        raise ValueError(
            f"Invalid full_text_status: {candidate.full_text_status!r}. "
            f"Allowed values: {sorted(FULL_TEXT_STATUS_VALUES)}."
        )
    if candidate.license_status not in LICENSE_STATUS_VALUES:
        raise ValueError(
            f"Invalid license_status: {candidate.license_status!r}. "
            f"Allowed values: {sorted(LICENSE_STATUS_VALUES)}."
        )
    if candidate.extraction_status not in EXTRACTION_STATUS_VALUES:
        raise ValueError(
            f"Invalid extraction_status: {candidate.extraction_status!r}. "
            f"Allowed values: {sorted(EXTRACTION_STATUS_VALUES)}."
        )
    if candidate.extraction_status in {"failed", "partial"} and not candidate.extraction_note:
        raise ValueError(
            "Extraction failure or partial extraction requires an extraction_note."
        )
    if candidate.retraction_status not in RETRACTION_STATUS_VALUES:
        raise ValueError(
            f"Invalid retraction_status: {candidate.retraction_status!r}. "
            f"Allowed values: {sorted(RETRACTION_STATUS_VALUES)}."
        )
    if candidate.correction_status not in RETRACTION_STATUS_VALUES:
        raise ValueError(
            f"Invalid correction_status: {candidate.correction_status!r}. "
            f"Allowed values: {sorted(RETRACTION_STATUS_VALUES)}."
        )
    if candidate.source_url:
        if not re.match(r"^https?://", candidate.source_url):
            raise ValueError("source_url must be an absolute http or https URL.")
    if candidate.doi:
        normalized = candidate.normalized_doi()
        if not normalized:
            raise ValueError("DOI value is present but non-normalizable.")
    return candidate


def document_record_id(candidate: CorpusCandidate | Mapping[str, Any]) -> str:
    candidate = validate_candidate_metadata(candidate)
    doi = candidate.normalized_doi()
    title = candidate.normalized_title()
    year = candidate.publication_year
    return stable_document_id(doi=doi, title=title, year=year)


def duplicate_candidate_records(
    candidates: Sequence[CorpusCandidate | Mapping[str, Any]],
) -> list[dict[str, Any]]:
    validated = [validate_candidate_metadata(candidate) for candidate in candidates]
    grouped: dict[tuple[str, str], list[CorpusCandidate]] = defaultdict(list)
    for candidate in validated:
        doi_key = candidate.normalized_doi()
        if doi_key:
            grouped[("doi", doi_key)].append(candidate)
        grouped[("title", candidate.normalized_title())].append(candidate)

    results: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for (kind, key), items in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1])):
        if len(items) <= 1:
            continue
        if (kind, key) in seen:
            continue
        seen.add((kind, key))
        record_ids = tuple(sorted(item.record_id for item in items))
        duplicates = {
            "kind": kind,
            "key": key,
            "record_ids": record_ids,
            "status": "duplicate" if kind == "doi" else "review_required",
            "detail": (
                "Multiple records share the same DOI; review for duplicates or version collisions."
                if kind == "doi"
                else "Multiple records share a normalized title; review for false-positive title collisions."
            ),
        }
        results.append(duplicates)
    return results


def screening_status_is_valid(value: str) -> bool:
    return str(value).lower() in SCREENING_STATUS_VALUES


def extraction_status_is_valid(value: str) -> bool:
    return str(value).lower() in EXTRACTION_STATUS_VALUES


def peer_review_status_is_valid(value: str) -> bool:
    return str(value).lower() in PEER_REVIEW_STATUS_VALUES


def license_status_is_valid(value: str) -> bool:
    return str(value).lower() in LICENSE_STATUS_VALUES


def retraction_flags(candidate: CorpusCandidate | Mapping[str, Any]) -> dict[str, str | None]:
    candidate = validate_candidate_metadata(candidate)
    review_trigger = {"retracted", "correction_pending", "corrected", "review_required"}
    return {
        "retraction_status": candidate.retraction_status,
        "correction_status": candidate.correction_status,
        "review_required": (
            "yes"
            if candidate.retraction_status in review_trigger
            or candidate.correction_status in review_trigger
            else "no"
        ),
    }


def build_corpus_manifest(
    candidates: Sequence[CorpusCandidate | Mapping[str, Any]],
    *,
    corpus_name: str,
    search_query: str,
    search_date: str,
    version: str,
) -> dict[str, Any]:
    validated = [validate_candidate_metadata(candidate) for candidate in candidates]
    by_screening_status = {
        status: sum(1 for candidate in validated if candidate.screening_status == status)
        for status in sorted(SCREENING_STATUS_VALUES)
    }
    by_extraction_status = {
        status: sum(1 for candidate in validated if candidate.extraction_status == status)
        for status in sorted(EXTRACTION_STATUS_VALUES)
    }
    duplicates = duplicate_candidate_records(validated)
    manifest = {
        "corpus_name": corpus_name,
        "version": version,
        "search_query": search_query,
        "search_date": search_date,
        "record_count": len(validated),
        "screening_status_counts": by_screening_status,
        "extraction_status_counts": by_extraction_status,
        "duplicate_candidates": duplicates,
        "inclusion_count": by_screening_status.get("include_core", 0)
        + by_screening_status.get("include_context", 0),
        "open_or_unassessed": by_screening_status.get("not_assessed", 0)
        + by_screening_status.get("potentially_relevant", 0),
        "needs_manual_review": len(duplicates),
        "status": "synthetic_software_manifest",
    }
    body = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    manifest["sha256"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return manifest


def summarize_corpus(
    candidates: Sequence[CorpusCandidate | Mapping[str, Any]],
    *,
    corpus_name: str,
    search_query: str,
    search_date: str,
    version: str,
) -> dict[str, Any]:
    manifest = build_corpus_manifest(
        candidates,
        corpus_name=corpus_name,
        search_query=search_query,
        search_date=search_date,
        version=version,
    )
    return {
        "corpus_name": manifest["corpus_name"],
        "version": manifest["version"],
        "record_count": manifest["record_count"],
        "inclusion_count": manifest["inclusion_count"],
        "open_or_unassessed": manifest["open_or_unassessed"],
        "needs_manual_review": manifest["needs_manual_review"],
        "screening_status_counts": manifest["screening_status_counts"],
        "extraction_status_counts": manifest["extraction_status_counts"],
        "sha256": manifest["sha256"],
    }
