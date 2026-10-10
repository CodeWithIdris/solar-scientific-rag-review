# Phase 1: Experimental Design Formalization

## Purpose and boundary

This document formalizes the frozen research question and the design constraints that must govern subsequent study phases. It defines the causal comparison and records which decisions are fixed versus still **OPEN**. It does not select models, corpus size, chunk size, top-k, hybrid fusion, benchmark metrics, or statistical tests. Those choices must be made and justified in the appropriate later design phase before implementation or data collection.

**Frozen research question**

> How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?

**Core principle:** Retrieval strategy is the principal manipulated variable. Every other experimentally relevant component is held constant across conditions unless a deviation is explicitly justified, documented, and assessed as a potential confounder.

## 1. Research question

The study compares the effects of BM25, dense, and hybrid retrieval on:

1. retrieval quality;
2. downstream answer quality; and
3. evidence attribution

for question answering over a shared corpus of solar-PV scientific literature. The comparison is controlled: the same question benchmark, corpus, preprocessing, generator, prompt, and evaluation protocol are used in all three conditions.

## 2. Independent variable

**Retrieval strategy**, with three categorical levels:

- BM25 retrieval;
- dense retrieval;
- hybrid retrieval.

The hybrid condition must combine lexical and dense retrieval, but its precise implementation, including fusion or combination method, is **OPEN**. No retrieval model, embedding model, analyzer/tokenizer, fusion rule, or parameter value is selected here.

No other factor is intentionally manipulated in Phase 1.

## 3. Experimental conditions

| Condition | Required identity | Implementation choices |
|---|---|---|
| BM25 | Lexical baseline using BM25 retrieval over the common prepared corpus | BM25 implementation, analyzer/tokenization, field treatment, parameters: **OPEN** |
| Dense | Dense semantic retrieval over the common prepared corpus | Embedding model/version, encoding and similarity/index settings: **OPEN** |
| Hybrid | A pre-specified combination of lexical and dense retrieval over that same corpus | Combination/fusion, normalization, weighting, deduplication, and parameters: **OPEN** |

All three conditions must use the same eligible corpus, question wording, preprocessing outputs, downstream generation conditions, and outcome-evaluation protocol. A purported condition that also changes the generator, prompt, corpus, chunking, context quantity, or another relevant component is not a clean retrieval-strategy condition; it must be flagged as confounded or separately justified and reported.

## 4. Dependent variables

The dependent-variable families are fixed by the RQ; their operational definitions and metrics are **OPEN**:

- **Retrieval quality:** quality of retrieved documents/passages/evidence relative to benchmark references or judgments.
- **Answer quality:** quality of the generated answer under the fixed generation condition.
- **Evidence attribution:** whether answer claims are attributed to supporting evidence from the shared corpus.

These are distinct outcome families. Retrieval performance must not be treated as a proxy for answer quality, faithfulness, or attribution. Evidence retrieval and generated-answer attribution must also be reported as distinct constructs where the chosen protocol measures both.

## 5. Secondary outcomes

Potential secondary outcomes, each requiring later justification and operationalization, are:

- answer faithfulness or support by retrieved evidence;
- answer-evidence alignment;
- citation precision and citation completeness/recall;
- abstention or answerability performance if the benchmark includes insufficient-evidence questions;
- retrieval and generation latency;
- computational/resource use or cost;
- subgroup results by question type, answerability, or evidence structure;
- robustness to repeated runs or other pre-specified perturbations.

Whether to include any item, and its metric, protocol, and multiplicity treatment, is **OPEN**. Do not assume that all secondary outcomes are required or available.

## 6. Controlled variables

The following conditions must be identical across the three retrieval arms:

- corpus membership and corpus snapshot/version;
- benchmark question set, wording, metadata, and answerability labels;
- document acquisition, extraction, normalization, and preprocessing;
- segmentation/chunking and document-to-retrieval-unit mapping;
- generator model and version;
- generation prompt and any system instructions;
- generation settings, decoding parameters, and other stochastic controls;
- context construction and quantity supplied to the generator;
- downstream evaluation protocol, reference material, assessors, and scoring instructions;
- compute environment and software versions where they can affect outputs;
- execution and logging procedures, subject to the randomized/repeated-run plan established later.

Which exact settings instantiate these controls is **OPEN**. Controls must be defined sufficiently precisely in the subsequent protocol that each arm is reproducible and comparable.

## 7. Experimental unit

The conceptual experimental unit is a benchmark question evaluated under a retrieval condition. Each question is to be exposed to all three retrieval conditions so that outcomes can be compared on a shared question set; this creates matched/paired condition observations at the question level.

The number of questions, any repeated generation runs, run order, randomization, and handling of stochastic outputs are **OPEN**. Whether a question contains multiple subquestions or is clustered by source paper must be assessed when the benchmark is defined.

## 8. Unit of analysis

The primary candidate unit of analysis is the question-level outcome within each retrieval condition, analyzed as matched outcomes across conditions. Where outcomes are claim-, citation-, passage-, or document-level, the aggregation to the question level and any hierarchical/clustered analysis are **OPEN**.

The statistical model, estimand, treatment of missing/invalid outputs, and whether inference generalizes beyond the benchmark items are **OPEN**. Individual claims or citations must not be treated as independent observations when they are nested within generated answers without a justified analysis.

## 9. Comparison structure

The planned structure is a three-condition, within-question comparison:

- BM25 vs dense;
- BM25 vs hybrid;
- dense vs hybrid.

Each comparison uses the same question benchmark and corresponding controlled outcome protocol. Retrieval outcomes are evaluated at retrieval level; answer and evidence-attribution outcomes are evaluated downstream using the contexts produced by each condition under identical generation constraints.

Primary contrasts, ordering, multiplicity adjustment, aggregation, and whether one overall omnibus test precedes pairwise comparisons are **OPEN**.

## 10. Experimental assumptions

The design relies on the following assumptions, to be examined and documented:

- The three conditions differ in retrieval strategy and not in other uncontrolled components.
- The corpus and benchmark are appropriate to the solar-PV scientific-literature scope of the RQ.
- Benchmark reference evidence and answer/evidence judgments are sufficiently valid and consistently applied.
- The same generation and evaluation procedures are applied to outputs from every arm.
- Retrieval indexes are built from equivalent source material and preprocessing outputs.
- Evaluation decisions are not influenced by knowledge of the retrieval condition where blinding is feasible.
- The outcome measures capture their intended constructs and are not conflated.

Operational tests of these assumptions and acceptable thresholds are **OPEN**. They must not be treated as established solely by this design document.

## 11. Potential confounders

Potential confounders include, but are not limited to:

- unequal corpus coverage, document eligibility, or index contents;
- different document extraction, cleaning, tokenization, metadata use, or chunking;
- different retrieval-unit granularity or duplicate handling;
- different numbers of retrieved items, total context tokens, truncation rules, or context ordering;
- different query rewriting, expansion, decomposition, or other query-time transformations;
- different rerankers, post-retrieval filters, or evidence compression;
- different generators, model versions, prompts, decoding settings, or system instructions;
- unequal compute, caching, timeout, or retry behavior that changes available evidence or outputs;
- condition-aware benchmark construction or tuning on evaluation questions;
- evaluator awareness of the retrieval condition or inconsistent scoring procedures;
- question/source-paper clustering, repeated questions, or leakage between corpus and benchmark construction;
- stochastic generation differences or unequal repeat counts.

These factors must either be held constant, excluded, or separately justified and recorded. A change that affects more than retrieval strategy is a potential confounder; do not silently incorporate it as part of the treatment.

## 12. Internal-validity threats

The protocol must assess:

- treatment contamination: an arm uses another arm's retrieved results or shared condition-specific artifacts;
- unequal retrieval context size or downstream evidence availability;
- different tuning effort or access to held-out/evaluation labels across arms;
- order, caching, rate-limit, or service drift effects;
- benchmark construction or annotation bias favoring one retrieval strategy;
- unblinded human scoring or inconsistent adjudication;
- selective exclusion of failed queries or model outputs;
- unreported deviations, retries, or missing data;
- stochastic variability obscuring or exaggerating condition differences;
- metric implementation or aggregation errors.

Mitigations, monitoring procedures, and severity thresholds are **OPEN** for protocol development.

## 13. Leakage controls

The subsequent protocol must specify and enforce:

- separation of corpus material used to construct benchmark questions/answers/evidence from any tuning data, where feasible;
- no tuning of retrievers, fusion parameters, prompts, or thresholds on final evaluation outcomes;
- controlled access to gold answers and reference evidence during system configuration;
- de-duplication and provenance checks for documents or question variants that could cross development/evaluation boundaries;
- separation of retrieval outputs and gold evidence during blinded assessment where feasible;
- logging of any benchmark exposure to models, annotators, or developers before evaluation.

The exact split strategy, deduplication rules, model-contamination checks, and annotation blinding plan are **OPEN**. Leakage risks must be reported even if complete elimination is infeasible.

## 14. Reproducibility requirements

Before execution, preserve sufficient information to reproduce each arm and analysis:

- corpus inventory, source provenance, eligibility decisions, and version/snapshot;
- document processing, extraction, preprocessing, and chunking configuration;
- retriever implementation, model identifiers and versions, configuration, and index-building procedure;
- hybrid-combination method and all parameters;
- generator identifier/version, prompt templates, generation settings, and context-construction rules;
- benchmark version, question/evidence references, annotation instructions, and splits;
- software/dependency versions, hardware/compute environment, and relevant service settings;
- per-query retrieval outputs, generated answers, evidence/citation outputs, run metadata, failures, and exclusions, subject to licensing/privacy constraints;
- evaluation code or scoring rubrics, statistical-analysis plan, and deviations from protocol.

The exact artifact format, repository, retention plan, licensing constraints, and release scope are **OPEN**.

## 15. Frozen decisions

The following are fixed for Phase 1:

1. The research question stated at the beginning of this document.
2. The target domain is solar-PV scientific literature.
3. The three experimental conditions are BM25, dense, and hybrid retrieval.
4. Retrieval strategy is the principal manipulated variable.
5. The three conditions share one corpus and one question benchmark.
6. Preprocessing, generator, prompt, and evaluation conditions are held constant across arms.
7. Retrieval quality, answer quality, and evidence attribution are outcome families and must remain analytically distinct.
8. A change affecting more than retrieval strategy is a potential confounder unless explicitly justified, documented, and analyzed as such.
9. No technical parameter may be selected merely because it is a convenient default.

## 16. Undecided parameters

All items below remain **OPEN** and must be resolved in a later, named design phase with rationale and evidence:

- corpus sources, eligibility criteria, size, time coverage, language scope, and document inclusion policy;
- question benchmark source/construction, size, types, answerability, evidence annotation, expert validation, and splits;
- benchmark sampling and question/source-paper clustering;
- document acquisition, PDF/text extraction, OCR, normalization, metadata fields, and preprocessing rules;
- retrieval unit, chunking method/size/overlap, and document-level aggregation;
- BM25 implementation, analyzer/tokenizer, fields, and parameters;
- dense embedding model/version, document/query encoding, similarity function, and index settings;
- hybrid fusion/combination method, normalization, weighting, deduplication, and parameters;
- candidate depth, final context count, context-token budget, truncation, and ordering;
- query rewriting, expansion, decomposition, or restriction to the original question;
- reranking, filtering, compression, and whether these are excluded or held constant;
- generator model/version, prompt, decoding settings, seed/repeat policy, and failure handling;
- exact retrieval, answer-quality, attribution, faithfulness, citation, abstention, latency, and resource metrics;
- human evaluation design, assessor qualifications, blinding, rubrics, adjudication, and agreement statistics;
- primary estimand, statistical model/test, paired analysis, confidence intervals, effect sizes, multiplicity control, and sample-size/power rationale;
- implementation environment, availability constraints, artifact release, and execution schedule.

This OPEN list is not permission to select defaults implicitly. Any selected value must be recorded in the later protocol with rationale and versioning.

## 17. Methodological risks

- A broad “hybrid” label can hide materially different systems. The later protocol must define the exact combination while preserving common conditions.
- Equal top-k does not necessarily imply equal context length, token budget, or evidence coverage. The meaning of equal context quantity must be fixed before testing.
- Equal context-token budgets may still yield different numbers of passages or evidence elements; the constraint and resulting differences must be reported.
- A benchmark with too few or unrepresentative questions may make paired effects unstable or limit generalization.
- Generated answers can be stochastic; a single run may not represent condition performance. Repeat strategy is **OPEN**.
- Retrieval metrics, answer correctness, faithfulness, citation precision, and citation completeness measure different properties and cannot substitute for one another.
- Solar-PV literature may contain heterogeneous terminology, document structures, and evidence representations that affect extraction and retrieval.
- Gold evidence may be incomplete or multi-valid; annotation protocol must account for this without favoring one arm.
- A retrieval arm may retrieve relevant but redundant or conflicting evidence; the answer and attribution protocol must define how that is scored.
- Resource and latency comparisons can be confounded by implementation or infrastructure differences; they are secondary unless subsequently specified otherwise.

## 18. Acceptance criteria

Phase 1 is accepted as a formal design boundary only if all of the following hold:

1. The frozen RQ and three retrieval conditions are stated without changing scope.
2. Retrieval strategy is the only planned manipulated variable.
3. Every controlled component is identified, and exact implementation settings not yet chosen are explicitly marked **OPEN**.
4. Retrieval quality, answer quality, and evidence attribution are distinguished as outcome families.
5. Experimental unit, unit of analysis, and matched comparison structure are stated without inventing sample sizes or statistical settings.
6. Confounders, internal-validity threats, leakage controls, and reproducibility requirements are identified for later operationalization.
7. No model, chunk size, top-k, fusion constant, metric threshold, corpus size, or statistical test is silently assumed.
8. The next phase is required to resolve OPEN parameters with documented rationale before implementation or data collection.

### Comparison-validation rule

If BM25, dense, and hybrid arms use different context quantities, prompts, generators, chunking/preprocessing, or generation settings, classify the comparison as **methodologically confounded** unless the deviation is explicitly justified, isolated, and reported. An identical question set alone does not make the comparison controlled.

If a proposed change affects anything beyond retrieval strategy, identify it as a **potential confounder** before incorporation. Do not silently redefine the experimental treatment to include unrelated system changes.
