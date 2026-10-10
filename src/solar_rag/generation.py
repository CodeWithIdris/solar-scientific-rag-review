from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence

from .context import ContextItem


class GeneratorConfigurationError(ValueError):
    """Raised when a generation decision is unresolved or a prompt is absent."""


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    question_id: str
    question: str
    context: tuple[ContextItem, ...]
    prompt_version: str
    prompt_text: str
    generation_parameters: dict[str, object]


@dataclass(frozen=True, slots=True)
class GenerationResult:
    answer: str
    cited_evidence_ids: tuple[str, ...]
    model_id: str
    raw_response: str
    finish_reason: str | None = None


class Generator(Protocol):
    model_id: str

    def generate(self, request: GenerationRequest) -> GenerationResult: ...


@dataclass(frozen=True, slots=True)
class PromptArtifact:
    version: str
    path: str
    sha256: str
    text: str


def load_prompt(path: str | Path, version: str) -> PromptArtifact:
    prompt_path = Path(path)
    if not version.strip():
        raise GeneratorConfigurationError("Prompt version must be explicit.")
    text = prompt_path.read_text(encoding="utf-8")
    if not text.strip():
        raise GeneratorConfigurationError("Prompt artifact is empty.")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return PromptArtifact(version, str(prompt_path), digest, text)


def build_request(
    *,
    question_id: str,
    question: str,
    context: Sequence[ContextItem],
    prompt: PromptArtifact,
    generation_parameters: dict[str, object],
) -> GenerationRequest:
    if not generation_parameters:
        raise GeneratorConfigurationError(
            "Generation parameters are unresolved; no provider defaults are assumed."
        )
    return GenerationRequest(
        question_id=question_id,
        question=question,
        context=tuple(context),
        prompt_version=prompt.version,
        prompt_text=prompt.text,
        generation_parameters=dict(generation_parameters),
    )
