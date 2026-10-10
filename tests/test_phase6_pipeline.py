from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from solar_rag.benchmark import load_benchmark
from solar_rag.config import (
    ConfigurationError,
    canonical_config_hash,
    load_config,
    readiness_statuses,
    require_configured,
    unresolved_decisions,
)
from solar_rag.context import ContextAssemblyError, assemble_context, context_fairness_status
from solar_rag.corpus import (
    CorpusValidationError,
    document_from_mapping,
    load_documents,
    stable_document_id,
    write_jsonl_new,
)
from solar_rag.evaluation import (
    MetricImplementationReport,
    abstention_outcome,
    attribution_metrics,
    metric_implementation_statuses,
    paired_question_differences,
    retrieval_metrics,
)
from solar_rag.generation import (
    GenerationRequest,
    GenerationResult,
    PromptArtifact,
)
from solar_rag.models import (
    AnswerJudgment,
    Chunk,
    ClaimJudgment,
    DocumentRecord,
    FailureRecord,
    QuestionRecord,
    RetrievalHit,
)
from solar_rag.processing import (
    PlainTextExtractor,
    ProcessingError,
    iter_chunks,
    normalize_text,
)
from solar_rag.pipeline import process_document, run_matched_question
from solar_rag.quality import run_leakage_checks, validate_arm_fairness
from solar_rag.results import ResultStoreError, validate_paired_rows
from solar_rag.retrieval import (
    BM25Retriever,
    DenseRetriever,
    HybridRetriever,
    RetrievalError,
    cosine_similarity,
    reciprocal_rank_fusion,
    scientific_tokens,
)
from solar_rag.runlog import TimingCollector, append_failure, create_run_manifest


def make_chunk(chunk_id: str, text: str, document_id: str = "doc-1") -> Chunk:
    return Chunk(chunk_id, document_id, text, 0, len(text))


class ConfigTests(unittest.TestCase):
    def test_example_config_is_valid_but_not_ready(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        self.assertTrue(config["decisions"])
        with self.assertRaises(ConfigurationError):
            require_configured(config, "study execution")
        self.assertEqual(len(canonical_config_hash(config)), 64)

    def test_config_rejects_an_extra_arm(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        config["primary_arms"].append("reranker")
        from solar_rag.config import validate_config

        with self.assertRaises(ConfigurationError):
            validate_config(config)

    def test_config_reports_distinct_readiness_gates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        statuses = readiness_statuses(config)
        self.assertEqual(statuses["configuration_schema_validity"], "PASS")
        self.assertEqual(statuses["software_pipeline_readiness"], "NOT_READY")
        self.assertEqual(statuses["scientific_study_readiness"], "BLOCKED")
        self.assertEqual(statuses["confirmatory_experiment_readiness"], "BLOCKED")

    def test_config_readiness_requires_frozen_shared_controls(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        for decision in config["decisions"].values():
            decision["status"] = "FROZEN"
            decision["value"] = "test-only"
        self.assertTrue(any(
            item.startswith("shared_controls.")
            for item in unresolved_decisions(config)
        ))
        with self.assertRaises(ConfigurationError):
            require_configured(config, "study execution")

    def test_config_rejects_malformed_decision_and_controls(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        del config["decisions"]["bm25_analyzer_and_parameters"]["value"]
        from solar_rag.config import validate_config

        with self.assertRaises(ConfigurationError):
            validate_config(config)
        config = load_config(root / "config" / "experiment.example.json")
        config["shared_controls"] = None
        with self.assertRaises(ConfigurationError):
            validate_config(config)


class IngestionAndProcessingTests(unittest.TestCase):
    def test_stable_document_id_uses_normalized_doi(self) -> None:
        first = stable_document_id(
            doi="https://doi.org/10.1234/TEST", title="A", year=2020
        )
        second = stable_document_id(doi="10.1234/test", title="Other", year=2021)
        self.assertEqual(first, second)

    def test_document_requires_title_and_validates_year(self) -> None:
        with self.assertRaises(CorpusValidationError):
            document_from_mapping({})
        with self.assertRaises(CorpusValidationError):
            document_from_mapping({"title": "Test", "publication_year": "1"})

    def test_duplicate_document_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "documents.jsonl"
            path.write_text(
                '{"document_id":"d","title":"One"}\n'
                '{"document_id":"d","title":"Two"}\n',
                encoding="utf-8",
            )
            with self.assertRaises(CorpusValidationError):
                load_documents(path)

    def test_write_jsonl_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            write_jsonl_new(path, [{"id": "a"}])
            with self.assertRaises(FileExistsError):
                write_jsonl_new(path, [{"id": "b"}])
            self.assertIn('"a"', path.read_text(encoding="utf-8"))

    def test_normalization_preserves_scientific_symbols_and_numbers(self) -> None:
        text = normalize_text("PV\tη = 21.4%;\r\n\n\nSiO₂")
        self.assertIn("η = 21.4%", text)
        self.assertIn("SiO₂", text)
        self.assertNotIn("\n\n\n", text)

    def test_chunking_requires_explicit_parameters_and_stable_ids(self) -> None:
        text = "alpha beta gamma delta epsilon zeta eta theta"
        with self.assertRaises(ProcessingError):
            list(iter_chunks(text, document_id="d", version="v1",
                             max_chars=0, overlap_chars=0))
        first = list(iter_chunks(text, document_id="d", version="v1",
                                 max_chars=15, overlap_chars=2))
        second = list(iter_chunks(text, document_id="d", version="v1",
                                  max_chars=15, overlap_chars=2))
        self.assertGreater(len(first), 1)
        self.assertEqual([item.chunk_id for item in first],
                         [item.chunk_id for item in second])
        self.assertTrue(all(item.provenance["offset_basis"] for item in first))


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.chunks = [
            make_chunk("c1", "perovskite solar cell efficiency"),
            make_chunk("c2", "silicon module degradation"),
            make_chunk("c3", "perovskite cell stability"),
        ]

    def test_bm25_is_deterministic_and_returns_contract(self) -> None:
        retriever = BM25Retriever(
            self.chunks, tokenizer=scientific_tokens, k1=1.2, b=0.75
        )
        first = retriever.retrieve("perovskite efficiency", 2)
        second = retriever.retrieve("perovskite efficiency", 2)
        self.assertEqual(first, second)
        self.assertEqual(first[0].chunk_id, "c1")
        self.assertEqual(first[0].condition, "bm25")

    def test_bm25_rejects_invalid_parameters(self) -> None:
        with self.assertRaises(RetrievalError):
            BM25Retriever(self.chunks, tokenizer=scientific_tokens, k1=0, b=0.5)

    def test_dense_adapter_uses_injected_embedding_and_similarity(self) -> None:
        vectors = {
            "perovskite solar cell efficiency": (1.0, 0.0),
            "silicon module degradation": (0.0, 1.0),
            "perovskite cell stability": (0.8, 0.2),
        }
        dense = DenseRetriever(
            self.chunks,
            embed_documents=lambda texts: [vectors[text] for text in texts],
            embed_query=lambda _: (1.0, 0.0),
            similarity=cosine_similarity,
            model_id="synthetic-test-only",
        )
        hits = dense.retrieve("synthetic query", 2)
        self.assertEqual(hits[0].chunk_id, "c1")
        self.assertEqual(hits[0].condition, "dense")

    def test_dense_requires_explicit_model_identity(self) -> None:
        with self.assertRaises(RetrievalError):
            DenseRetriever(
                self.chunks,
                embed_documents=lambda texts: [(1.0, 0.0) for _ in texts],
                embed_query=lambda _: (1.0, 0.0),
                similarity=cosine_similarity,
                model_id="",
            )

    def test_rrf_merges_duplicates_and_tracks_component_ranks(self) -> None:
        bm25 = [
            RetrievalHit(1, "doc-1", "c1", 4.0, "bm25"),
            RetrievalHit(2, "doc-1", "c2", 2.0, "bm25"),
        ]
        dense = [
            RetrievalHit(1, "doc-1", "c2", 0.9, "dense"),
            RetrievalHit(2, "doc-1", "c3", 0.8, "dense"),
        ]
        fused = reciprocal_rank_fusion(
            bm25, dense, rank_constant=10, weights={"bm25": 1, "dense": 1}, top_k=3
        )
        self.assertEqual(fused[0].chunk_id, "c2")
        self.assertEqual(fused[0].component_ranks, {"bm25": 2, "dense": 1})
        self.assertTrue(all(hit.condition == "hybrid" for hit in fused))


class BenchmarkContextAndEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.question = QuestionRecord(
            "q1",
            "Which evidence supports the result?",
            answerability="answerable_from_corpus",
            split="pilot",
            required_evidence_groups=(frozenset({"c1", "c1-alt"}), frozenset({"c2"})),
            required_claims=("claim-a", "claim-b"),
        )
        self.hits = [
            RetrievalHit(1, "doc-1", "c1-alt", 1.0, "bm25"),
            RetrievalHit(2, "doc-2", "c2", 0.5, "bm25"),
        ]

    def test_load_synthetic_benchmark(self) -> None:
        root = Path(__file__).resolve().parents[1]
        questions = load_benchmark(root / "data" / "pilot" / "synthetic_questions.jsonl")
        self.assertEqual(len(questions), 2)

    def test_synthetic_corpus_to_chunk_to_retrieval_metric(self) -> None:
        root = Path(__file__).resolve().parents[1]
        pilot_root = root / "data" / "pilot"
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
        questions = load_benchmark(pilot_root / "synthetic_questions.jsonl")
        question = questions[0]
        hit = RetrievalHit(1, chunks[0].document_id, chunks[0].chunk_id, 1.0, "bm25")
        scores = retrieval_metrics(question, [hit], k=1)
        self.assertEqual(scores.recall_at_k, 1.0)
        self.assertIsNone(scores.ndcg_at_k)
        self.assertIn("relevance_grades_open", scores.status)

    def test_retrieval_metrics_support_alternative_and_multi_evidence(self) -> None:
        metrics = retrieval_metrics(
            self.question,
            self.hits,
            k=2,
            relevance_grades={"c1-alt": 1.0, "c2": 1.0},
        )
        self.assertEqual(metrics.recall_at_k, 1.0)
        self.assertEqual(metrics.reciprocal_rank, 1.0)
        self.assertEqual(metrics.ndcg_at_k, 1.0)

    def test_metrics_use_reported_ranks_cutoff_and_deduplicate(self) -> None:
        hits = [
            RetrievalHit(1, "doc-1", "irrelevant", 0.9, "bm25"),
            RetrievalHit(2, "doc-1", "c1-alt", 0.8, "bm25"),
            RetrievalHit(3, "doc-1", "c1-alt", 0.7, "bm25"),
            RetrievalHit(4, "doc-2", "c2", 0.6, "bm25"),
        ]
        metrics = retrieval_metrics(
            self.question,
            hits,
            k=3,
            relevance_grades={"c1-alt": 1.0, "c2": 1.0},
        )
        self.assertEqual(metrics.recall_at_k, 0.5)
        self.assertEqual(metrics.reciprocal_rank, 0.5)
        self.assertAlmostEqual(
            metrics.ndcg_at_k,
            (1.0 / 1.584962500721156) / (1.0 + 1.0 / 1.584962500721156),
        )

    def test_metrics_zero_when_no_relevant_item_within_cutoff(self) -> None:
        hits = [RetrievalHit(1, "doc-1", "irrelevant", 0.9, "bm25")]
        metrics = retrieval_metrics(self.question, hits, k=1)
        self.assertEqual(metrics.recall_at_k, 0.0)
        self.assertEqual(metrics.reciprocal_rank, 0.0)

    def test_metrics_reject_duplicate_ranks_and_invalid_scores(self) -> None:
        duplicate_ranks = [
            RetrievalHit(1, "doc-1", "c1", 1.0, "bm25"),
            RetrievalHit(1, "doc-2", "c2", 0.9, "bm25"),
        ]
        with self.assertRaises(ValueError):
            retrieval_metrics(self.question, duplicate_ranks, k=2)
        invalid_score = [RetrievalHit(1, "doc-1", "c1", float("nan"), "bm25")]
        with self.assertRaises(ValueError):
            retrieval_metrics(self.question, invalid_score, k=2)

    def test_relevant_result_beyond_cutoff_has_zero_mrr(self) -> None:
        metrics = retrieval_metrics(
            self.question,
            [RetrievalHit(4, "doc-1", "c1-alt", 0.9, "bm25")],
            k=3,
        )
        self.assertEqual(metrics.recall_at_k, 0.0)
        self.assertEqual(metrics.reciprocal_rank, 0.0)

    def test_unanswerable_retrieval_metrics_are_not_applicable(self) -> None:
        question = QuestionRecord(
            "q2", "Unsupported?", answerability="unsupported_by_corpus", split="pilot"
        )
        self.assertIsNone(retrieval_metrics(question, [], k=2).recall_at_k)

    def test_context_enforces_common_explicit_budget_and_missing_chunk_error(self) -> None:
        chunks = {
            "c1": make_chunk("c1", "a b"),
            "c2": make_chunk("c2", "c d", "doc-2"),
            "c1-alt": make_chunk("c1-alt", "e f"),
        }
        context = assemble_context(
            self.hits,
            chunks,
            max_tokens=2,
            count_tokens=lambda text: len(text.split()),
            overflow_policy="skip",
        )
        self.assertEqual(context.token_count, 2)
        self.assertEqual(len(context.items), 1)
        self.assertEqual(context.requested_max_tokens, 2)
        self.assertEqual(context.fairness_status, "BLOCKED")
        self.assertEqual(
            context_fairness_status(
                requested_max_tokens=2,
                actual_token_count=2,
                tokenizer_name="production_tokenizer",
            ),
            "READY",
        )
        self.assertEqual(
            context_fairness_status(
                requested_max_tokens=2,
                actual_token_count=2,
                tokenizer_name="<lambda>",
            ),
            "BLOCKED",
        )
        with self.assertRaises(ContextAssemblyError):
            assemble_context(
                self.hits, {"c1": chunks["c1"]}, max_tokens=5,
                count_tokens=lambda text: len(text.split()),
                overflow_policy="skip",
            )

    def test_metric_implementation_statuses_are_explicit_and_not_fake(self) -> None:
        reports = metric_implementation_statuses()
        self.assertIsInstance(reports["Recall@k"], MetricImplementationReport)
        self.assertEqual(reports["MRR"].status, "IMPLEMENTED")
        self.assertEqual(reports["resource/cost"].status, "DEFERRED")
        self.assertIn("answer_correctness", reports)

    def test_attribution_precision_and_completeness(self) -> None:
        judgments = [
            AnswerJudgment(
                "q1",
                "bm25",
                "correct",
                "relevant",
                1.0,
                1.0,
                "answered_supported",
                (
                    ClaimJudgment("claim-a", "Claim A", "supported", ("e1",), ("e1",)),
                    ClaimJudgment("claim-b", "Claim B", "unsupported", ("e2",), ()),
                ),
            )
        ]
        metrics = attribution_metrics(
            judgments,
            required_claim_ids=("claim-a", "claim-b"),
            available_evidence_ids={"e1", "e2"},
            partial_support_policy="no_credit",
        )
        self.assertEqual(metrics["citation_precision"], 0.5)
        self.assertEqual(metrics["citation_completeness"], 0.5)

    def test_attribution_rejects_citations_not_in_supplied_context(self) -> None:
        judgment = AnswerJudgment(
            "q1", "bm25", "correct", "relevant", 1.0, 1.0,
            "answered_supported",
            (ClaimJudgment("claim-a", "Claim A", "supported", ("e1",), ("e1",)),),
        )
        metrics = attribution_metrics(
            [judgment],
            required_claim_ids=("claim-a",),
            available_evidence_ids=set(),
            partial_support_policy="no_credit",
        )
        self.assertEqual(metrics["citation_precision"], 0.0)
        self.assertEqual(metrics["citation_completeness"], 0.0)

    def test_matched_pipeline_uses_one_generator_contract_for_three_arms(self) -> None:
        chunks = [
            make_chunk("c1", "module efficiency condition A"),
            make_chunk("c2", "module efficiency condition B", "doc-2"),
        ]
        chunk_map = {chunk.chunk_id: chunk for chunk in chunks}
        dense_vectors = {
            "module efficiency condition A": (1.0, 0.0),
            "module efficiency condition B": (0.0, 1.0),
        }
        bm25 = BM25Retriever(chunks, tokenizer=scientific_tokens, k1=1.2, b=0.75)
        dense = DenseRetriever(
            chunks,
            embed_documents=lambda texts: [dense_vectors[text] for text in texts],
            embed_query=lambda _: (1.0, 0.0),
            similarity=cosine_similarity,
            model_id="synthetic-test-only",
        )
        hybrid = HybridRetriever(
            bm25,
            dense,
            rank_constant=10,
            weights={"bm25": 1, "dense": 1},
            bm25_candidate_depth=2,
            dense_candidate_depth=2,
        )

        class FakeGenerator:
            model_id = "synthetic-generator-test-only"

            def generate(self, request: GenerationRequest) -> GenerationResult:
                return GenerationResult(
                    "Synthetic response",
                    tuple(item.evidence_id for item in request.context[:1]),
                    self.model_id,
                    "synthetic raw output",
                )

        question = QuestionRecord(
            "q1", "module efficiency condition A",
            answerability="answerable_from_corpus",
            split="pilot",
            required_evidence_groups=(frozenset({"c1"}),),
        )
        rows = run_matched_question(
            question,
            retrievers={"bm25": bm25, "dense": dense, "hybrid": hybrid},
            retrieval_cutoffs={"bm25": 2, "dense": 2, "hybrid": 2},
            chunks_by_id=chunk_map,
            context_budget=20,
            count_tokens=lambda text: len(text.split()),
            overflow_policy="skip",
            generator=FakeGenerator(),
            prompt=PromptArtifact("synthetic-v1", "fixture", "hash", "Synthetic only."),
            generation_parameters={"temperature": 0},
        )
        self.assertEqual([row["condition"] for row in rows], ["bm25", "dense", "hybrid"])
        self.assertEqual({row["generator_model"] for row in rows},
                         {"synthetic-generator-test-only"})
        self.assertEqual({row["prompt_version"] for row in rows}, {"synthetic-v1"})
        self.assertTrue(all(row["status"] == "completed" for row in rows))

    def test_matched_pipeline_rejects_different_cutoffs_and_chunk_sets(self) -> None:
        chunks = [
            make_chunk("c1", "module efficiency condition A"),
            make_chunk("c2", "module efficiency condition B", "doc-2"),
        ]
        vectors = {
            "module efficiency condition A": (1.0, 0.0),
            "module efficiency condition B": (0.0, 1.0),
        }
        bm25 = BM25Retriever(chunks, tokenizer=scientific_tokens, k1=1.2, b=0.75)
        dense = DenseRetriever(
            chunks,
            embed_documents=lambda texts: [vectors[text] for text in texts],
            embed_query=lambda _: (1.0, 0.0),
            similarity=cosine_similarity,
            model_id="synthetic-generator-test-only",
        )
        hybrid = HybridRetriever(
            bm25, dense, rank_constant=10, weights={"bm25": 1, "dense": 1},
            bm25_candidate_depth=2, dense_candidate_depth=2,
        )

        class GeneratorStub:
            model_id = "synthetic-generator-test-only"

            def generate(self, request: GenerationRequest) -> GenerationResult:
                return GenerationResult("answer", (), self.model_id, "raw")

        shared = {
            "question": QuestionRecord(
                "q1", "module efficiency", answerability="answerable_from_corpus",
                split="pilot", required_evidence_groups=(frozenset({"c1"}),),
            ),
            "retrievers": {"bm25": bm25, "dense": dense, "hybrid": hybrid},
            "chunks_by_id": {chunk.chunk_id: chunk for chunk in chunks},
            "context_budget": 20,
            "count_tokens": lambda text: len(text.split()),
            "overflow_policy": "skip",
            "generator": GeneratorStub(),
            "prompt": PromptArtifact("v1", "fixture", "hash", "prompt"),
            "generation_parameters": {"temperature": 0},
        }
        with self.assertRaises(ValueError):
            run_matched_question(
                **shared, retrieval_cutoffs={"bm25": 1, "dense": 2, "hybrid": 2}
            )
        with self.assertRaises(ValueError):
            run_matched_question(
                **{**shared, "chunks_by_id": {"c1": chunks[0]}},
                retrieval_cutoffs={"bm25": 2, "dense": 2, "hybrid": 2},
            )
        altered_chunks = [
            make_chunk("c1", "changed content with same identifier"),
            chunks[1],
        ]
        altered_dense = DenseRetriever(
            altered_chunks,
            embed_documents=lambda texts: [(1.0, 0.0) for _ in texts],
            embed_query=lambda _: (1.0, 0.0),
            similarity=cosine_similarity,
            model_id="synthetic-generator-test-only",
        )
        altered_bm25 = BM25Retriever(
            altered_chunks, tokenizer=scientific_tokens, k1=1.2, b=0.75
        )
        altered_hybrid = HybridRetriever(
            altered_bm25, altered_dense, rank_constant=10,
            weights={"bm25": 1, "dense": 1},
            bm25_candidate_depth=2, dense_candidate_depth=2,
        )
        with self.assertRaises(ValueError):
            run_matched_question(
                **{
                    **shared,
                    "retrievers": {
                        "bm25": altered_bm25, "dense": altered_dense,
                        "hybrid": altered_hybrid,
                    },
                },
                retrieval_cutoffs={"bm25": 2, "dense": 2, "hybrid": 2},
            )

    def test_paired_question_differences_keep_matching_by_question(self) -> None:
        results = paired_question_differences({
            "bm25": {"q1": 1.0, "q2": 0.0},
            "dense": {"q1": 0.0, "q2": 0.0},
            "hybrid": {"q1": 1.0, "q2": None},
        })
        self.assertEqual(results["bm25_minus_dense"]["differences"], [1.0, 0.0])
        self.assertEqual(results["bm25_minus_hybrid"]["n_paired_questions"], 1)

    def test_abstention_categories_remain_distinct(self) -> None:
        base = ("q2", "bm25", "incorrect", "relevant", None, None)
        expected = {
            "appropriate_abstention": True,
            "unsupported_answer": False,
            "hallucinated_answer": False,
            "contradictory_answer": False,
        }
        for status, correct in expected.items():
            judgment = AnswerJudgment(*base, status)
            result = abstention_outcome(
                judgment, answerability="unsupported_by_corpus"
            )
            self.assertEqual(result["correct_abstention"], correct)

    def test_answerable_question_abstention_is_inappropriate(self) -> None:
        judgment = AnswerJudgment(
            "q1", "bm25", "incorrect", "relevant", None, None,
            "appropriate_abstention",
        )
        result = abstention_outcome(
            judgment, answerability="answerable_from_corpus"
        )
        self.assertTrue(result["inappropriate_abstention"])
        with self.assertRaises(ValueError):
            abstention_outcome(judgment, answerability="OPEN")


class QualityAndReproducibilityTests(unittest.TestCase):
    def test_fairness_accepts_identical_shared_control_manifests(self) -> None:
        fields = {
            "corpus_version": "c1",
            "document_ids_sha256": "docs",
            "preprocessing_version": "p1",
            "chunking_version": "ch1",
            "chunk_ids_sha256": "chunks",
            "question_ids_sha256": "questions",
            "evidence_annotations_version": "e1",
            "retrieval_evaluation_version": "r1",
            "context_budget": 100,
            "context_assembly_version": "a1",
            "generator_model": "same",
            "prompt_version": "v1",
            "generation_parameters": {"temperature": 0},
            "decoding_settings": {"seed": 1},
            "answer_evaluation_version": "ev1",
        }
        arms = {name: dict(fields) for name in ("bm25", "dense", "hybrid")}
        self.assertEqual(validate_arm_fairness(arms), [])

    def test_fairness_detects_a_context_budget_difference(self) -> None:
        fields = {
            "corpus_version": "c1",
            "document_ids_sha256": "docs",
            "preprocessing_version": "p1",
            "chunking_version": "ch1",
            "chunk_ids_sha256": "chunks",
            "question_ids_sha256": "questions",
            "evidence_annotations_version": "e1",
            "retrieval_evaluation_version": "r1",
            "context_budget": 100,
            "context_assembly_version": "a1",
            "generator_model": "same",
            "prompt_version": "v1",
            "generation_parameters": {"temperature": 0},
            "decoding_settings": {"seed": 1},
            "answer_evaluation_version": "ev1",
        }
        arms = {name: dict(fields) for name in ("bm25", "dense", "hybrid")}
        arms["dense"]["context_budget"] = 99
        findings = validate_arm_fairness(arms)
        self.assertTrue(any(item.check == "fairness:context_budget" for item in findings))

    def test_leakage_checks_report_exact_question_contamination_and_open_cutoff(self) -> None:
        question = QuestionRecord(
            "q1", "What is condition A?", split="development",
            answerability="unsupported_by_corpus",
        )
        findings = run_leakage_checks(
            documents=[DocumentRecord("d1", "Synthetic", publication_year=2026)],
            chunks=[make_chunk("c1", "same text"), make_chunk("c2", "same text")],
            questions=[question],
            full_text_by_document={"d1": "The paper asks: What is condition A?"},
            publication_cutoff=None,
        )
        checks = {item.check for item in findings}
        self.assertIn("question_in_source_text", checks)
        self.assertIn("duplicate_chunk_text", checks)
        self.assertIn("post_publication_material", checks)

    def test_paired_rows_require_exactly_three_primary_conditions(self) -> None:
        rows = []
        for condition in ("bm25", "dense", "hybrid"):
            rows.append({
                "run_id": "r1", "question_id": "q1", "condition": condition,
                "status": "completed", "retrieval_hits": [],
                "context_evidence_ids": [], "answer": "", "judgments": {},
            })
        validate_paired_rows(rows)
        with self.assertRaises(ResultStoreError):
            validate_paired_rows(rows[:2])

    def test_failure_log_is_structured_jsonl(self) -> None:
        failure = FailureRecord(
            "r1", "q1", "dense", "retrieval", "timeout",
            "synthetic timeout", "2026-10-08T00:00:00+00:00", True,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "failures.jsonl"
            append_failure(path, failure)
            row = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(row["status"], "timeout")
            self.assertTrue(row["retryable"])

    def test_manifest_records_missing_git_as_null(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        manifest = create_run_manifest(
            run_id="synthetic-run",
            config=config,
            corpus_version="synthetic-v1",
            benchmark_version="synthetic-v1",
            retrieval_condition="bm25",
            prompt_version=None,
            cwd=root,
        )
        self.assertIn("git_commit", manifest)
        self.assertEqual(manifest["reproducibility_status"], "configuration_incomplete")

    def test_manifest_marks_provisional_decision_incomplete(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "experiment.example.json")
        for decision in config["decisions"].values():
            decision["status"] = "FROZEN"
            decision["value"] = "synthetic-test-only"
        config["decisions"]["bm25_analyzer_and_parameters"]["status"] = "PROVISIONAL"
        for key in (
            "corpus_version",
            "preprocessing_version",
            "chunking_version",
            "benchmark_version",
            "generator",
            "prompt_version",
            "evaluation_version",
        ):
            config["shared_controls"][key] = "synthetic-test-only"
        config["shared_controls"]["context_budget"] = 10
        config["shared_controls"]["generation_parameters"] = {"temperature": 0}
        manifest = create_run_manifest(
            run_id="synthetic-provisional",
            config=config,
            corpus_version="synthetic-v1",
            benchmark_version="synthetic-v1",
            retrieval_condition="bm25",
            prompt_version="synthetic-v1",
            cwd=root,
        )
        self.assertEqual(
            manifest["reproducibility_status"], "configuration_incomplete"
        )

    def test_latency_collector_requires_all_stages_for_complete_summary(self) -> None:
        collector = TimingCollector()
        with collector.measure("retrieval"):
            pass
        with self.assertRaises(ValueError):
            collector.summary()
        for stage in ("context_assembly", "generation", "total_pipeline"):
            with collector.measure(stage):
                pass
        result = collector.summary()
        self.assertEqual(set(result), TimingCollector.REQUIRED_STAGES)


if __name__ == "__main__":
    unittest.main()
