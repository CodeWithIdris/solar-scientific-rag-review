from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Iterator

from .models import DocumentRecord


_ID_NAMESPACE = uuid.UUID("8e754815-f7e1-4cc3-9166-132477fbd5ad")


class CorpusValidationError(ValueError):
    """Raised when a corpus record is incomplete or duplicated."""


def stable_document_id(*, doi: str | None, title: str, year: int | None) -> str:
    normalized_doi = normalize_doi(doi) if doi else ""
    identity = normalized_doi or (
        f"{normalize_title(title)}|{year if year is not None else ''}"
    )
    if not identity.strip("|"):
        raise CorpusValidationError(
            "A stable document ID requires a DOI or title/year identity."
        )
    return "doc-" + uuid.uuid5(_ID_NAMESPACE, identity).hex


def normalize_doi(doi: str) -> str:
    value = doi.strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    value = re.sub(r"^doi:\s*", "", value)
    value = re.sub(r"[?#].*$", "", value)
    value = value.strip().rstrip("/")
    if not value.startswith("10."):
        return ""
    return value


def normalize_title(title: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", title).casefold().split())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def document_from_mapping(data: dict[str, object]) -> DocumentRecord:
    title = str(data.get("title", "")).strip()
    if not title:
        raise CorpusValidationError("Document title is required.")
    doi = str(data["doi"]).strip() if data.get("doi") else None
    year_value = data.get("publication_year")
    if year_value is None or year_value == "":
        year = None
    elif isinstance(year_value, bool):
        raise CorpusValidationError("publication_year must not be a boolean.")
    elif isinstance(year_value, int):
        year = year_value
    elif isinstance(year_value, str):
        try:
            year = int(year_value)
        except ValueError as exc:
            raise CorpusValidationError(
                "publication_year string must contain an integer."
            ) from exc
    else:
        raise CorpusValidationError("publication_year must be an integer or string.")
    document_id = str(data.get("document_id") or "").strip()
    if not document_id:
        document_id = stable_document_id(doi=doi, title=title, year=year)
    if year is not None and not 1000 <= year <= 2200:
        raise CorpusValidationError(f"Invalid publication year: {year}.")
    authors = data.get("authors", [])
    topics = data.get("topics", [])
    if not isinstance(authors, list) or not all(
        isinstance(author, str) for author in authors
    ):
        raise CorpusValidationError("authors must be an array of strings.")
    if not isinstance(topics, list) or not all(
        isinstance(topic, str) for topic in topics
    ):
        raise CorpusValidationError("topics must be an array of strings.")
    known = {
        "document_id", "title", "authors", "publication_year", "doi",
        "source_url", "document_type", "topics", "full_text_provenance",
        "eligibility_status", "peer_review_status",
        "extraction_status", "version", "retraction_status", "text_path",
        "text_sha256", "duplicate_of",
    }
    return DocumentRecord(
        document_id=document_id,
        title=title,
        authors=tuple(authors),
        publication_year=year,
        doi=doi,
        source_url=str(data["source_url"]) if data.get("source_url") else None,
        document_type=str(data.get("document_type", "OPEN")),
        topics=tuple(topics),
        eligibility_status=str(data.get("eligibility_status", "not_assessed")),
        peer_review_status=str(data.get("peer_review_status", "not_checked")),
        full_text_provenance=str(data.get("full_text_provenance", "OPEN")),
        extraction_status=str(data.get("extraction_status", "not_started")),
        version=str(data.get("version", "OPEN")),
        retraction_status=str(data.get("retraction_status", "not_checked")),
        text_path=str(data["text_path"]) if data.get("text_path") else None,
        text_sha256=str(data["text_sha256"]) if data.get("text_sha256") else None,
        duplicate_of=str(data["duplicate_of"]) if data.get("duplicate_of") else None,
        metadata={key: value for key, value in data.items() if key not in known},
    )


def load_jsonl(path: str | Path) -> Iterator[dict[str, object]]:
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise CorpusValidationError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc
            if not isinstance(value, dict):
                raise CorpusValidationError(
                    f"Line {line_number} must contain a JSON object."
                )
            yield value


def load_documents(path: str | Path) -> list[DocumentRecord]:
    records = [document_from_mapping(row) for row in load_jsonl(path)]
    ids = [record.document_id for record in records]
    if len(ids) != len(set(ids)):
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        raise CorpusValidationError(
            "Duplicate document IDs; no records were overwritten: "
            + ", ".join(duplicates)
        )
    return records


def document_source_path(document: DocumentRecord, corpus_root: str | Path) -> Path:
    if not document.text_path:
        raise CorpusValidationError(
            f"Document {document.document_id!r} has no text_path."
        )
    root = Path(corpus_root).resolve()
    text_path = (root / document.text_path).resolve()
    if not text_path.is_relative_to(root):
        raise CorpusValidationError(
            f"Document {document.document_id!r} text_path escapes corpus root."
        )
    if not text_path.is_file():
        raise CorpusValidationError(
            f"Document source does not exist: {document.document_id!r}."
        )
    return text_path


def load_document_text(document: DocumentRecord, corpus_root: str | Path) -> str:
    text_path = document_source_path(document, corpus_root)
    text = text_path.read_text(encoding="utf-8")
    actual_hash = sha256_text(text)
    if document.text_sha256 and document.text_sha256 != actual_hash:
        raise CorpusValidationError(
            f"Text checksum mismatch for {document.document_id!r}."
        )
    return text


def write_jsonl_new(
    path: str | Path,
    records: Iterable[
        DocumentRecord | dict[str, object]
    ],
) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        for record in records:
            value = asdict(record) if isinstance(record, DocumentRecord) else record
            stream.write(
                json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n"
            )
