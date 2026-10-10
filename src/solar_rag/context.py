from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from .models import Chunk, RetrievalHit


class ContextAssemblyError(ValueError):
    """Raised when context rules are missing or exceed the explicit budget."""


@dataclass(frozen=True, slots=True)
class ContextItem:
    evidence_id: str
    document_id: str
    text: str
    rank: int


@dataclass(frozen=True, slots=True)
class AssembledContext:
    items: tuple[ContextItem, ...]
    token_count: int
    excluded_chunk_ids: tuple[str, ...]
    overflow_policy: str
    requested_max_tokens: int
    fairness_status: str = "BLOCKED"


def context_fairness_status(
    *,
    requested_max_tokens: int,
    actual_token_count: int,
    tokenizer_name: str | None,
) -> str:
    """The project cannot claim token-budget fairness until a production tokenizer is fixed."""
    if requested_max_tokens <= 0:
        raise ContextAssemblyError("Context budget must be explicitly positive.")
    if actual_token_count < 0:
        raise ContextAssemblyError("Actual context token count cannot be negative.")
    if tokenizer_name is None or not tokenizer_name.strip():
        return "BLOCKED"
    normalized = tokenizer_name.strip().lower()
    if normalized in {"lambda", "<lambda>", "anonymous", "unknown"}:
        return "BLOCKED"
    if actual_token_count <= requested_max_tokens:
        return "READY"
    return "BLOCKED"


def assemble_context(
    hits: Sequence[RetrievalHit],
    chunks_by_id: dict[str, Chunk],
    *,
    max_tokens: int,
    count_tokens: Callable[[str], int],
    overflow_policy: str,
    tokenizer_name: str | None = None,
) -> AssembledContext:
    if max_tokens <= 0:
        raise ContextAssemblyError("Context budget must be explicitly positive.")
    if overflow_policy not in {"skip", "error"}:
        raise ContextAssemblyError("overflow_policy must be explicitly 'skip' or 'error'.")
    seen: set[str] = set()
    selected: list[ContextItem] = []
    excluded: list[str] = []
    used = 0
    for hit in sorted(hits, key=lambda item: (item.rank, item.chunk_id)):
        if hit.chunk_id in seen:
            continue
        seen.add(hit.chunk_id)
        chunk = chunks_by_id.get(hit.chunk_id)
        if chunk is None:
            raise ContextAssemblyError(
                f"Retrieved chunk {hit.chunk_id!r} is absent from the shared chunk store."
            )
        if chunk.document_id != hit.document_id:
            raise ContextAssemblyError(
                f"Retrieved document/chunk mismatch for {hit.chunk_id!r}."
            )
        size = count_tokens(chunk.text)
        if size < 0:
            raise ContextAssemblyError("Token counter returned a negative count.")
        if used + size > max_tokens:
            if overflow_policy == "error":
                raise ContextAssemblyError(
                    f"Context budget exceeded at chunk {hit.chunk_id!r}."
                )
            excluded.append(hit.chunk_id)
            continue
        selected.append(
            ContextItem(hit.chunk_id, hit.document_id, chunk.text, hit.rank)
        )
        used += size
    fairness_status = context_fairness_status(
        requested_max_tokens=max_tokens,
        actual_token_count=used,
        tokenizer_name=tokenizer_name or getattr(count_tokens, "__name__", None),
    )
    return AssembledContext(
        tuple(selected),
        used,
        tuple(excluded),
        overflow_policy,
        max_tokens,
        fairness_status,
    )
