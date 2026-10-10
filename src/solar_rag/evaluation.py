from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .models import (
    AnswerJudgment,
    QuestionRecord,
    RetrievalHit,
    RetrievalMetrics,
)


@dataclass(frozen=True, slots=True)
class MetricImplementationReport:
    name: str
    status: str
    inputs: str
    scoring_behavior: str
    edge_cases: tuple[str, ...]
    determinism: str
    limitations: str


def metric_implementation_statuses() -> dict[str, MetricImplementationReport]:
    """Classify implemented versus deferred metrics without inventing a production evaluator."""
    return {
        "Recall@k": MetricImplementationReport(
            "Recall@k",
            "IMPLEMENTED",
            "QuestionRecord, retrieval hits, k",
            "Covered required evidence groups divided by total required groups up to k; zero when no relevant evidence is returned within cutoff.",
            ("no relevant evidence", "fewer than k hits", "duplicate hits", "question not answerable"),
            "Deterministic for the same hit list and k.",
            "Uses chunk IDs as evidence groups; does not infer missing group relevance or an alternate gold evidence set beyond supplied question metadata.",
        ),
        "MRR": MetricImplementationReport(
            "MRR",
            "IMPLEMENTED",
            "QuestionRecord, retrieval hits, k",
            "Reciprocal of the first retrieved relevant rank within cutoff; zero if first relevant result is beyond cutoff or absent.",
            ("no relevant evidence", "first relevant hit beyond k", "duplicate ranks rejected"),
            "Deterministic for the same hit list and k.",
            "Only defines retrieval rank quality, not downstream answer correctness or evidence attribution.",
        ),
        "nDCG@k": MetricImplementationReport(
            "nDCG@k",
            "PARTIAL",
            "QuestionRecord, retrieval hits, k, optional relevance_grades",
            "Discounted cumulative gain with explicit graded relevance when relevance grades are supplied; status remains not-scored if grades are OPEN.",
            ("graded relevance", "fewer than k hits", "duplicate evidence IDs", "missing relevance grades"),
            "Deterministic for a fixed grade map and rank ordering.",
            "Grade mapping and alternative-evidence grouping remain OPEN; the implementation does not select a production relevance scale.",
        ),
        "answer_correctness": MetricImplementationReport(
            "answer_correctness",
            "SPECIFIED_ONLY",
            "AnswerJudgment records supplied by an evaluator",
            "No implemented code computes correctness; judgments must be recorded externally with explicit rubric/label semantics.",
            ("supported answer", "unsupported answer", "contradictory answer"),
            "Depends on recorded judgments, not a built-in scoring function.",
            "A production correctness rubric and judge calibration remain unresolved; this is not an automated metric in the codebase.",
        ),
        "answer_relevance": MetricImplementationReport(
            "answer_relevance",
            "SPECIFIED_ONLY",
            "AnswerJudgment records supplied by an evaluator",
            "No built-in relevance scorer is implemented.",
            ("relevant answer", "irrelevant answer"),
            "Deterministic only when the judging process records labels.",
            "Relevance labels and judge instructions remain outside the code and are therefore not operationalized here.",
        ),
        "completeness": MetricImplementationReport(
            "completeness",
            "SPECIFIED_ONLY",
            "AnswerJudgment records supplied by an evaluator",
            "A completeness field exists but no study-specific rubric or metric computation is implemented.",
            ("missing required claims", "partially answered question"),
            "Deterministic only after an explicit rubric and labels are defined.",
            "The code validates numeric ranges but does not invent a scoring formula or gold checklist.",
        ),
        "faithfulness": MetricImplementationReport(
            "faithfulness",
            "SPECIFIED_ONLY",
            "AnswerJudgment records supplied by an evaluator",
            "A faithfulness score field exists but no operational faithfulness evaluator is implemented.",
            ("supported", "unsupported", "hallucinated"),
            "Deterministic only when a faithful judge is specified.",
            "No provider model, calibration corpus, or evidence abstraction method was selected.",
        ),
        "claim-level evidence attribution": MetricImplementationReport(
            "claim-level evidence attribution",
            "IMPLEMENTED",
            "AnswerJudgment and ClaimJudgment objects with cited evidence IDs",
            "Counts cited claim-evidence pairs and valid support status coverage against required claims.",
            ("supported claims", "partially supported claims", "unsupported claims", "incorrect attribution"),
            "Deterministic for a fixed set of judgments and evidence IDs.",
            "It is a structural metric for attributes already annotated; it does not supply the ground-truth claim set or human judgments on its own.",
        ),
        "citation/evidence precision": MetricImplementationReport(
            "citation/evidence precision",
            "IMPLEMENTED",
            "AnswerJudgment claims and cited evidence IDs",
            "Valid claim-evidence pairs divided by all cited claim-evidence pairs; returns None when there are no citations.",
            ("empty citation set", "unsupported claim", "incorrect attribution"),
            "Deterministic for the same annotations and evidence set.",
            "The code does not define the gold citation set or judge the citation quality of a generator response automatically.",
        ),
        "citation/evidence completeness": MetricImplementationReport(
            "citation/evidence completeness",
            "IMPLEMENTED",
            "AnswerJudgment claims, required claim IDs, available evidence IDs",
            "Coverage of required supportable claims by correctly attributed evidence; returns None when required claims are absent.",
            ("required claims present", "no required claims", "missing evidence"),
            "Deterministic when required claims and evidence are fixed.",
            "It measures annotation- and requirement-defined coverage, not a production citation recall metric from an unseen benchmark.",
        ),
        "abstention": MetricImplementationReport(
            "abstention",
            "IMPLEMENTED",
            "AnswerJudgment plus answerability status",
            "Classifies appropriate vs inappropriate abstention, unsupported answers, hallucinated answers, and contradictory answers.",
            ("answerable question", "unsupported question", "malformed answer"),
            "Deterministic for the same judgment and answerability state.",
            "It validates a predefined label set and does not choose a production abstention policy or calibration rule.",
        ),
        "latency": MetricImplementationReport(
            "latency",
            "PARTIAL",
            "TimingCollector stage measurements",
            "Records elapsed milliseconds for retrieval, context assembly, generation, and total pipeline stages.",
            ("missing stage", "successful timing", "timing summary"),
            "Deterministic for the same environment and cooled caches, but environment dependent.",
            "No approved latency protocol, warm-up procedure, hardware logging, or cost model is selected.",
        ),
        "resource/cost": MetricImplementationReport(
            "resource/cost",
            "DEFERRED",
            "No implemented resource/cost reporting fields beyond run manifest metadata",
            "No cost model or measured token/provider compute accounting is implemented.",
            ("no selected provider", "no cost accounting"),
            "Not established in code.",
            "The production provider, token accounting, and cost normalization remain unresolved scientific and operational decisions.",
        ),
    }


class EvaluationError(ValueError):
    """Raised when the metric is not defined by the available annotations."""


VALID_SUPPORT = {"supported", "partially_supported", "unsupported", "incorrectly_attributed"}
VALID_ABSTENTION = {
    "appropriate_abstention",
    "unsupported_answer",
    "hallucinated_answer",
    "contradictory_answer",
    "inappropriate_abstention",
    "answered_supported",
    "malformed_or_empty",
}


def retrieval_metrics(
    question: QuestionRecord,
    hits: Sequence[RetrievalHit],
    *,
    k: int,
    relevance_grades: Mapping[str, float] | None = None,
) -> RetrievalMetrics:
    if k <= 0:
        raise EvaluationError("Metric cutoff k must be explicitly positive.")
    if question.answerability != "answerable_from_corpus":
        return RetrievalMetrics(None, None, None, "not_applicable_unanswerable")
    groups = question.required_evidence_groups
    if not groups:
        raise EvaluationError("Answerable question has no gold evidence groups.")
    ordered_hits = sorted(hits, key=lambda hit: (hit.rank, hit.chunk_id))
    seen_ranks: set[int] = set()
    ranked_ids: list[tuple[int, str]] = []
    seen: set[str] = set()
    for hit in ordered_hits:
        if (
            isinstance(hit.rank, bool)
            or not isinstance(hit.rank, int)
            or hit.rank <= 0
        ):
            raise EvaluationError("Retrieved ranks must be positive integers.")
        if hit.rank in seen_ranks:
            raise EvaluationError("Retrieved ranks must be unique within a query.")
        seen_ranks.add(hit.rank)
        if not hit.chunk_id or not hit.document_id or not math.isfinite(hit.score):
            raise EvaluationError("Retrieved hits must have valid IDs and finite scores.")
        if hit.chunk_id not in seen:
            ranked_ids.append((hit.rank, hit.chunk_id))
            seen.add(hit.chunk_id)
    top = [(rank, chunk_id) for rank, chunk_id in ranked_ids if rank <= k]
    covered_groups = sum(
        any(chunk_id in group for _, chunk_id in top) for group in groups
    )
    recall = covered_groups / len(groups)
    relevant_ids = set().union(*groups)
    reciprocal_rank = next(
        (1.0 / rank for rank, chunk_id in top
         if chunk_id in relevant_ids),
        0.0,
    )
    ndcg: float | None = None
    status = "scored; ndcg_not_scored_relevance_grades_open"
    if relevance_grades is not None:
        grades = dict(relevance_grades)
        if any(not math.isfinite(value) or value < 0 for value in grades.values()):
            raise EvaluationError("Relevance grades must be finite and non-negative.")
        dcg = sum(
            (2.0 ** grades.get(chunk_id, 0.0) - 1.0) / math.log2(rank + 1)
            for rank, chunk_id in top
        )
        ideal_grades = sorted(
            (grade for grade in grades.values() if grade > 0), reverse=True
        )[:k]
        idcg = sum(
            (2.0 ** grade - 1.0) / math.log2(rank + 1)
            for rank, grade in enumerate(ideal_grades, start=1)
        )
        ndcg = dcg / idcg if idcg > 0 else None
        status = "scored"
    return RetrievalMetrics(recall, reciprocal_rank, ndcg, status)


def attribution_metrics(
    judgments: Sequence[AnswerJudgment],
    *,
    required_claim_ids: Sequence[str],
    available_evidence_ids: set[str],
    partial_support_policy: str,
) -> dict[str, object]:
    if partial_support_policy not in {"credit", "no_credit"}:
        raise EvaluationError(
            "partial_support_policy must be explicitly 'credit' or 'no_credit'; "
            "the scientific scoring choice remains OPEN."
        )
    for judgment in judgments:
        for claim in judgment.claims:
            if claim.support_status not in VALID_SUPPORT:
                raise EvaluationError(
                    f"Unknown support status {claim.support_status!r}."
                )
    cited_pairs = 0
    valid_pairs = 0
    supported_required: set[str] = set()
    status_counts = {status: 0 for status in VALID_SUPPORT}
    for judgment in judgments:
        for claim in judgment.claims:
            status_counts[claim.support_status] += 1
            valid_citations = (
                set(claim.valid_supporting_evidence_ids)
                .intersection(available_evidence_ids)
            )
            cited = set(claim.cited_evidence_ids)
            cited_pairs += len(cited)
            if claim.support_status == "supported" or (
                claim.support_status == "partially_supported"
                and partial_support_policy == "credit"
            ):
                valid_pairs += len(cited.intersection(valid_citations))
            if (
                claim.support_status == "supported"
                or (
                    claim.support_status == "partially_supported"
                    and partial_support_policy == "credit"
                )
            ) and cited.intersection(valid_citations):
                supported_required.add(claim.claim_id)
    required = set(required_claim_ids)
    precision = valid_pairs / cited_pairs if cited_pairs else None
    completeness = (
        len(required.intersection(supported_required)) / len(required)
        if required
        else None
    )
    return {
        "citation_precision": precision,
        "citation_completeness": completeness,
        "cited_claim_evidence_pairs": cited_pairs,
        "valid_claim_evidence_pairs": valid_pairs,
        "required_claim_count": len(required),
        "correctly_attributed_required_claim_count": len(
            required.intersection(supported_required)
        ),
        "claim_support_status_counts": status_counts,
        "partial_support_policy": partial_support_policy,
    }


def abstention_outcome(
    judgment: AnswerJudgment, *, answerability: str
) -> dict[str, bool | str]:
    status = judgment.abstention_status
    if status not in VALID_ABSTENTION:
        raise EvaluationError(f"Unknown abstention status {status!r}.")
    valid_answerability = {
        "answerable_from_corpus",
        "unsupported_by_corpus",
        "insufficient_or_indeterminate",
    }
    if answerability not in valid_answerability:
        raise EvaluationError(
            f"Answerability {answerability!r} is not scoreable."
        )
    is_unanswerable = answerability in {
        "unsupported_by_corpus",
        "insufficient_or_indeterminate",
    }
    is_any_abstention = status in {
        "appropriate_abstention",
        "inappropriate_abstention",
    }
    return {
        "status": status,
        "correct_abstention": is_unanswerable
        and status == "appropriate_abstention",
        "unsupported_answer": status == "unsupported_answer",
        "hallucinated_answer": status == "hallucinated_answer",
        "contradictory_answer": status == "contradictory_answer",
        "inappropriate_abstention": not is_unanswerable and is_any_abstention,
    }


def validate_answer_judgment(judgment: AnswerJudgment) -> None:
    if not judgment.question_id or judgment.condition not in {
        "bm25", "dense", "hybrid"
    }:
        raise EvaluationError("Judgment requires a question ID and primary arm.")
    if judgment.abstention_status not in VALID_ABSTENTION:
        raise EvaluationError(
            f"Unknown abstention status {judgment.abstention_status!r}."
        )
    for value in (judgment.completeness, judgment.faithfulness):
        if value is not None and (not math.isfinite(value) or not 0 <= value <= 1):
            raise EvaluationError("Completeness/faithfulness scores must be in [0, 1].")


def macro_question_mean(
    question_scores: Mapping[str, float | None],
) -> float | None:
    """Average one score per question; missing scores are excluded, not imputed."""
    valid = [score for score in question_scores.values() if score is not None]
    if not valid:
        return None
    if any(not math.isfinite(score) for score in valid):
        raise EvaluationError("Question scores must be finite.")
    return sum(valid) / len(valid)


def paired_question_differences(
    scores_by_condition: Mapping[str, Mapping[str, float | None]],
) -> dict[str, dict[str, object]]:
    """Return matched per-question differences; no inferential test is selected."""
    required = {"bm25", "dense", "hybrid"}
    if set(scores_by_condition) != required:
        raise EvaluationError("Paired scoring requires exactly the three primary arms.")
    question_sets = [set(scores_by_condition[arm]) for arm in required]
    if any(question_set != question_sets[0] for question_set in question_sets[1:]):
        raise EvaluationError("Question IDs differ across retrieval conditions.")
    output: dict[str, dict[str, object]] = {}
    contrasts = (("bm25", "dense"), ("bm25", "hybrid"), ("dense", "hybrid"))
    for left, right in contrasts:
        differences: list[float] = []
        for question_id in sorted(question_sets[0]):
            left_score = scores_by_condition[left][question_id]
            right_score = scores_by_condition[right][question_id]
            if left_score is not None and right_score is not None:
                differences.append(left_score - right_score)
        output[f"{left}_minus_{right}"] = {
            "differences": differences,
            "n_paired_questions": len(differences),
        }
    return output
