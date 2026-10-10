from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solar_rag.benchmark import load_benchmark
from solar_rag.corpus import load_documents
from solar_rag.generation import GenerationRequest, GenerationResult, PromptArtifact
from solar_rag.pipeline import process_document, run_matched_question
from solar_rag.processing import PlainTextExtractor
from solar_rag.retrieval import (
    BM25Retriever,
    DenseRetriever,
    HybridRetriever,
    cosine_similarity,
    scientific_tokens,
)


class SyntheticGenerator:
    model_id = "synthetic-generator-test-only"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        evidence_ids = tuple(item.evidence_id for item in request.context[:1])
        answer = (
            "Synthetic fixture response with no scientific interpretation."
            if evidence_ids
            else "Synthetic fixture: the supplied context contains no evidence."
        )
        return GenerationResult(answer, evidence_ids, self.model_id, answer)


def main() -> int:
    pilot_root = ROOT / "data" / "pilot"
    documents = load_documents(pilot_root / "synthetic_documents.jsonl")
    chunks = []
    for document in documents:
        _, _, document_chunks = process_document(
            document,
            corpus_root=str(pilot_root),
            extractor=PlainTextExtractor(),
            max_chars=1000,
            overlap_chars=0,
        )
        chunks.extend(document_chunks)
    if len(chunks) != 2:
        raise RuntimeError("Synthetic fixture expected exactly two chunks.")

    vectors = {
        chunk.chunk_id: (
            (1.0, 0.0) if chunk.document_id == "synthetic-doc-001" else (0.0, 1.0)
        )
        for chunk in chunks
    }
    vector_by_text = {chunk.text: vectors[chunk.chunk_id] for chunk in chunks}
    bm25 = BM25Retriever(chunks, tokenizer=scientific_tokens, k1=1.2, b=0.75)
    dense = DenseRetriever(
        chunks,
        embed_documents=lambda texts: [vector_by_text[text] for text in texts],
        embed_query=lambda query: (
            (1.0, 0.0) if "condition a" in query.casefold() else (0.0, 1.0)
        ),
        similarity=cosine_similarity,
        model_id="synthetic-test-only",
    )
    hybrid = HybridRetriever(
        bm25,
        dense,
        rank_constant=10,
        weights={"bm25": 1.0, "dense": 1.0},
        bm25_candidate_depth=2,
        dense_candidate_depth=2,
    )
    questions = load_benchmark(pilot_root / "synthetic_questions.jsonl")
    prompt = PromptArtifact(
        "synthetic-prompt-v1",
        "fixture-only",
        "fixture-only",
        "Synthetic software test; not a study prompt.",
    )
    run_count = 0
    for question in questions:
        rows = run_matched_question(
            question,
            retrievers={"bm25": bm25, "dense": dense, "hybrid": hybrid},
            retrieval_cutoffs={"bm25": 2, "dense": 2, "hybrid": 2},
            chunks_by_id={chunk.chunk_id: chunk for chunk in chunks},
            context_budget=200,
            count_tokens=lambda value: len(value.split()),
            overflow_policy="skip",
            generator=SyntheticGenerator(),
            prompt=prompt,
            generation_parameters={"temperature": 0},
        )
        if [row["condition"] for row in rows] != ["bm25", "dense", "hybrid"]:
            raise RuntimeError("Synthetic matched-arm execution was incomplete.")
        if len({row["generator_model"] for row in rows}) != 1:
            raise RuntimeError("Synthetic arms did not share one generator.")
        if len({row["prompt_version"] for row in rows}) != 1:
            raise RuntimeError("Synthetic arms did not share one prompt version.")
        run_count += len(rows)

    print(
        json.dumps(
            {
                "status": "synthetic_technical_smoke_test_passed",
                "fixture_type": "synthetic_software_validation_only",
                "documents_processed": len(documents),
                "shared_chunks_created": len(chunks),
                "questions_exercised": len(questions),
                "condition_runs": run_count,
                "scientific_performance_evaluated": False,
                "production_configuration_ready": False,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
