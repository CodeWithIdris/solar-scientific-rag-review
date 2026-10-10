# Phase 6 — Independent Implementation Audit

**Audit scope:** source-code and synthetic-only technical audit of the Phase 6 scaffold.  
**Frozen research question:** unchanged.  
**Final corpus, benchmark, and experiment:** not accessed or run.

## 1. Files and components inspected

Inspected the Phase 1–5 design documents; Phase 6A implementation audit and Phase 6Z pilot report; `README.md`; `config/experiment.example.json`; all modules under `src/solar_rag/`; the synthetic pilot inputs and runner; and `tests/test_phase6_pipeline.py`.

The primary implementation surfaces were:

- Retrieval: `retrieval.py` — BM25, injected dense adapter, RRF, and hybrid wrapper.
- Execution/context: `pipeline.py`, `context.py`, and `generation.py`.
- Evaluation: `evaluation.py` and evaluation-related dataclasses in `models.py`.
- Validation/provenance: `corpus.py`, `benchmark.py`, `processing.py`, `config.py`, `quality.py`, `results.py`, and `runlog.py`.

This review verified code behavior and synthetic tests only. It did not evaluate scientific performance, approve a study setting, or establish corpus/benchmark validity.

## 2. Verified working components

| Component | Result | Evidence from implementation/tests |
|---|---|---|
| Corpus/benchmark input loading | PASS WITH LIMITATIONS | JSONL schema, duplicate IDs, source-path containment, and benchmark fields are validated; validation does not establish scientific eligibility. |
| Shared text processing/chunk identifiers | PASS WITH LIMITATIONS | Deterministic normalization/chunk IDs and source offsets are tested; production extraction/OCR quality is not verified. |
| BM25 | PASS WITH LIMITATIONS | Deterministic BM25 score computation, descending score order, and stable chunk-ID tie-break are present. The same injected tokenizer is used for index and query. Analyzer and parameters remain OPEN. |
| Dense retrieval | NOT IMPLEMENTED as a production model; PASS as adapter | `DenseRetriever` accepts external document/query encoders and similarity. It validates dimensions, numeric/finite values, and sorts scores descending. No production encoder, vector index, encoding policy, or similarity choice is supplied. It is not a working selected dense model. |
| Hybrid/RRF | PASS WITH LIMITATIONS | Reciprocal-rank fusion validates component labels, ranks, IDs, scores, weights, and conflicting chunk-to-document mappings; duplicate chunk IDs contribute once per component; stable chunk-ID tie ordering is used. Candidate depths, fusion constant, and weights are not selected for production. |
| Context assembly | PASS WITH LIMITATIONS | Common rank ordering, deduplication, evidence IDs, a positive token ceiling, and explicit overflow policy are implemented and tested. |
| Matched execution | PASS WITH LIMITATIONS | The same question, generator object, prompt artifact, generation parameters, context budget, and assembly rules are passed to all arms. The generator request has no explicit retrieval-condition field. Equal final cutoffs and identical indexed/context chunk records are now enforced. |
| Structured output and pairing | PASS WITH LIMITATIONS | Result rows have schema/status validation; a separate validator detects incomplete three-arm question pairs. Writing rows and enforcing complete pairs are not one atomic orchestration operation. |
| Failure/run metadata utilities | PASS WITH LIMITATIONS | Structured failure JSONL and timing hooks exist; callers must invoke them. They are not integrated into automatic retries or a fault-tolerant run controller. |

BM25 score ordering is highest score first; zero-score chunks are omitted. Dense ordering assumes the injected similarity returns larger-is-better scores; this is a callback contract rather than a verified property of any production model. RRF ranks component hits by their explicit `rank`, and its output score is a fusion score, not comparable to native BM25 or dense scores.

## 3. Metric correctness results

Phase 5 Sections 6–9 define answerable-only evidence Recall@k, reciprocal rank zero when no relevant evidence appears within evaluated depth, duplicate suppression, and graded nDCG@k with an OPEN relevance/alternative-evidence mapping.

| Metric/edge case | Result |
|---|---|
| Recall@k | PASS WITH LIMITATIONS — divides covered required evidence groups by the number of groups; alternatives within a group share one denominator unit. A missing required group yields zero contribution, not a missing observation. |
| MRR/RR | PASS WITH LIMITATIONS — uses the explicit hit rank and returns zero when the first relevant result is beyond `k` or absent. |
| nDCG@k | PASS WITH LIMITATIONS — implements gain `2^rel - 1` and logarithmic rank discount, and scores only when grades are supplied. Phase 5’s alternative-evidence/grade-set-to-IDCG mapping is OPEN; the implementation cannot determine whether alternative passages should be collapsed before IDCG. |
| Unanswerable retrieval item | PASS — retrieval metrics return `None` with `not_applicable_unanswerable`; the code does not conflate an unanswerable item with zero recall. Separate misleading-evidence/abstention diagnostics are not aggregated here. |
| Duplicate hits / invalid ranks / scores | PASS — duplicate chunk IDs count once; duplicate/non-positive/non-integer ranks and non-finite scores are rejected. |
| Fewer than k / rank gaps / multiple evidence groups | PASS WITH LIMITATIONS — metrics use reported rank and cutoff, not list length as a substitute for rank; hand-calculated synthetic tests cover multi-group coverage and cutoff behavior. Document-level recall is not implemented. |

Hand-calculated test case: for required groups `{c1, c1-alt}` and `{c2}`, hits at ranks 1 (irrelevant), 2 (`c1-alt`), 3 (duplicate `c1-alt`), and 4 (`c2`), at `k=3`, Recall@3 is `1/2 = 0.5`, RR@3 is `1/2 = 0.5`, and with unit grades on `c1-alt` and `c2`, nDCG@3 is `(1/log2(3)) / (1 + 1/log2(3))`. A relevant item only at rank 4 gives Recall@3 and RR@3 of zero. A no-relevant-hit case gives zero recall/RR. These are synthetic arithmetic checks, not study outcomes.

No scoring function operationalizes correctness, answer relevance, completeness, or faithfulness. `AnswerJudgment` is a record structure with limited range/status validation, not an evaluator. `attribution_metrics` is operational but depends on supplied human/other claim judgments. Its citation precision counts cited claim/evidence pairs; completeness measures required-claim coverage, not a general citation-recall score. Phase 4/5 choices about claim matching, partial support, and score scales remain OPEN.

## 4. Retrieval correctness results

| Check | Result | Finding |
|---|---|---|
| BM25 ranking | PASS | Formula and deterministic score-descending, chunk-ID tie ordering are implemented. |
| Tokenization | PASS WITH LIMITATIONS | BM25 uses the same supplied tokenizer on indexed chunk text and query. The production analyzer and technical-token behavior remain OPEN. |
| Dense ranking direction | PASS WITH LIMITATIONS | Descending ordering is explicit. No selected adapter exists to verify model-specific similarity semantics. |
| RRF rank/tie handling | PASS | Component ranks are used for fusion; final ties sort by chunk ID. |
| Hybrid duplicate chunks | PASS | A duplicate chunk contributes at most once in each component list; ranks from both components are retained. |
| Stable IDs/common schema | PASS WITH LIMITATIONS | Stable IDs are built in processing; retrievers return `RetrievalHit`. Runtime matched execution now checks full chunk-record equality against the context store, not only ID equality. |
| Missing/invalid scores | PASS | BM25, dense, RRF, and metric input paths reject non-finite values; dense rejects malformed embeddings. |
| Determinism | PASS WITH LIMITATIONS | Current built-in ranking/fusion tie behavior is deterministic for fixed inputs. External encoders/indexes and any provider behavior are not covered. |
| Production dense model | NOT IMPLEMENTED | Only an injected adapter is implemented; no model is selected or packaged. |

The audit added checks for duplicate IDs, rank/score validity, and BM25/dense chunk-set equality. Synthetic fixtures do not justify selecting any production parameter or model.

## 5. Fairness-enforcement results

**Enforced by `run_matched_question`:** exactly the three named arms, distinct retriever instances, identical final retrieval cutoff, identical full chunk records (including text and provenance fields) in every retriever and the context map, one question argument, common context budget/counting/overflow function, one generator instance, one prompt artifact, and one generation-parameter object. Retrieval condition is not passed as a generator instruction.

**Checked only by optional manifest validator:** equal corpus/document/chunk/question/evidence/evaluation versions and hashes, context controls, generator, prompt, decoding, and answer-evaluation version. The validator compares manifest values; it does not prove they correspond to runtime objects and is not automatically invoked by `run_matched_question`.

**Potential confounder / unresolved:** the code enforces the same maximum context-token budget, not identical realized token counts. Retrieval arms select different content and may yield different `context_token_count`; the `skip` policy can also leave unused budget. Counts are recorded but not compared across arms. Prompt and serialization overhead are not included by the context counter. This must be resolved and approved under the controlled-context rule before final testing; the audit does not invent a truncation/padding policy.

The same selection policy and rank order are used, but this alone does not guarantee identical realized context quantity. Different retrieved evidence is the intended treatment consequence; a systematically different amount of context is a separate fairness concern. The implementation now flags invalid citations to evidence IDs not supplied in the assembled context by returning an `invalid_citation` status and recording those IDs.

**Validation result:** PASS WITH LIMITATIONS. Automated synthetic tests confirm common arguments and reject differing cutoffs/chunk sets. Actual production arm manifests and realized context parity are NOT VERIFIED.

## 6. Failure-handling results

| Failure path | Result |
|---|---|
| Retrieval/generation/evaluator exception | PASS WITH LIMITATIONS — exceptions propagate; there is no broad catch or success-shaped fallback. |
| Empty retrieval | Representable as a failure/result status; no end-to-end policy automatically records the corresponding row. |
| Timeout/retry | NOT IMPLEMENTED — failure records have a `retryable` field and statuses include timeout, but no timeout or retry controller exists. |
| Malformed output/invalid evidence IDs | Statuses are available; invalid citations against the assembled context are now explicitly flagged. Full generated-output/evaluator validation is not integrated. |
| Structured logs | PASS WITH LIMITATIONS — append helpers write structured JSONL, but the pipeline does not automatically invoke them for every failure. |
| Failed observations | Not silently caught/deleted in the inspected pipeline; errors propagate. However, a failed arm can interrupt execution before a complete triple is stored. A later pairing validator can detect incompleteness but does not preserve/reconstruct the missing observation automatically. |

Failure policy, retries, timeouts, and intention-to-evaluate/missingness treatment remain OPEN in Phase 5. No production resilience claim is warranted.

## 7. Leakage-check limitations

**PASS WITH LIMITATIONS** for implemented heuristics. `quality.py` can flag normalized exact duplicate chunk/question text, duplicate DOI/title candidates, verbatim question/reference-answer occurrences in source text, exact duplicate questions across splits, and publication dates beyond a supplied cutoff. An unset cutoff is reported as not assessed.

It does **not** detect paraphrase/semantic leakage, near-duplicate documents/chunks, answer leakage beyond the exact reference-answer substring check, or general source-document overlap/related-paper contamination across development and test evidence. DOI normalization is basic. These are review heuristics, not a reliable leakage detector or proof of leakage prevention. Real-corpus checks are NOT VERIFIED.

## 8. Reproducibility limitations

**PASS WITH LIMITATIONS** for partial run metadata; **NOT VERIFIED** for study reproducibility.

- Manifest includes config hash, corpus and benchmark version strings supplied by caller, retrieval condition, selected fields for embedding/generator/prompt/seed, Python/platform, optional software versions/hardware, and Git commit where available.
- The manifest does not embed the full configuration, content hashes for corpus/benchmark/source files, complete active retrieval/index parameters, dependency lock/environment export, or model artifact hashes. Caller-supplied version labels do not prove artifact identity.
- `create_run_manifest` now marks any OPEN/PROVISIONAL/DEFERRED decision or missing required shared control as `configuration_incomplete`.
- Git was directly checked: `git rev-parse --show-toplevel` fails because the workspace is not a Git repository. The test confirms manifests record `git_commit: null`. No repository was initialized.
- No root dependency manifest/lock file was found. Current core code/tests use Python standard library; optional PDF support has no approved/installable dependency in the manifest.
- The configured environment reports Python 3.14.2 on Windows. No independent cross-platform/repeated-environment verification was performed.

Without source-control provenance, frozen source/data hashes, and a pinned dependency/environment record, a research run is not yet reproducible.

## 9. Tests rerun and exact outcomes

Final verification after audit fixes:

1. **Unit/integration suite:** `python -m unittest discover -s tests -v` — **39 tests passed, 0 failed, 0 errors**. The single suite includes retrieval, metric, ingestion, config, fairness, provenance, and pipeline tests; one test explicitly exercises the synthetic matched pipeline.
2. **Synthetic end-to-end smoke:** passed — 2 synthetic documents, 2 synthetic chunks, 2 synthetic questions, 6 condition executions. Output explicitly states no scientific performance was evaluated and production configuration is not ready.
3. **Configuration validation:** passed schema validation; reports unresolved methodological decisions and `study_execution_ready: false`.
4. **Input-schema validation:** passed — 2 synthetic documents and 2 synthetic questions; CLI explicitly says validation is not eligibility approval.
5. **Syntax/compile and imports:** `compileall` and imports of package, CLI, retrieval, evaluation, pipeline, quality, and run logging passed.
6. **Pylance diagnostics:** no errors reported for the 14 package modules and test file checked.

Audit iteration outcomes are retained for transparency: the first direct terminal test invocation lacked `PYTHONPATH` and failed importing `solar_rag`; after setting the documented source path, an intermediate 35-test run exposed an overstrict missing-grade assertion on alternative evidence. That assertion was removed because the alternative-to-grade mapping remains OPEN. Subsequent final runs passed; the final count is 39, not the earlier Phase 6 report’s historical 29.

No real corpus, final benchmark, scientific output, or comparative performance result was used.

## 10. Defects found and fixes made

1. **Metric depth/rank handling:** MRR previously searched beyond the evaluated cutoff and metrics relied on list order. Metrics now sort by validated explicit rank, apply the evaluated rank cutoff, deduplicate chunks, and reject duplicate/invalid ranks and non-finite hit scores. Added hand-calculated edge-case tests.
2. **Attribution validity:** a cited ID could be counted as valid without being supplied to the generator. Attribution now requires intersection with available context evidence; added regression test.
3. **Abstention classification:** invalid answerability labels were accepted and answerable-question abstentions were not counted as inappropriate. Labels are validated and answerable abstentions are classified as inappropriate; added tests.
4. **Matched-arm controls:** pipeline accepted unequal final cutoffs and retrievers indexing a different chunk set or different chunk content under the same IDs. It now rejects unequal cutoffs and full chunk-record mismatches; hybrid components must index identical chunk records. Added regression tests.
5. **Configuration readiness:** readiness previously could ignore null shared controls, and a schema-valid config could be reported as ready based only on decision status. Shared controls now participate in unresolved status; basic shared-control types/positive context budget are validated.
6. **Manifest status:** only OPEN decisions affected manifest status; PROVISIONAL/DEFERRED and missing shared controls could be mislabeled as recorded. Manifest status now uses the complete unresolved-configuration check; regression test added.
7. **Configuration schema guards:** missing decision `value` fields and malformed `shared_controls` could escape as low-level errors. The validator now rejects them explicitly; regression tests added.
8. **Retrieval validity:** BM25/dense/HYBRID paths now reject invalid identities, ranks, weights/parameters, or score values where applicable; hybrid components must expose identical chunk records. Deterministic ordering is explicit.

The implementation deliberately does not resolve nDCG’s alternative-evidence semantics, actual context-quantity policy, or any OPEN production setting.

## 11. Unresolved decisions

No production decision was selected. Remaining OPEN/PROVISIONAL items include: corpus eligibility/sampling/version and extraction/QC; benchmark questions/splits/answerability/evidence annotations; normalization and chunk size/overlap; BM25 analyzer/parameters; dense model/encoding/similarity/index; hybrid candidate depths/fusion settings; final retrieval cutoff; exact context-budget accounting and realized-quantity policy; generator/model, prompt, decoding and provider; correctness/relevance/completeness/faithfulness and attribution rubrics; alternative-evidence nDCG mapping; evaluator and reliability design; retries/timeouts/missingness; latency/resource protocol; and Phase 5 tests, intervals, thresholds, power/precision and analysis lock.

## 12. Methodological risks

- Realized context token quantity may differ by arm despite identical maximum budget; the final design must decide how this is controlled or amend/document it before final testing.
- `skip` context overflow can result in unequal selected-token totals and variable evidence counts.
- Retrieval metrics cover required evidence groups, not secondary document recall or unanswerable misleading-evidence rates.
- nDCG’s ideal ranking currently uses supplied grade values; alternative passage/evidence-group treatment remains OPEN.
- Human/automated answer scoring is not an implemented evaluator. Attribution depends on validated claim-level annotations.
- Optional fairness manifests are caller-supplied; equal metadata values do not establish runtime identity.
- A failure may leave incomplete triples; retries/missingness policy and durable orchestration remain absent.
- Basic exact-match leakage checks do not detect semantic or source-overlap contamination.
- Partial manifests and absent Git/dependency locks weaken repeatability.

## 13. Readiness blockers

Priority order:

1. No approved, screened, versioned solar-PV scientific corpus or verified extraction/provenance package.
2. No final/expert-validated benchmark with frozen questions, splits, answerability, evidence alternatives, and required claims.
3. Required Phase 2–5 technical and scoring parameters remain OPEN/PROVISIONAL; none may be chosen from synthetic fixtures.
4. Resolve context-budget accounting and possible realized context-quantity imbalance before the matched experiment.
5. Implement/approve operational answer-quality and evidence-attribution scoring, calibration/reliability, and unanswerable handling.
6. Lock failure, retry, timeout, missing-observation, latency, and statistical procedures.
7. Add immutable source control and full corpus/benchmark/config/model/dependency provenance; run and pass actual three-arm fairness/leakage checks before final test access.

## 14. Final readiness verdict

**INDEPENDENT PHASE 6 AUDIT: PASS WITH OPEN ITEMS**  
**FINAL-EXPERIMENT READINESS: NOT READY**

The synthetic scaffold is technically testable, and confirmed defects identified in this audit were corrected and regression-tested. Readiness remains blocked by missing real study artifacts, unresolved methodological choices, incomplete answer/evidence evaluation, context-quantity control, and reproducibility/failure-orchestration limitations. Passing synthetic tests are not evidence of scientific superiority. The final experiment was not run.

## 15. Phase 6B.1 completion audit addendum (2026-10-09)

The latest completion-pass claims were independently verified against the code and environment:

- The repo uses a `src/` layout; the initial direct test command failed with `ModuleNotFoundError` when `PYTHONPATH` was absent.
- The supported project command is therefore:
  `Set-Location "C:\Users\idrid\Downloads\solar-scientific-rag-review"; $env:PYTHONPATH = "src"; .\.venv\Scripts\python -m unittest discover -s tests -q`
- Observation: 41 tests ran, 41 passed, exit code 0.
- `pytest` is not installed in the active environment; `python -m pytest --version` exited with `No module named pytest`.
- The synthetic smoke test passed:
  `.\.venv\Scripts\python scripts\run_synthetic_pilot.py`
  output: 2 documents, 2 questions, 6 arm runs, `synthetic_technical_smoke_test_passed`.
- `git status --short` failed with `fatal: not a git repository`, confirming unavailable Git provenance.
- A minimal dependency manifest was added at [../../requirements.txt](../../requirements.txt) because no project dependency file existed.
- The implementation remains scientifically blocked despite passing synthetic checks; the real corpus, benchmark, model selection, context policy, and evaluation rubric remain unresolved.

This addendum preserves the earlier audit as historical evidence and adds the verified completion audit recorded above.
