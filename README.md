# Solar Scientific RAG Literature Audit

Working project title:

Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Energy Scientific Literature

This repository contains infrastructure for a methodological literature screening audit. It does not yet contain completed screening decisions or a final literature review.

## Repository Structure

- `literature/bib/Solar Scientific RAG.bib` - source BibTeX library.
- `literature/pdfs/` - intended storage location for full-text PDFs.
- `SCREENING_PROTOCOL.md` - screening rules, inclusion/exclusion criteria, controlled values, and evidence-recording requirements.
- `screening/screening_matrix.csv` - main extraction matrix for all candidate records.
- `screening/critical_papers.csv` - verified high-overlap or critical methodological papers.
- `screening/exclusions.csv` - excluded records with reasons and evidence locations.

## Current Status

The screening infrastructure has been created, but the actual literature screening has not been performed.

No paper should be classified as methodologically overlapping based only on a title, abstract, or search snippet when the relevant methodology is not explicitly established. Ambiguous papers should be marked for full-text verification.

## Phase 6B software completion status

The Phase 6 scaffold now includes explicit readiness gates for configuration validity, software readiness, scientific readiness, and confirmatory experiment readiness. Context assembly records requested and actual token use and sets a blocked fairness status until a production tokenizer is approved and verified. Failure logging distinguishes retrieval, generation, citation, evaluation, retry, and partial-arm failure states without silently converting exceptions into zero scores. Metric-implementation reporting classifies each metric as IMPLEMENTED, PARTIAL, SPECIFIED ONLY, or DEFERRED. These are software-level controls only; they do not approve a real scientific corpus, benchmark, model, prompt, or final experiment.

## Basic Workflow

1. Use `SCREENING_PROTOCOL.md` before making any screening decision.
2. Import BibTeX records into `screening/screening_matrix.csv`.
3. Verify methodological details from full text whenever possible.
4. Record uncertainty explicitly with `Unclear`, `Not assessed`, or `Potentially-Relevant`.
5. Record specific PDF evidence locations for inclusion, exclusion, overlap, and methodological claims.
6. Move or duplicate verified high-overlap papers into `screening/critical_papers.csv`.
7. Record excluded papers in `screening/exclusions.csv`.

## Controlled Decisions

Use these exact values for core screening decisions:

- `overlap_level`: `None`, `Low`, `Moderate`, `High`, `Critical`
- `relevance_decision`: `Include-Core`, `Include-Context`, `Potentially-Relevant`, `Exclude`
- `confidence`: `High`, `Medium`, `Low`

## Audit Rule

Do not claim novelty, decide the final research gap, modify the research title, invent missing methodology, or infer paper relevance from keyword matches alone. This repository is for methodological screening first.

## Phase 6 Implementation Scaffold

Phase 6 adds an implementation scaffold under `src/solar_rag/`, a central
configuration template at `config/experiment.example.json`, synthetic-only
fixtures under `data/pilot/`, and standard-library tests under `tests/`.
The fixture texts are invented test data, not scientific documents, corpus
evidence, or benchmark results.

The scaffold implements metadata/JSONL validation, append-only corpus writes,
extractor adapters (plain text and optional PyMuPDF), conservative shared text
normalization and explicit-parameter chunking, BM25, an injected dense-embedding
interface, RRF hybrid retrieval, common context assembly, a shared generator
contract, question-level retrieval/attribution metrics, failure/run logging,
timing hooks, fairness checks, and contamination checks.

Important Phase 2–5 settings remain **OPEN**. The example configuration
therefore cannot authorize a study run. It intentionally selects no production
embedding model, index, BM25 parameter/analyzer policy, chunk size, retrieval
cutoff, RRF settings, context budget, generator, prompt, scoring rubric, or
latency protocol. No provider credentials belong in the configuration file.
The optional PDF adapter raises an explicit error until a PyMuPDF version is
approved and installed; no dependency was added.

From the repository root in PowerShell, use the project-local virtual environment and set the source path explicitly:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python -m solar_rag.cli validate-config config\experiment.example.json
.\.venv\Scripts\python -m unittest discover -s tests -q
.\.venv\Scripts\python scripts\run_synthetic_pilot.py
```

The project currently supports the standard-library `unittest` runner. `pytest` is not installed and is not part of the supported validation path. The earlier direct invocation without `PYTHONPATH` failed with `ModuleNotFoundError: No module named 'solar_rag'`; that was an environment/setup issue, not a project-code failure.

`validate-config` reports unresolved decisions and does not run retrieval or
generation. To validate corpus/benchmark input syntax only, use:

```powershell
.\.venv\Scripts\python -m solar_rag.cli validate-inputs --corpus data\pilot\synthetic_documents.jsonl --benchmark data\pilot\synthetic_questions.jsonl
```

This validation does not establish scientific eligibility. The synthetic
benchmark is not a substitute for Phase 4 expert-validated data, and the
software tests do not count as a scientific pilot. Final corpus/test
construction and confirmatory evaluation remain prohibited until required
Phase 1–5 decisions and source artifacts are approved.

## Dependency and environment record

- Python version verified in this workspace: 3.14.2
- Runtime dependencies: none beyond the Python standard library in the current scaffold
- Test dependencies: none beyond the standard-library `unittest` runner
- Dependency manifest: [requirements.txt](./requirements.txt)
- Git provenance: unavailable in the current workspace; `git status` returns `fatal: not a git repository`

## Phase 7 corpus-acquisition workflow

The repository now includes a protocol-level solar-PV corpus acquisition workflow and curation utilities under [notes/methodology](./notes/methodology) and [src/solar_rag/corpus_workflow.py](./src/solar_rag/corpus_workflow.py). These components support auditable candidate metadata validation, duplicate detection, stable document-ID assignment, retraction/correction review, screening-status enforcement, and manifest generation for a real-world corpus workflow without approving a final scientific corpus or final experiment.

The frozen research question remains unchanged, and confirmatory-experiment readiness remains BLOCKED until a real corpus, benchmark, and production settings are explicitly approved.
