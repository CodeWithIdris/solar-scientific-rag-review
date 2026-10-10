# Phase 6A — Project Implementation Audit

**Audit date:** 2026-10-08  
**Scope:** repository state before Phase 6 implementation  
**Status:** audit only; no corpus was ingested and no benchmark experiment was run.

## 1. Existing infrastructure

The repository currently contains:

- The frozen study protocols: [Phase 1](./phase1_experimental_design.md), [Phase 2](./phase2_retrieval_architecture_specification.md), [Phase 3](./phase3_corpus_design_protocol.md), [Phase 4](./phase4_benchmark_protocol.md), and [Phase 5](./phase5_evaluation_statistical_analysis_plan.md).
- Literature screening material: `literature/bib/Solar Scientific RAG.bib`, the screening CSV files, paper notes, `SCREENING_PROTOCOL.md`, and `scripts/build_screening_outputs.py`.
- A README documenting that the project was established for literature screening, with PDFs intended under `literature/pdfs/`.
- A local `.venv` containing Python 3.14.2 and pip. The environment has not been audited for retrieval/model packages; implementation should not rely on packages until justified by a dependency manifest and an explicit environment decision.

## 2. Reusable components

- The stable screening records and BibTeX library can supply literature discovery metadata, but they are not a corpus manifest and do not establish lawful full-text availability or extraction status.
- Phase 2 defines common chunk/result/context interfaces and fairness requirements; Phase 3 defines corpus provenance and document metadata requirements; Phase 4 defines benchmark fields and evidence annotation requirements; Phase 5 defines metrics, evaluation units, and failure semantics.
- `scripts/build_screening_outputs.py` is specific to literature-screening CSV generation. It is not a document ingestion or RAG pipeline and should remain untouched.

No implemented document extractor, chunker, retriever, generator, benchmark loader, evaluator, run store, or automated tests were found.

## 3. Missing components

- Corpus document manifest and lawful full-text files.
- Metadata validation, extraction adapters, shared normalization and chunking.
- BM25, dense embedding/index, hybrid fusion, common context assembly, and retrieval result contract.
- Frozen benchmark data and evidence/reference annotations.
- Generator/provider, prompt, output schema, and human/automated scoring integration.
- Retrieval/answer/evidence metrics, structured failures, timing, run manifests, config validation, leakage/fairness checks, and implementation tests.
- Phase 6 pilot-validation report and pilot artifacts.

## 4. Conflicts and methodological boundaries

No direct conflict in the instructions prevents building non-final infrastructure. However, the current Phase 1–5 protocols deliberately leave consequential settings open, including dense model, embedding behavior, index type, BM25 analyzer and parameters, candidate depths, hybrid fusion/RRF settings, chunk dimensions/overlap, context budget, generator, prompts/settings, benchmark size/split, score rubric, and latency procedure. These values must not be filled with convenient defaults or silently frozen by code.

Phase 2/3 do not authorize final corpus construction, final indexing, final benchmark construction, or experimental evaluation. Phase 6 authorizes implementation and a development/pilot stage, but no real corpus PDFs or benchmark are present. Technical validation can therefore use explicitly synthetic fixtures only; it cannot establish scientific retrieval or QA performance. Acquisition/selection of actual corpus and benchmark records remains gated on the earlier phase approvals and access policies.

## 5. Technical debt and risks

- There is no Git repository metadata in the workspace, so commit-based provenance cannot presently be recorded. A manifest must represent the commit as unavailable rather than inventing one.
- Bibliographic records in the screening library are heterogeneous and include grey literature, preprints, reports, and records that do not satisfy the Phase 3 primary-corpus policy. They must not be ingested as eligible documents without screening.
- Full-text extraction varies across PDF structure, tables, equations, OCR, and page locations. Lossy extraction must be explicitly surfaced; it cannot silently drop documents.
- Dense retrieval requires a selected model/runtime and potentially substantial downloads or compute. The interface should remain pluggable and refuse to run when a model is not configured.
- Generation requires a provider/model choice and possibly secrets. No provider or key may be hard-coded; generation must fail clearly when unconfigured.
- Evaluation contains OPEN score-scale, claim matching, and denominator decisions. Infrastructure can preserve raw annotations and compute only fully specified metrics; it must reject ambiguous/missing evaluation rules rather than fabricate scores.
- Corpus/benchmark leakage checks require source content and final split metadata that are not currently available. The checks can be implemented and validated synthetically but actual contamination status remains unknown.
- A generic framework risks suggesting methodological decisions have been made. Configuration and reports must carry explicit `FROZEN`, `PROVISIONAL`, `OPEN`, or `DEFERRED` status.

## 6. Dependencies

No root-level `pyproject.toml`, `requirements.txt`, lock file, Node manifest, or existing test configuration was found. The existing screening script uses the Python standard library. Prefer standard-library implementations for data validation, stable IDs, chunking scaffolding, BM25, metrics, manifests, and tests. External PDF, embedding, vector-index, LLM, or statistical packages may be introduced only after the related decision is approved, the dependency manifest is updated, and the chosen environment is explicitly configured.

## 7. Recommended implementation sequence

1. Establish a package/test layout, typed data contracts, versioned central JSON configuration, status validation, structured logs, and run manifest.
2. Implement corpus/benchmark ingestion validation, source/provenance preservation, deterministic preprocessing, and a shared chunk interface; test with synthetic records.
3. Implement transparent deterministic BM25 and common retrieval interface; leave analyzer and scoring parameters explicitly open/configurable.
4. Implement dense retrieval behind an injected embedding/index adapter. Add deterministic synthetic embeddings for tests only; do not select a production model.
5. Implement hybrid combination behind a configured fusion strategy; prevent production execution until Phase 2 candidate-budget/fusion choices are approved.
6. Implement shared context assembly with an explicit OPEN budget guard, common generator interface with no default provider/model, and prompt version loading.
7. Implement question-level retrieval metrics and claim/evidence scoring interfaces with strict input validation; do not invent unresolved rubric rules.
8. Implement failure states, timing hooks, leakage/fairness checks, reproducibility outputs, and focused synthetic unit/integration tests.
9. Execute only the synthetic technical smoke test. Do not use final questions, final corpus, or results to tune the primary protocol.
10. Produce the Phase 6 pilot report, clearly distinguishing verified synthetic pipeline behavior from unexecuted real-corpus/pilot components, and mark final-experiment readiness `NOT READY` while any gating OPEN decisions or source artifacts remain unresolved.

## 8. Audit conclusion

Proceed with a small, standard-library-first implementation scaffold and synthetic tests. Do not install dependencies, acquire/download literature, select production models, construct the final benchmark, or run final/test-set evaluation during this implementation step. Report unresolved decisions as blockers and preserve the frozen research question and three-arm design.
