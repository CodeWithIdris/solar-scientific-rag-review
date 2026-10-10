from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .benchmark import load_benchmark
from .config import ConfigurationError, load_config, unresolved_decisions
from .corpus import CorpusValidationError, load_documents


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="solar-rag")
    commands = parser.add_subparsers(dest="command", required=True)
    config_parser = commands.add_parser("validate-config")
    config_parser.add_argument("path", type=Path)
    input_parser = commands.add_parser("validate-inputs")
    input_parser.add_argument("--corpus", type=Path, required=True)
    input_parser.add_argument("--benchmark", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate-config":
            config = load_config(args.path)
            print(
                json.dumps(
                    {
                        "status": "valid_schema",
                        "unresolved_decisions": unresolved_decisions(config),
                        "study_execution_ready": not unresolved_decisions(config),
                    },
                    indent=2,
                )
            )
            return 0
        documents = load_documents(args.corpus)
        questions = load_benchmark(args.benchmark)
        print(
            json.dumps(
                {
                    "status": "valid_inputs",
                    "document_count": len(documents),
                    "question_count": len(questions),
                    "note": "Input validation is not scientific eligibility approval.",
                },
                indent=2,
            )
        )
        return 0
    except (ConfigurationError, CorpusValidationError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
