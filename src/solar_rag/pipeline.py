from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import asdict
from typing import Any

from .context import assemble_context
from .corpus import document_source_path, sha256_text
from .generation import (
    GenerationRequest,
    Generator,
    PromptArtifact,
    build_request,
)
from .models import Chunk, DocumentRecord, QuestionRecord
from .processing import TextExtractor, iter_chunks
from .retrieval import Retriever


class PipelineError(ValueError):
    """Raised when common run controls or arm interfaces are inconsistent."""


def process_document(
    document: DocumentRecord,
    *,
    corpus_root: str,
    extractor: TextExtractor,
    max_chars: int,
    overlap_chars: int,
) -> tuple[str, str, list[Chunk]]:
    """Extract and chunk one document without discarding failures or provenance."""
    if document.eligibility_status != "eligible":
        raise PipelineError(
            f"Document {document.document_id!r} has not passed explicit corpus screening."
        )
    if document.retraction_status in {"not_checked", "OPEN", ""}:
        raise PipelineError(
            f"Document {document.document_id!r} has unresolved status screening."
        )
    if document.full_text_provenance in {"OPEN", "", "not_recorded"}:
        raise PipelineError(
            f"Document {document.document_id!r} has unresolved full-text provenance."
        )
    text_path = document_source_path(document, corpus_root)
    text, page_spans = extractor.extract(str(text_path))
    chunks = list(
        iter_chunks(
            text,
            document_id=document.document_id,
            version=document.version,
            max_chars=max_chars,
            overlap_chars=overlap_chars,
            page_spans=page_spans,
        )
    )
    return text, sha256_text(text), chunks


def run_arm(
    question: QuestionRecord,
    *,
    retriever: Retriever,
    retrieval_cutoff: int,
    chunks_by_id: dict[str, Chunk],
    context_budget: int,
    count_tokens: Callable[[str], int],
    overflow_policy: str,
    generator: Generator,
    prompt: PromptArtifact,
    generation_parameters: dict[str, object],
) -> dict[str, Any]:
    if retriever.condition not in {"bm25", "dense", "hybrid"}:
        raise PipelineError("Only the three primary retrieval conditions are accepted.")
    hits = retriever.retrieve(question.question, retrieval_cutoff)
    context = assemble_context(
        hits,
        chunks_by_id,
        max_tokens=context_budget,
        count_tokens=count_tokens,
        overflow_policy=overflow_policy,
    )
    request: GenerationRequest = build_request(
        question_id=question.question_id,
        question=question.question,
        context=context.items,
        prompt=prompt,
        generation_parameters=generation_parameters,
    )
    response = generator.generate(request)
    if response.model_id != generator.model_id:
        raise PipelineError(
            "Generator response model identity does not match configured interface."
        )
    unavailable_citations = sorted(
        set(response.cited_evidence_ids)
        .difference(item.evidence_id for item in context.items)
    )
    return {
        "question_id": question.question_id,
        "condition": retriever.condition,
        "status": "invalid_citation" if unavailable_citations else "completed",
        "retrieval_hits": [asdict(hit) for hit in hits],
        "context_evidence_ids": [item.evidence_id for item in context.items],
        "context_token_count": context.token_count,
        "excluded_chunk_ids": list(context.excluded_chunk_ids),
        "prompt_version": prompt.version,
        "prompt_sha256": prompt.sha256,
        "generator_model": response.model_id,
        "generation_parameters": dict(generation_parameters),
        "answer": response.answer,
        "cited_evidence_ids": list(response.cited_evidence_ids),
        "unavailable_cited_evidence_ids": unavailable_citations,
        "raw_response": response.raw_response,
        "finish_reason": response.finish_reason,
    }


def run_matched_question(
    question: QuestionRecord,
    *,
    retrievers: Mapping[str, Retriever],
    retrieval_cutoffs: Mapping[str, int],
    chunks_by_id: dict[str, Chunk],
    context_budget: int,
    count_tokens: Callable[[str], int],
    overflow_policy: str,
    generator: Generator,
    prompt: PromptArtifact,
    generation_parameters: dict[str, object],
) -> list[dict[str, Any]]:
    required = {"bm25", "dense", "hybrid"}
    if set(retrievers) != required or set(retrieval_cutoffs) != required:
        raise PipelineError("Matched run requires exactly BM25, dense, and hybrid.")
    if len(set(retrieval_cutoffs.values())) != 1:
        raise PipelineError(
            "All three arms must use the same final retrieval cutoff."
        )
    if len(set(retrievers.values())) != 3:
        raise PipelineError("Each primary arm must have its own retriever instance.")
    common_chunks = dict(chunks_by_id)
    if any(
        dict(retriever.indexed_chunks) != common_chunks
        for retriever in retrievers.values()
    ):
        raise PipelineError(
            "BM25, dense, hybrid, and context assembly must use identical chunk records."
        )
    rows = []
    for condition in ("bm25", "dense", "hybrid"):
        retriever = retrievers[condition]
        if retriever.condition != condition:
            raise PipelineError(f"Retriever identity mismatch for {condition}.")
        rows.append(
            run_arm(
                question,
                retriever=retriever,
                retrieval_cutoff=retrieval_cutoffs[condition],
                chunks_by_id=chunks_by_id,
                context_budget=context_budget,
                count_tokens=count_tokens,
                overflow_policy=overflow_policy,
                generator=generator,
                prompt=prompt,
                generation_parameters=generation_parameters,
            )
        )
    return rows
