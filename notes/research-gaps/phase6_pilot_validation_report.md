# Phase 6Z — Pilot Validation Report

## 1. Implementation status

**Status:** `PASS WITH OPEN ITEMS` for synthetic technical validation. This is not a scientific pilot and does not establish comparative retrieval or QA performance.

## 2. Components implemented

- Phase 6A project audit and implementation sequence.
- Central JSON experiment template with the frozen RQ, exact three-arm guard, and explicit decision statuses.
- JSONL document/benchmark ingestion, stable document IDs, duplicate rejection, source-path containment checks, non-overwriting corpus output, metadata records, and source provenance fields.
- Plain-text extractor and optional PyMuPDF adapter that reports the missing approved dependency explicitly.
- Conservative shared Unicode/whitespace normalization and explicit-parameter, stable-ID chunking with page/source metadata support.
- Deterministic BM25 implementation; injected dense embedding/similarity adapter; RRF hybrid retriever; common retrieval contract.
- Common context assembly with caller-supplied tokenizer, explicit budget, deterministic rank order, duplicate removal, and explicit overflow policy.
- Shared generator interface and prompt artifact hashing; no production provider, generator, prompt, or secret is selected.
- Benchmark loader, retrieval metrics (Recall@k, MRR, and nDCG only when explicit relevance grades are supplied), question-level paired differences, answer judgment records, attribution measures, and separate abstention outcome labels.
- Append-only result/failure logging, run manifest generation, timing hooks, cross-arm fairness checks, exact-match contamination/duplicate checks, and synthetic unit/integration tests.
- README instructions and a synthetic end-to-end smoke runner.

## 3. Tests performed

- Standard-library unit/integration suite against synthetic fixtures.
- Synthetic corpus-manifest ingestion, text extraction, shared chunking, benchmark loading, BM25/dense/hybrid retrieval, common context and generator interface, metrics, paired result validation, failure/run metadata, fairness and leakage checks.
- Example configuration validation and explicit demonstration that study execution remains blocked while decisions are OPEN.
- Synthetic input-schema validation.
- Python bytecode compilation.
- Pylance diagnostics on the implementation and tests.

## 4. Tests passed

- Historical initial Phase 6 validation: **29/29 automated tests passed** at that time.
- Independent Phase 6 audit rerun after audit fixes: **39/39 automated tests passed**.
- Synthetic end-to-end smoke test passed: 2 synthetic documents, 2 synthetic questions, and 6 condition runs (BM25, dense, hybrid for each question).
- Configuration validation passed and reported unresolved decisions; `study_execution_ready` was `false`.
- Synthetic document/benchmark input validation passed.
- Python compilation passed.
- Pylance reported no remaining errors in all checked package modules and the test file.

The final smoke test exercised software flow only. It did not score answers, evaluate scientific evidence, select a model, compare retrieval effectiveness, or create a result suitable for research claims. See the [independent implementation audit](./phase6_independent_implementation_audit.md) for the exact rerun commands/outcomes, intermediate failures, fixes, and remaining limitations.

## 5. Tests failed

The historical Phase 6 test run found one test-fixture document-ID mismatch in context assembly, corrected before its 29/29 pass. During the independent audit, the first direct terminal invocation lacked `PYTHONPATH` and failed to import `solar_rag`; after setting the documented source path, an intermediate run exposed an overstrict grade-completeness assertion for alternative evidence. That assertion was removed because the alternative-evidence relevance mapping is OPEN. The final audit suite passed 39/39 with no unresolved test failure. The observed intermediate failures are documented in the independent audit.

## 6. Known limitations

- No eligible full-text scientific corpus or approved corpus snapshot is present; the `literature/bib/` records are discovery/screening metadata, not an approved corpus.
- No final or expert-validated development/test benchmark exists. The pilot fixture text and questions are explicitly invented software fixtures and are not research evidence.
- Production PDF extraction is not enabled because a dependency/version and extraction acceptance procedure have not been approved. PyMuPDF support is an optional adapter only; no package was installed.
- Production dense retrieval has no embedding model, tokenizer/encoding instruction, vector index, similarity setting, or ANN configuration. Synthetic vectors are test-only.
- BM25 analyzer/parameters, production chunk boundaries/overlap, retrieval cutoffs, hybrid candidate budget/RRF parameters, context token budget/overflow rule, generator, prompt, generation controls, evaluation rubrics, and statistical decisions remain OPEN or PROVISIONAL.
- The context utility counts chunk-text tokens through an injected tokenizer; whether prompt/serialization overhead is included in the approved context budget remains OPEN and must be resolved before a real run.
- nDCG returns not-scored status unless explicit relevance grades are supplied. The Phase 4 relevance scale and alternative-evidence mapping are unresolved.
- Answer correctness, relevance, completeness, and faithfulness have judgment fields but no operational scoring functions. Attribution helpers depend on judgments supplied externally; there are no raters, calibration, scoring sessions, or adjudication data. No automated judge was selected.
- Timing hooks separate stages, but no study latency protocol, hardware, warm-up, cache, concurrency, or repeated-run procedure has been approved or measured.
- Leakage checks currently flag exact question/reference-answer text matches, exact duplicate chunk/question text, potential duplicate papers, and publication-cutoff violations when a cutoff is set. They do not establish semantic or paraphrase leakage, and real-corpus checks are unrun.
- Fairness validation is implemented and tested on synthetic manifests; no actual arm manifests exist. Matched execution now enforces equal final retrieval cutoffs and identical indexed/context chunk records (including text) and uses common generator/prompt/parameters. It enforces a common context-token ceiling, not equal realized token counts; that context-quantity issue is an explicit final-experiment blocker.
- Failure statuses/logging are implemented, but production retry/timeout handling is deliberately unresolved and there is no external provider integration.
- No confirmatory statistical tests, confidence intervals, power assessment, or significance decisions are executed by this scaffold; final Phase 5 decisions must be locked before these are implemented/run against study data.
- The workspace is not a Git repository; run manifests correctly record the commit as unavailable. Reproducibility therefore still requires establishing versioned source control before a real study run.

## 7. Unresolved configuration decisions

See [`config/experiment.example.json`](../../config/experiment.example.json). In particular:

- approved corpus and benchmark versions/split;
- extraction package/version and acceptance/QC;
- preprocessing and chunking configuration;
- BM25 analyzer and parameters;
- dense model, query/document encoding, similarity, and index;
- hybrid fusion, candidate depths, and candidate-budget semantics;
- retrieval cutoffs and context budget;
- generator/model, prompt, and generation/decoding settings;
- evaluation version, relevance grades, scoring rubrics, partial-support treatment, and thresholds;
- failure retries/timeouts;
- latency measurement protocol;
- final analysis-plan lock and reproducibility repository metadata.

Synthetic values in `data/pilot/synthetic_config.json` are not study decisions and must not be copied into the production configuration by default.

## 8. Reproducibility status

**Synthetic software validation:** reproducible within the configured Python 3.14.2 environment using the standard library; the test run and synthetic smoke command are documented in [README.md](../../README.md).  
**Research run:** not reproducible/ready. No Git commit, frozen corpus, benchmark, production model, prompt, complete configuration, or final run manifest exists. The run-manifest code emits a null Git commit rather than inventing one.

## 9. Cross-arm fairness status

**Implementation check:** present and covered by tests that detect a context-budget mismatch and reject different final retrieval cutoffs or indexed chunk records, including different text under matching IDs. The common matched-run interface sends all three arms through the same context assembly, generator object, prompt artifact, and generation parameters; it does not pass retrieval-condition identity as a behavioral instruction to the generator.

**Study status:** not yet empirically verified. There are no production indexes, final corpus/chunks, benchmark, or arm manifests. Actual context token counts can differ by arm under the common ceiling/skip policy; the protocol must resolve this before final testing. Before any research run, generate real manifests and require the fairness validator to pass with identical corpus/document/chunk/question/evidence/evaluation identities and all non-retrieval controls.

## 10. Data-leakage status

**Implementation check:** exact-text question/answer leakage, duplicate paper identifiers/titles, duplicate chunks/questions, cross-split exact duplicate questions, and configured publication-cutoff violations are checked and tested synthetically.

**Study status:** not assessed. The corpus and final benchmark are absent; the publication cutoff and split policy remain unresolved. Exact-match checks do not establish absence of semantic leakage.

## 11. Runtime observations

The local synthetic smoke completed successfully and processed 2 documents, created 2 shared chunks, exercised 2 synthetic questions across all 3 arms (6 total arm executions), and generated no performance report. This timing is an environment-specific software smoke observation only; it is not a retrieval, latency, or cost result.

## 12. Recommended fixes / blockers before final-experiment readiness

1. Resolve the Phase 1–5 OPEN decisions under their stated procedures and publish a versioned approved configuration; do not copy synthetic fixture settings.
2. Establish a Git repository or another immutable source-version mechanism before real runs.
3. Approve the Phase 3 corpus policy and lawful source set, acquire/screen full text, and validate extraction/provenance/retraction metadata.
4. Select and approve the PDF extraction dependency/version and quality-control policy.
5. Construct and freeze development and final benchmark artifacts under Phase 4, including evidence units/relevance, alternative evidence logic, answerability, and claim/citation references.
6. Select production retriever/model/index/fusion settings through approved development-only procedures and pin all artifacts.
7. Configure one approved generator/prompt and enforce matched generation/context controls.
8. Finalize the scoring rubrics, partial-support rule, nDCG relevance mapping, evaluator/reliability protocol, failure/retry behavior, latency procedure, statistical tests, effect thresholds, power/precision assessment, multiplicity and confidence intervals.
9. Extend leakage checks to the approved split/corpus evidence graph and perform/report actual contamination adjudication.
10. Create the immutable final config/run manifest and verify all three real-arm fairness manifests before any final-test access.

## Decision status

### FROZEN

- The research question is unchanged.
- BM25, dense, and hybrid are the only primary retrieval arms.
- Retrieval strategy is the principal manipulated variable.
- The same corpus, preprocessing/chunking, questions/evidence annotations, context constraints, generator/prompt/settings, and evaluation are required across arms.
- The question is the matched primary inferential unit; nested chunks, documents, claims, citations, and answer sentences are not independent observations.
- No composite score is used to manufacture a universal winner.

### PROVISIONAL

- RRF remains the Phase 2 working hybrid candidate; exact method/parameters/budget are not frozen.
- No-reranker architecture remains provisional.
- Three co-primary outcome domains and the candidate statistical hierarchy remain subject to Phase 5 resolution/lock.

### OPEN

- Production corpus and benchmark; document eligibility and extraction settings; BM25 and dense settings; hybrid budget/fusion parameters; chunking, retrieval cutoffs, and context budget; generator, prompt, and decoding; rubrics, graders, reliability, and relevance grades; retries/failure estimand; latency protocol; statistical effect thresholds, prospective precision/power, tests, interval procedure, and final config hash.

### DEFERRED

- Final benchmark evaluation, confirmatory statistical analysis, interpretation of comparative results, and any final-experiment readiness approval.

## Final decision

**PHASE 6 STATUS: PASS WITH OPEN ITEMS**  
**FINAL-EXPERIMENT READINESS: NOT READY**

Blocking issues are the absent approved real corpus and benchmark, unresolved production retrieval/generation/evaluation settings, missing PDF extraction approval, open Phase 5 statistical decisions, unrun real-data leakage/fairness checks, and lack of version-control commit provenance. No final experiment was run.

## 9. Phase 6B.1 completion addendum (2026-10-09)

The following completion-specific validation was audited independently and recorded:

- Initial unsupported test execution without `PYTHONPATH` failed with `ModuleNotFoundError` and exit code 1.
- The supported validation command is `Set-Location "C:\Users\idrid\Downloads\solar-scientific-rag-review"; $env:PYTHONPATH = "src"; .\.venv\Scripts\python -m unittest discover -s tests -q`.
- Observed result: `Ran 41 tests ... OK`.
- `pytest` is absent; the current environment does not provide it.
- Synthetic smoke test: `.\.venv\Scripts\python scripts\run_synthetic_pilot.py` passed and reported `synthetic_technical_smoke_test_passed` with 2 documents, 2 questions, and 6 condition runs.
- Dependency manifest: [../../requirements.txt](../../requirements.txt) was added because no manifest existed.
- Git provenance remains unavailable: `git status --short` returned `fatal: not a git repository`.

This addendum records the verified environment issue that caused the earlier failed run and preserves the earlier testing record as historical evidence.
