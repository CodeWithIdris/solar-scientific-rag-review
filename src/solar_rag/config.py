from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_ARMS = ("bm25", "dense", "hybrid")
ALLOWED_STATUS = {"FROZEN", "PROVISIONAL", "OPEN", "DEFERRED"}
FROZEN_RESEARCH_QUESTION = (
    "How do BM25, dense, and hybrid retrieval strategies, compared under "
    "identical corpus, question-benchmark, preprocessing, generator, prompt, "
    "and evaluation conditions, affect retrieval quality, answer quality, "
    "and evidence attribution in question answering over solar-PV scientific "
    "literature?"
)


class ConfigurationError(ValueError):
    """Raised when configuration is incomplete or internally inconsistent."""


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open(encoding="utf-8") as stream:
        config = json.load(stream)
    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != "1":
        raise ConfigurationError("schema_version must be the string '1'.")
    arms = config.get("primary_arms")
    if arms != list(REQUIRED_ARMS):
        raise ConfigurationError(
            f"primary_arms must be exactly {list(REQUIRED_ARMS)!r}."
        )
    if config.get("research_question") != FROZEN_RESEARCH_QUESTION:
        raise ConfigurationError("The frozen research question must not be changed.")
    decisions = config.get("decisions")
    if not isinstance(decisions, dict) or not decisions:
        raise ConfigurationError("decisions must be a non-empty object.")
    for name, item in decisions.items():
        if not isinstance(item, dict):
            raise ConfigurationError(f"decision {name!r} must be an object.")
        if "value" not in item:
            raise ConfigurationError(f"decision {name!r} must declare a value field.")
        if item.get("status") not in ALLOWED_STATUS:
            raise ConfigurationError(
                f"decision {name!r} must have a valid status."
            )
        if item.get("status") == "OPEN" and item.get("value") not in (None, ""):
            raise ConfigurationError(
                f"OPEN decision {name!r} must not specify an assumed value."
            )
    controls = config.get("shared_controls", {})
    if not isinstance(controls, dict):
        raise ConfigurationError("shared_controls must be an object.")
    required = {
        "corpus_version",
        "preprocessing_version",
        "chunking_version",
        "benchmark_version",
        "context_budget",
        "generator",
        "prompt_version",
        "generation_parameters",
        "evaluation_version",
    }
    missing = sorted(required.difference(controls))
    if missing:
        raise ConfigurationError(
            "shared_controls is missing fields: " + ", ".join(missing)
        )
    for name in (
        "corpus_version",
        "preprocessing_version",
        "chunking_version",
        "benchmark_version",
        "generator",
        "prompt_version",
        "evaluation_version",
    ):
        if controls[name] is not None and (
            not isinstance(controls[name], str) or not controls[name].strip()
        ):
            raise ConfigurationError(
                f"shared_controls.{name} must be a non-empty string or null."
            )
    context_budget = controls["context_budget"]
    if context_budget is not None and (
        isinstance(context_budget, bool)
        or not isinstance(context_budget, int)
        or context_budget <= 0
    ):
        raise ConfigurationError(
            "shared_controls.context_budget must be a positive integer or null."
        )
    generation_parameters = controls["generation_parameters"]
    if generation_parameters is not None and not isinstance(
        generation_parameters, dict
    ):
        raise ConfigurationError(
            "shared_controls.generation_parameters must be an object or null."
        )


def unresolved_decisions(config: dict[str, Any]) -> list[str]:
    unresolved = [
        name
        for name, decision in config["decisions"].items()
        if decision["status"] != "FROZEN"
        or decision["value"] in (None, "")
    ]
    required_shared = (
        "corpus_version",
        "preprocessing_version",
        "chunking_version",
        "benchmark_version",
        "context_budget",
        "generator",
        "prompt_version",
        "generation_parameters",
        "evaluation_version",
    )
    unresolved.extend(
        f"shared_controls.{name}"
        for name in required_shared
        if config.get("shared_controls", {}).get(name) in (None, "", {})
        or (
            name == "generation_parameters"
            and not config.get("shared_controls", {}).get(name)
        )
    )
    return sorted(set(unresolved))


def readiness_statuses(config: dict[str, Any]) -> dict[str, str]:
    """Return distinct readiness gates without permitting scientific defaults."""
    try:
        validate_config(config)
        schema_valid = "PASS"
    except ConfigurationError:
        return {
            "configuration_schema_validity": "FAIL",
            "software_pipeline_readiness": "NOT_READY",
            "scientific_study_readiness": "BLOCKED",
            "confirmatory_experiment_readiness": "BLOCKED",
        }

    unresolved = unresolved_decisions(config)
    software_ready = "READY" if not unresolved else "NOT_READY"
    scientific_ready = "BLOCKED" if unresolved else "NOT_READY"
    confirmatory_ready = "BLOCKED"
    return {
        "configuration_schema_validity": schema_valid,
        "software_pipeline_readiness": software_ready,
        "scientific_study_readiness": scientific_ready,
        "confirmatory_experiment_readiness": confirmatory_ready,
    }


def require_configured(config: dict[str, Any], component: str) -> None:
    unresolved = unresolved_decisions(config)
    if unresolved:
        raise ConfigurationError(
            f"{component} cannot run as a study configuration; unresolved "
            f"decisions: {', '.join(unresolved)}"
        )


def canonical_config_hash(config: dict[str, Any]) -> str:
    encoded = json.dumps(
        config, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
