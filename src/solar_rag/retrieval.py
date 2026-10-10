from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Protocol

from .models import Chunk, RetrievalHit


class RetrievalError(ValueError):
    """Raised when retrieval inputs or unresolved settings are invalid."""


class Retriever(Protocol):
    condition: str
    chunk_ids: frozenset[str]
    indexed_chunks: Mapping[str, Chunk]

    def retrieve(self, query: str, top_k: int) -> list[RetrievalHit]: ...


Tokenizer = Callable[[str], Sequence[str]]
Embedder = Callable[[Sequence[str]], Sequence[Sequence[float]]]
Similarity = Callable[[Sequence[float], Sequence[float]], float]


def scientific_tokens(text: str) -> list[str]:
    """A transparent tokenization utility; use requires an explicit design choice."""
    return re.findall(r"[^\W_]+(?:[.+/%-][^\W_]+)*", text.casefold(), flags=re.UNICODE)


class BM25Retriever:
    condition = "bm25"

    def __init__(
        self,
        chunks: Sequence[Chunk],
        *,
        tokenizer: Tokenizer,
        k1: float,
        b: float,
    ) -> None:
        if not chunks:
            raise RetrievalError("BM25 requires a non-empty shared chunk set.")
        if not math.isfinite(k1) or not math.isfinite(b) or k1 <= 0 or not 0 <= b <= 1:
            raise RetrievalError("BM25 requires k1 > 0 and 0 <= b <= 1.")
        chunk_ids = [chunk.chunk_id for chunk in chunks]
        if len(chunk_ids) != len(set(chunk_ids)):
            raise RetrievalError("BM25 chunk IDs must be unique.")
        self._chunks = tuple(chunks)
        self._tokenizer = tokenizer
        self._k1 = k1
        self._b = b
        self._terms = [Counter(tokenizer(chunk.text)) for chunk in chunks]
        self._lengths = [sum(counts.values()) for counts in self._terms]
        self._average_length = sum(self._lengths) / len(self._lengths) or 1.0
        document_frequency: Counter[str] = Counter()
        for counts in self._terms:
            document_frequency.update(counts.keys())
        self._document_frequency = document_frequency

    @property
    def chunk_ids(self) -> frozenset[str]:
        return frozenset(chunk.chunk_id for chunk in self._chunks)

    @property
    def indexed_chunks(self) -> Mapping[str, Chunk]:
        return {chunk.chunk_id: chunk for chunk in self._chunks}

    def retrieve(self, query: str, top_k: int) -> list[RetrievalHit]:
        if top_k < 0:
            raise RetrievalError("top_k must be non-negative.")
        terms = self._tokenizer(query)
        if not terms or top_k == 0:
            return []
        n_docs = len(self._chunks)
        scores: list[tuple[float, Chunk]] = []
        for chunk, frequencies, length in zip(
            self._chunks, self._terms, self._lengths, strict=True
        ):
            score = 0.0
            for term in terms:
                tf = frequencies.get(term, 0)
                if tf == 0:
                    continue
                df = self._document_frequency[term]
                idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
                denominator = tf + self._k1 * (
                    1.0 - self._b + self._b * length / self._average_length
                )
                score += idf * tf * (self._k1 + 1.0) / denominator
            if score > 0:
                if not math.isfinite(score):
                    raise RetrievalError("BM25 produced a non-finite score.")
                scores.append((score, chunk))
        scores.sort(key=lambda item: (-item[0], item[1].chunk_id))
        return [
            RetrievalHit(
                rank=rank,
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                score=score,
                condition=self.condition,
            )
            for rank, (score, chunk) in enumerate(scores[:top_k], start=1)
        ]


class DenseRetriever:
    """Dense retrieval adapter; model, encoding, index and similarity are injected."""

    condition = "dense"

    def __init__(
        self,
        chunks: Sequence[Chunk],
        *,
        embed_documents: Embedder,
        embed_query: Callable[[str], Sequence[float]],
        similarity: Similarity,
        model_id: str,
    ) -> None:
        if not model_id.strip():
            raise RetrievalError("Dense model identity is required; none is selected.")
        if not chunks:
            raise RetrievalError("Dense retrieval requires shared chunks.")
        chunk_ids = [chunk.chunk_id for chunk in chunks]
        if len(chunk_ids) != len(set(chunk_ids)):
            raise RetrievalError("Dense chunk IDs must be unique.")
        vectors = list(embed_documents([chunk.text for chunk in chunks]))
        if len(vectors) != len(chunks):
            raise RetrievalError("Embedding adapter returned a mismatched vector count.")
        if any(not vector for vector in vectors):
            raise RetrievalError("Embedding adapter returned an empty vector.")
        dimensions = {len(vector) for vector in vectors}
        if len(dimensions) != 1:
            raise RetrievalError("Document embedding dimensions do not match.")
        try:
            numeric_vectors = tuple(
                tuple(float(value) for value in vector) for vector in vectors
            )
        except (TypeError, ValueError, OverflowError) as exc:
            raise RetrievalError("Embedding adapter returned a non-numeric vector.") from exc
        if any(
            not math.isfinite(value)
            for vector in numeric_vectors
            for value in vector
        ):
            raise RetrievalError("Embedding adapter returned a non-finite vector.")
        self._chunks = tuple(chunks)
        self._vectors = numeric_vectors
        self._embed_query = embed_query
        self._similarity = similarity
        self.model_id = model_id

    @property
    def chunk_ids(self) -> frozenset[str]:
        return frozenset(chunk.chunk_id for chunk in self._chunks)

    @property
    def indexed_chunks(self) -> Mapping[str, Chunk]:
        return {chunk.chunk_id: chunk for chunk in self._chunks}

    def retrieve(self, query: str, top_k: int) -> list[RetrievalHit]:
        if top_k < 0:
            raise RetrievalError("top_k must be non-negative.")
        if not query.strip() or top_k == 0:
            return []
        try:
            vector = tuple(float(value) for value in self._embed_query(query))
        except (TypeError, ValueError, OverflowError) as exc:
            raise RetrievalError("Query encoder returned a non-numeric vector.") from exc
        if not vector or len(vector) != len(self._vectors[0]):
            raise RetrievalError("Query embedding dimension differs from document vectors.")
        if any(not math.isfinite(value) for value in vector):
            raise RetrievalError("Query encoder returned a non-finite vector.")
        scored = [
            (float(self._similarity(vector, stored)), chunk)
            for chunk, stored in zip(self._chunks, self._vectors, strict=True)
        ]
        if any(not math.isfinite(score) for score, _ in scored):
            raise RetrievalError("Similarity adapter returned a non-finite score.")
        scored.sort(key=lambda item: (-item[0], item[1].chunk_id))
        return [
            RetrievalHit(rank, chunk.document_id, chunk.chunk_id, score, self.condition)
            for rank, (score, chunk) in enumerate(scored[:top_k], start=1)
        ]


class HybridRetriever:
    condition = "hybrid"

    def __init__(
        self,
        bm25: Retriever,
        dense: Retriever,
        *,
        rank_constant: float,
        weights: Mapping[str, float],
        bm25_candidate_depth: int,
        dense_candidate_depth: int,
    ) -> None:
        if bm25.condition != "bm25" or dense.condition != "dense":
            raise RetrievalError("Hybrid requires the primary BM25 and dense retrievers.")
        if dict(bm25.indexed_chunks) != dict(dense.indexed_chunks):
            raise RetrievalError(
                "BM25 and dense components must index identical chunk records."
            )
        if bm25_candidate_depth <= 0 or dense_candidate_depth <= 0:
            raise RetrievalError("Hybrid component depths must be explicitly positive.")
        self._bm25 = bm25
        self._dense = dense
        self._rank_constant = rank_constant
        self._weights = dict(weights)
        self._bm25_depth = bm25_candidate_depth
        self._dense_depth = dense_candidate_depth

    @property
    def chunk_ids(self) -> frozenset[str]:
        return self._bm25.chunk_ids

    @property
    def indexed_chunks(self) -> Mapping[str, Chunk]:
        return self._bm25.indexed_chunks

    def retrieve(self, query: str, top_k: int) -> list[RetrievalHit]:
        bm25_hits = self._bm25.retrieve(query, self._bm25_depth)
        dense_hits = self._dense.retrieve(query, self._dense_depth)
        return reciprocal_rank_fusion(
            bm25_hits,
            dense_hits,
            rank_constant=self._rank_constant,
            weights=self._weights,
            top_k=top_k,
        )


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise RetrievalError("Cosine vectors must have identical dimensions.")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        raise RetrievalError("Cosine similarity is undefined for a zero vector.")
    return sum(a * b for a, b in zip(left, right, strict=True)) / (
        left_norm * right_norm
    )


def reciprocal_rank_fusion(
    bm25_hits: Sequence[RetrievalHit],
    dense_hits: Sequence[RetrievalHit],
    *,
    rank_constant: float,
    weights: Mapping[str, float],
    top_k: int,
) -> list[RetrievalHit]:
    if not math.isfinite(rank_constant) or rank_constant <= 0:
        raise RetrievalError("RRF rank_constant must be explicitly positive.")
    if (
        set(weights) != {"bm25", "dense"}
        or any(not math.isfinite(value) or value < 0 for value in weights.values())
    ):
        raise RetrievalError("RRF requires non-negative weights for bm25 and dense.")
    if not any(weights.values()):
        raise RetrievalError("At least one RRF component weight must be positive.")
    if top_k < 0:
        raise RetrievalError("top_k must be non-negative.")
    scores: dict[str, float] = defaultdict(float)
    docs: dict[str, str] = {}
    ranks: dict[str, dict[str, int]] = defaultdict(dict)
    for method, hits in (("bm25", bm25_hits), ("dense", dense_hits)):
        seen: set[str] = set()
        ordered_hits = sorted(hits, key=lambda hit: (hit.rank, hit.chunk_id))
        observed_ranks: set[int] = set()
        for hit in ordered_hits:
            if (
                isinstance(hit.rank, bool)
                or not isinstance(hit.rank, int)
                or hit.rank <= 0
            ):
                raise RetrievalError(f"{method} ranks must be positive integers.")
            if hit.rank in observed_ranks:
                raise RetrievalError(f"{method} component ranks must be unique.")
            observed_ranks.add(hit.rank)
            if hit.condition != method:
                raise RetrievalError(
                    f"{method} component contains a hit labeled {hit.condition!r}."
                )
            if not hit.chunk_id or not hit.document_id or not math.isfinite(hit.score):
                raise RetrievalError(f"{method} component contains an invalid hit.")
            if hit.chunk_id in seen:
                continue
            seen.add(hit.chunk_id)
            previous_doc = docs.get(hit.chunk_id)
            if previous_doc is not None and previous_doc != hit.document_id:
                raise RetrievalError(
                    f"Chunk {hit.chunk_id!r} maps to conflicting document IDs."
                )
            docs[hit.chunk_id] = hit.document_id
            ranks[hit.chunk_id][method] = hit.rank
            scores[hit.chunk_id] += weights[method] / (rank_constant + hit.rank)
    ordered = sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))
    return [
        RetrievalHit(
            rank=rank,
            document_id=docs[chunk_id],
            chunk_id=chunk_id,
            score=scores[chunk_id],
            condition="hybrid",
            component_ranks=dict(ranks[chunk_id]),
        )
        for rank, chunk_id in enumerate(ordered[:top_k], start=1)
    ]
