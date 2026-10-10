from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Callable, Iterator

from .models import Chunk


class ProcessingError(ValueError):
    """Raised when a document cannot be processed without losing traceability."""


def normalize_text(text: str) -> str:
    """Apply conservative Unicode/whitespace normalization without NLP rewriting."""
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in normalized.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", normalized).strip()


def stable_chunk_id(document_id: str, version: str, start: int, end: int) -> str:
    identity = f"{document_id}\0{version}\0{start}\0{end}".encode("utf-8")
    return "chk-" + hashlib.sha256(identity).hexdigest()[:24]


def iter_chunks(
    text: str,
    *,
    document_id: str,
    version: str,
    max_chars: int,
    overlap_chars: int,
    page_spans: tuple[tuple[int, int, int], ...] = (),
) -> Iterator[Chunk]:
    if max_chars <= 0:
        raise ProcessingError("max_chars must be explicitly set to a positive value.")
    if overlap_chars < 0 or overlap_chars >= max_chars:
        raise ProcessingError("overlap_chars must satisfy 0 <= overlap < max_chars.")
    source = normalize_text(text)
    if not source:
        raise ProcessingError(f"Document {document_id!r} has no extractable text.")
    start = 0
    while start < len(source):
        hard_end = min(start + max_chars, len(source))
        end = hard_end
        if hard_end < len(source):
            boundary = source.rfind("\n\n", start + 1, hard_end)
            if boundary > start:
                end = boundary
            else:
                boundary = source.rfind(" ", start + 1, hard_end)
                if boundary > start:
                    end = boundary
        segment = source[start:end].strip()
        if segment:
            page = next(
                (
                    page_number
                    for span_start, span_end, page_number in page_spans
                    if span_start < end and span_end > start
                ),
                None,
            )
            yield Chunk(
                chunk_id=stable_chunk_id(document_id, version, start, end),
                document_id=document_id,
                text=segment,
                start_char=start,
                end_char=end,
                page=page,
                provenance={
                    "source_version": version,
                    "offset_basis": "normalized_extracted_text",
                },
            )
        if end >= len(source):
            break
        next_start = max(start + 1, end - overlap_chars)
        while next_start < end and source[next_start].isspace():
            next_start += 1
        start = next_start


class TextExtractor:
    """Extraction adapter contract; concrete PDF adapters require approval/dependency."""

    def extract(self, _path: str) -> tuple[str, tuple[tuple[int, int, int], ...]]:
        raise NotImplementedError(
            f"{type(self).__name__} must implement extraction for {_path!r}."
        )


class PlainTextExtractor(TextExtractor):
    def extract(self, path: str) -> tuple[str, tuple[tuple[int, int, int], ...]]:
        from pathlib import Path

        source = Path(path)
        if source.suffix.casefold() not in {".txt", ".text"}:
            raise ProcessingError(
                f"Unsupported format {source.suffix!r}; PDF extractor/dependency "
                "has not been selected. Record an extraction failure; do not skip."
            )
        return source.read_text(encoding="utf-8"), ()


class PyMuPDFExtractor(TextExtractor):
    """Optional PDF extractor; dependency is intentionally not installed here."""

    def extract(self, path: str) -> tuple[str, tuple[tuple[int, int, int], ...]]:
        from pathlib import Path

        source = Path(path)
        if source.suffix.casefold() != ".pdf":
            raise ProcessingError(f"Expected a PDF file, received {source.suffix!r}.")
        try:
            import pymupdf
        except ImportError as exc:
            raise ProcessingError(
                "PDF extraction is unavailable: select and install an approved "
                "PyMuPDF version before processing the corpus."
            ) from exc
        page_texts: list[str] = []
        spans: list[tuple[int, int, int]] = []
        cursor = 0
        with pymupdf.open(source) as document:
            for page_index in range(document.page_count):
                page_number = page_index + 1
                page = document.load_page(page_index)
                extracted = page.get_text("text")
                if not isinstance(extracted, str):
                    raise ProcessingError(
                        f"PDF page {page_number} did not yield text output."
                    )
                page_text = normalize_text(extracted)
                page_texts.append(page_text)
                start = cursor
                cursor += len(page_text)
                spans.append((start, cursor, page_number))
                if page_number < len(document):
                    page_texts.append("\n\n")
                    cursor += 2
        return "".join(page_texts), tuple(spans)


def extract_with_status(
    extractor: TextExtractor, path: str, on_failure: Callable[[str], None]
) -> tuple[str, tuple[tuple[int, int, int], ...]] | None:
    try:
        return extractor.extract(path)
    except (OSError, UnicodeError, ProcessingError) as exc:
        on_failure(f"{type(exc).__name__}: {exc}")
        return None
