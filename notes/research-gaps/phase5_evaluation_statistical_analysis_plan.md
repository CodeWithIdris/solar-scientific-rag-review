# Phase 5 — Evaluation Framework and Statistical Analysis Plan

## Status and scope

**Phase status:** pre-specified analysis framework. This document defines outcome constructs, statistical units, a test-selection decision tree, missingness rules, reporting, and plan-lock requirements. It does not run the experiment, calculate performance, tune retrieval systems, or choose a winner.

**Frozen research question (unchanged):**

> How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?

Labels:

- **FROZEN:** fixed by prior approved study design.
- **PROVISIONAL:** recommended analysis choice pending confirmation before test access.
- **OPEN — requires methodological decision:** unresolved; must be resolved and logged before final test outcomes are inspected.
- **DEFERRED:** belongs to a later protocol or execution stage.

No statistical method may be selected, replaced, or tuned because it gives a more favorable or statistically significant result. Decisions must be locked before final test analysis.

## 1. Phase 5 objective

Pre-specify:

- outcome hierarchy and operational definitions;
- primary question-level estimands and matched comparisons;
- retrieval, answer, evidence-attribution, abstention, and efficiency summaries;
- statistical tests, assumption checks, uncertainty intervals, effect sizes, and multiplicity control;
- missing and failed observation handling;
- evaluator blinding/reliability;
- exploratory relationship and subgroup analyses;
- sensitivity analyses, reproducibility artifacts, and an immutable plan lock.

Where Phase 4 annotation decisions or Phase 2 retrieval cutoffs remain OPEN, this plan records the dependency and the latest point at which the value must be frozen. No final test results may be accessed before those items are resolved.

## 2. Relationship to Phases 1–4

- **Phase 1:** retrieval strategy (BM25, dense, hybrid) is the only planned manipulated variable; common corpus, benchmark, preprocessing, chunking, generator, prompt, context budget, and evaluation conditions are required.
- **Phase 2:** defines retrieval architecture, context controls, and unresolved candidate-depth/top-k choices. Those values must be frozen before the final test evaluation.
- **Phase 3:** defines the solar-PV scientific-literature corpus and provenance. Corpus identity/version is common across arms.
- **Phase 4:** defines question IDs, answerability, evidence, required claims, numerical conditions, topic/difficulty labels, and matched development/test structure. Annotation reliability and OPEN benchmark decisions must be resolved before analysis lock.

This phase does not silently change any earlier decision. Any incompatibility is logged as a protocol issue; changes require a versioned amendment before test results are inspected.

**Confounder validation rule:** BM25, dense, and hybrid are the only primary retrieval arms, and retrieval strategy is the principal manipulated variable. The arms must use the same corpus snapshot and document set, preprocessing, chunking/retrieval-unit mapping, benchmark questions and evidence annotations, retrieval-evaluation protocol, context budget/assembly rules, generator, prompt, generation parameters and decoding settings, and answer/evidence-evaluation procedure. If conditions differ in any of these or another experimentally relevant component, the comparison is potentially confounded and must not be described as cleanly isolating retrieval strategy without a documented methodological justification and protocol amendment made before final test results are inspected. Do not introduce another experimental variable to resolve a confound.

## 3. Experimental structure

Each question is evaluated under all three conditions:

```text
question_id
  ├── BM25
  ├── Dense
  └── Hybrid
```

The design is within-question/matched. Analysis compares condition outcomes for the same questions. The three arms are not independent samples. The question benchmark and corpus version are common.

Primary inference concerns the performance differences on the frozen test benchmark. Generalization beyond those questions/corpus depends on sampling and benchmark design and must be qualified.

## 4. Statistical unit

1. **Experimental unit:** one benchmark question exposed to one retrieval condition; the same question is assigned to all three conditions.
2. **Observational unit:** one valid condition-specific run record for a question, including retrieval output and downstream answer where executed.
3. **Primary statistical unit:** the question. Calculate per-question/per-condition outcomes first, then compare matched conditions.
4. **Aggregation unit:** question-level score for each endpoint; summarize across questions and any predeclared strata.
5. **Document-level unit:** source papers are evidence/provenance and may induce clustering between questions. They are not automatically independent observations.
6. **Claim/citation/chunk/sentence units:** nested measurement units used to construct question-level metrics, not independent experimental sample units.

Repeated generation runs, if used, remain nested within question-condition and must be averaged or modeled accordingly; they do not multiply the independent question sample size.

## 5. Outcome hierarchy

### 5.1 Co-primary outcome domains — PROVISIONAL

The frozen RQ names three distinct outcome domains. To avoid promoting every metric to primary, designate one primary endpoint per domain:

1. **Retrieval quality:** question-level evidence Recall@k at the predeclared primary cutoff.
2. **Answer quality:** question-level factual correctness score under the Phase 4 claim/answer rubric.
3. **Evidence attribution:** question-level claim-attribution completeness, defined against the fixed Phase 4 set of required evidence-bearing claims; omitted claims do not disappear from the denominator.

One endpoint per domain is designated co-primary because the frozen RQ explicitly asks about three distinct outcome domains; a single endpoint could conceal a trade-off among them. This choice entails a larger confirmatory testing family and is paired with the multiplicity control in Section 28. These are co-primary domains, not a single composite or a system “winner” score. The exact retrieval cutoff and rubric score encoding must be frozen before final evaluation. Evidence-attribution denominator handling, especially on unanswerable items, is defined in Section 18.

**Status note:** Primary-domain selection is PROVISIONAL until Phase 4 gold-evidence/relevance reliability and Phase 2 primary retrieval cutoff are confirmed. If the prescribed evidence annotations cannot support the endpoint, amend the plan before test access; do not substitute a metric after seeing results.

### 5.2 Secondary outcomes

- MRR and nDCG@k, where the relevance annotation supports their interpretation;
- answer relevance, completeness, and faithfulness;
- evidence/citation precision;
- correct abstention and inappropriate abstention rates;
- multi-document required-source coverage;
- numerical answer correctness;
- retrieval, generation, and end-to-end latency;
- resource/cost outcomes if consistently measurable.

### 5.3 Exploratory outcomes

- retrieval-quality association with answer correctness, completeness, faithfulness, or attribution;
- subgroup differences by question type, answerability, single-/multi-document status, quantitative status, difficulty, and PV topic;
- sensitivity analyses not designated confirmatory;
- interactions or mechanisms not stated as primary hypotheses.

Exploratory results are labeled as such and are not used to redefine primary endpoints.

## 6. Retrieval-quality evaluation

### 6.1 Evidence and relevance representation

Use Phase 4 gold evidence IDs, evidence-set logic, relevance labels, claim links, and source document IDs. The primary retrieval unit should be the shared chunk/evidence unit because the system retrieves chunks; document-level performance is secondary and derived by mapping retrieved chunks to unique `document_id`s.

For each question, relevance is determined independently of retrieval outputs. The primary recall calculation uses required evidence units/claim-support units and allows the Phase 4 alternate-sufficient-evidence logic. Context/background evidence is not counted as required support merely because it is topically related.

Phase 4 must provide a sufficiently reliable evidence relevance annotation. Whether relevance is binary or graded, alternative-set matching, and final gold-unit matching are **OPEN — requires methodological decision** until annotation reliability is confirmed. If graded labels are unreliable, use binary support relevance for the confirmatory retrieval endpoints and retain graded results only as exploratory.

### 6.2 Metric aggregation

Compute each metric per question and condition. Report macro question-level summaries so questions with more chunks or citations do not receive greater statistical weight. Do not pool every chunk/rank across questions as if independent.

For multi-document questions, per-question recall can be partial; full source-set coverage is additionally reported as a secondary measure. MRR reports first relevant evidence only and cannot establish full multi-document sufficiency.

## 7. Recall@k

### 7.1 Primary definition

Let \(G_q\) be the set of distinct **required, retrievable gold evidence units** for answerable question \(q\), after collapsing alternative units according to Phase 4 evidence-set logic. Let \(R_{q,c}^{(k)}\) be the first \(k\) unique retrieved chunk IDs for question \(q\) under condition \(c\), after the common deduplication policy.

For binary evidence relevance:

\[
\operatorname{Recall@k}_{q,c}
=
\frac{\left|\{g\in G_q:\text{a retrieved unit in }R_{q,c}^{(k)}
\text{ matches/supports }g\}\right|}{|G_q|}
,\quad |G_q|>0.
\]

For multiple sufficient evidence sets, a retrieved item can cover the corresponding required claim/evidence role; equivalent alternate passages count as the same required evidence target rather than multiplying the denominator. The exact match/coverage mapping must be encoded in Phase 4 annotations before test lock.

### 7.2 Interpretation and multi-document cases

- Passage/chunk-level Recall@k is the primary retrieval measure.
- Document-level Recall@k is secondary: numerator is unique required source documents retrieved; denominator is required source documents.
- A multi-document item can receive partial passage/document recall if only some required evidence sources are found; report full required-source coverage separately.
- Duplicates count once.
- Retrieved irrelevant/context-only chunks do not enter the numerator.

### 7.3 Unanswerable items

Unanswerable questions have no gold evidence denominator. Do not assign retrieval Recall@k = 0, because that would conflate an appropriate absence of evidence with retrieval failure. Exclude these from the answerable-only retrieval Recall@k denominator and report separate unsupported-evidence retrieval/abstention diagnostics: whether the system retrieves misleading near-neighbor evidence and whether it abstains. Number of such items and exclusions are always reported.

### 7.4 Cutoff and reporting

The primary \(k\) is the final downstream candidate/context-selection depth or another predeclared retrieval cutoff, as justified in Phase 2. Its exact value is **OPEN**. Additional prespecified \(k\) values form secondary retrieval curves; do not choose the most favorable \(k\) after results. Report mean and median question-level Recall@k, spread, and paired differences with confidence intervals.

## 8. MRR

For answerable question \(q\), let \(r_{q,c}\) be the rank of the first retrieved unique chunk that supports at least one required claim or is annotated as directly relevant. Then:

\[
\operatorname{RR}_{q,c} =
\begin{cases}
1/r_{q,c}, & \text{if a relevant result is retrieved};\\
0, & \text{if none occurs within the evaluated depth.}
\end{cases}
\]

MRR is the macro mean of question-level reciprocal ranks over answerable questions. A duplicate relevant chunk does not create extra rank opportunities. For multiple relevant passages, only the first relevant result contributes to MRR; it does not measure whether all required passages or sources were retrieved. Therefore MRR is a secondary ranking metric and should be interpreted cautiously for multi-document/comparative synthesis.

Unanswerable items are excluded from standard MRR and analyzed with separate unsupported-evidence/abstention outcomes. No relevant result within candidate depth receives RR = 0, a true retrieval outcome, not missing data.

## 9. nDCG@k

For question \(q\) and condition \(c\):

\[
\operatorname{DCG@k}_{q,c}
=\sum_{i=1}^{k}\frac{2^{rel_{q,c,i}}-1}{\log_2(i+1)}
\]

\[
\operatorname{nDCG@k}_{q,c}
=\frac{\operatorname{DCG@k}_{q,c}}{\operatorname{IDCG@k}_{q}}
\]

where `rel` is the frozen relevance grade for the retrieved chunk relative to the question's required claims/evidence. IDCG is the ideal ranking of the available gold relevance units under the same `k` and set logic.

The grade scale and gain mapping are **OPEN** because Phase 4 marks relevance grades provisional. Do not adopt an example scale without validating annotator agreement. If a graded scale is not sufficiently reliable, use binary relevance with a prespecified binary DCG gain and label that version clearly. nDCG@k is secondary; report answerable questions only. Unanswerable questions have no IDCG and are evaluated separately.

## 10. Answer-quality evaluation

Answer outcomes are scored per question and condition using Phase 4 reference answers, required claims, conditions, numerical rules, caveats, and contradictory-evidence annotations. Preserve separate dimensions:

- correctness;
- relevance;
- completeness;
- faithfulness.

Human evaluation is the reference standard for subjective/scientific judgments unless a validated deterministic metric is appropriate. Any automatic score remains separate and is not silently substituted for human judgments.

## 11. Correctness

Correctness is whether the answer's substantive claims are scientifically consistent with the frozen corpus/reference and correctly scoped to conditions and uncertainty.

Candidate question-level rubric (**PROVISIONAL; anchors require calibration before test**):

- **2 — Correct:** all material claims are supported as scientifically accurate; no material condition/unit/causal-strength error.
- **1 — Partially correct:** some required facts are accurate, but at least one required claim/condition is missing or a non-central error/qualification exists; no materially false central conclusion.
- **0 — Incorrect:** central answer is false, materially contradicts the evidence, answers the wrong condition/question, or fabricates a decisive claim.

For answerable questions with multiple required claims, preserve claim-level correctness and derive question-level score by the approved rubric, not exact string matching. For unanswerable questions, correctness is assessed through the abstention/unsupported-answer rubric, not by treating silence as correct on all items.

Equivalent wording and multiple valid answers are accepted if they preserve the supported proposition, condition, and evidential strength. Conflicting literature is scored against the structured reference that represents the disagreement, not a forced single value.

## 12. Relevance

Relevance measures whether the response addresses the question asked.

Candidate rubric (**PROVISIONAL**):

- **2:** directly answers the requested scientific issue and stays on scope;
- **1:** partially addresses it but includes notable irrelevant material or misses a requested aspect;
- **0:** answers a different question, is largely off-topic, or gives no relevant response where an answer is available.

Raters score relevance independently of factual correctness. A fluent, correct statement that does not answer the asked question may be correct in isolation but irrelevant.

## 13. Completeness

Use Phase 4 required claims. For answerable question \(q\):

\[
\operatorname{Completeness}_{q,c}
=\frac{\sum_{j=1}^{m_q} w_{qj} I(\text{required claim }j\text{ is correctly present})}
{\sum_{j=1}^{m_q}w_{qj}}
\]

Equal weights are the default candidate; weights are **OPEN** and should remain equal unless Phase 4 establishes a scientific reason for unequal criticality before test evaluation. Optional claims are excluded from the denominator. Conditions, units, comparison sides, and required caveats are claims or claim qualifiers in the denominator where annotated as essential.

Report the question-level proportion and macro-average across questions. The numerator is not the number of generated sentences. For unanswerable questions, completeness is handled as abstention/uncertainty communication rather than an empty required-claim set.

## 14. Faithfulness

Faithfulness is the degree to which substantive answer claims are supported by the **retrieved context supplied to the generator**, not merely by any document in the corpus or by external knowledge.

At claim level, classify each answer claim as:

- supported by retrieved evidence;
- partially supported/overstated;
- unsupported by retrieved evidence;
- contradicted by retrieved evidence;
- unscorable due to malformed/insufficient attribution record.

Aggregate to a question-level proportion of scorable claims supported, while reporting partially supported and contradicted claims separately. This is distinct from correctness: a factually true claim absent from supplied evidence can be unfaithful; an answer can be faithful to retrieved text but scientifically incomplete or based on a source's limited claim.

Exact claim segmentation, treatment of purely stylistic claims, and rubric anchors are **OPEN** under Phase 4 and must be calibrated before test scoring.

## 15. Evidence-attribution evaluation

Evaluate at claim and citation/evidence level, then aggregate to the question. Claim-level attribution is the primary conceptual unit because compound answers may contain multiple assertions and citations can support one assertion but not another. Raw claim/citation counts are never treated as independent experimental `n`.

Each answer claim is linked to:

- required/reference claim, if applicable;
- zero or more generated citation/evidence IDs;
- actual retrieved chunk/document/span;
- support status and scope/condition;
- whether a citation is absent, incorrect, partial, or contradictory.

The question-level endpoint and denominator rules below must be finalized before scoring.

## 16. Claim-level attribution

Definitions:

- **Supported claim:** cited retrieved evidence entails or directly supports the claim at the stated scope, condition, and certainty.
- **Partially supported claim:** evidence supports only a subset of the proposition, omits an essential condition, or is weaker than the wording.
- **Unsupported claim:** no supplied retrieved evidence supports it.
- **Incorrectly attributed claim:** cited evidence is irrelevant, misidentified, attached to the wrong claim, or concerns a materially different condition/result.

Compound claims are split into atomic propositions when their components can differ in truth/support. A trained annotator applies the Phase 4 segmentation guide; a second reviewer independently checks a sample or all claims according to the approved annotation plan. Preserve the original sentence and the mapping to atomic claims. Segmentation rubric and reliability threshold are **OPEN** and must be frozen before final test scoring.

## 17. Evidence/citation precision

For question \(q\), define a **claim-citation pair** as one explicit citation/evidence reference linked by the answer to one atomic claim. Let \(P_q\) be the number of such pairs whose cited retrieved evidence actually supports the linked claim at the claimed scope/condition; let \(C_q\) be the total number of scorable claim-citation pairs.

\[
\operatorname{AttributionPrecision}_q = P_q/C_q,\quad C_q>0.
\]

Report the proportion of incorrect/irrelevant/partial citations separately. A claim with two citations contributes two pairs; do not give automatic credit to one good citation if another citation attached to the same claim is materially wrong. Treatment of a partially supporting pair and multiple citations for equivalent evidence is **OPEN**, to be resolved in the scoring rubric before test scoring.

If no citations are provided, precision is undefined, not 1. Report citation absence and attribution completeness separately. Do not silently set undefined precision to zero and mix it with scored precision; the final aggregation rule is **OPEN**.

## 18. Evidence/citation completeness

For answerable questions, let \(A_q\) be the number (or predeclared weight) of required evidence-bearing claims in the frozen Phase 4 reference, whether or not the system includes them; let \(S_q\) be the number of those claims that are correctly stated and have at least one valid supporting citation to retrieved evidence.

\[
\operatorname{AttributionCompleteness}_q = S_q/A_q,\quad A_q>0.
\]

Optional contextual claims/citations are not in the denominator. An omitted required claim remains in the denominator and contributes no complete attribution. A missing citation reduces completeness but is not an incorrect citation. Incorrect citation means a citation is present but fails to support the linked claim; it reduces precision and does not count as complete support. A claim that is factually incorrect is not counted as a correctly stated claim for complete attribution.

Unanswerable questions use abstention/citation-fabrication outcomes; they do not have a normal answer-claim completeness denominator. Report invented citations separately.

## 19. Unanswerable questions

Use the Phase 4 answerability labels:

- answerable from corpus;
- answerable in principle but unsupported by this corpus;
- insufficient/indeterminate evidence;
- invalid question (excluded before final test).

Only valid unsupported/insufficient items enter abstention analysis. Preserve the two unanswerable subtypes separately in data; whether to pool them is **OPEN** before test lock.

Answerable questions where a system retrieves no evidence remain answerable benchmark items; they are not relabeled unanswerable based on a condition's failure.

## 20. Abstention evaluation

Primary abstention outcome for valid unanswerable questions is **correct abstention rate** at question level:

\[
\text{Correct abstention rate}
=\frac{\text{unanswerable questions with explicit, appropriate evidence-insufficiency response}}
{\text{all valid unanswerable questions with a valid system response}}.
\]

Correct abstention, unsupported answer, and hallucinated/contradictory answer are distinct question-level outcomes. **Unsupported answer** means a substantive assertion lacks support in the available corpus/context; **hallucinated answer** means a fabricated or materially invented assertion, with contradiction recorded separately. A hallucinated assertion may also be unsupported, but the labels must not be treated as synonyms. Report alongside:

- inappropriate abstention rate on answerable questions;
- unsupported-answer rate on unanswerable questions;
- hallucinated/contradictory answer rate;
- partial supported-answer-plus-uncertainty rate where appropriate.

A generic refusal is not automatically correct: it must correspond to an unanswerable item and communicate insufficiency. On answerable items, an unjustified refusal is an inappropriate abstention. Confidence calibration metrics are not included unless a calibrated confidence output is part of the frozen response format.

## 21. Multi-document evaluation

For multi-document items:

- report passage-level and required-document Recall@k;
- report complete required-source coverage (all mandatory source documents/evidence roles retrieved) as a secondary binary outcome;
- assess answer completeness against all required source-linked claims;
- assess whether the answer synthesizes the relationship, not just lists isolated findings;
- require attribution to each source needed for a complete synthesis;
- report partial retrieval/answer coverage without awarding full credit when a necessary source is absent.

Alternative sufficient source sets follow Phase 4 logic. One paper summarizing another is not counted as two retrieved sources unless Phase 4 annotations explicitly make that document a sufficient alternative. Multi-document items remain one question-level statistical unit.

## 22. Quantitative-answer evaluation

Score numerical responses against Phase 4 item-specific value, unit, condition, metric definition, and tolerance.

Full numerical credit requires:

- value within the predeclared permissible rounding/tolerance;
- compatible unit or a valid, correctly applied conversion;
- correct experimental condition/sample/technology/time period;
- correct metric identity and direction (e.g., efficiency vs power, rate vs total).

Partial/zero scoring for wrong units, wrong conditions, missing values, or unsupported conversions is set in an item-level rubric before test scoring. Do not tune tolerance after observing system answers. If a value has no scientifically justified tolerance, compare at source-reported precision after a predeclared rounding rule or exclude the question before test freeze.

Numerical tolerance and item score mapping remain OPEN until Phase 4 annotations are approved.

## 23. Efficiency evaluation

Report separately:

- retrieval latency;
- generation latency;
- end-to-end latency;
- resource use/memory and computational cost where consistently measurable.

Record hardware, software, concurrency, batch size, cache state, warm-up, network/provider, retries, timeouts, and measurement timestamps. Use a predeclared warm-up and repeated timing protocol on the same environment. Do not interpret total latency as retrieval latency. Report medians and interquartile ranges for skewed latency, plus mean/standard deviation when useful.

Latency/resource analysis is secondary. Exact repeats, warm-up count, cost accounting, and resource metric are OPEN and must be frozen before measurement. The hybrid arm's two component searches must be included in its retrieval cost.

## 24. Descriptive statistics

For each outcome and condition report:

- question count and valid/missing/failure counts;
- mean and standard deviation for approximately symmetric question-level distributions;
- median, interquartile range, minimum, and maximum for skewed/bounded outcomes;
- proportions with numerator/denominator and confidence intervals for binary outcomes;
- question-level paired differences and their distribution;
- category/topic distribution and denominators.

For each pairwise comparison report absolute difference on the original scale, paired effect size, confidence interval, and corrected p-value where inferential testing is designated. Do not report only a pooled mean or a rank ordering.

## 25. Primary comparison

The primary comparison is a three-condition within-question comparison for each co-primary outcome domain:

1. BM25 vs dense;
2. BM25 vs hybrid;
3. dense vs hybrid.

For each domain, calculate the omnibus condition test and all three predeclared pairwise contrasts. The omnibus test assesses whether any condition differs; it does not establish which pair differs. The confirmatory tests are not gated on omnibus significance: the omnibus and all pairwise tests belong to the single multiplicity family defined in Section 28 and are interpreted only using that procedure. Pairwise effects and uncertainty are reported for all planned contrasts.

There is no single composite rank or universal winner. A condition may perform differently across retrieval, answer, and attribution outcomes.

## 26. Statistical-test selection

### 26.1 Prespecified decision tree — PROVISIONAL pending endpoint encoding

Use question-level matched outcomes, with condition as the within-question factor. Select tests by the outcome's measurement type and design, not by observed p-values:

| Outcome type | Omnibus condition test | Pairwise follow-up | Assumptions / fallback |
|---|---|---|---|
| Binary correctness/complete-source/correct-abstention | Cochran's Q for complete matched binary observations | Paired McNemar tests | If sparse discordant cells, use exact McNemar; family correction applies |
| Ordinal rubric score | Friedman test | Paired Wilcoxon signed-rank if difference distribution/symmetry assumptions are tenable; otherwise paired permutation/sign test | Report ordinal distributions; use permutation fallback predeclared |
| Bounded per-question proportion (Recall@k, completeness, attribution proportion) | Friedman on question-level scores as conservative rank-based primary; paired permutation test may be the prespecified robustness check | Wilcoxon signed-rank or paired permutation on within-question differences | Do not treat constituent passages/claims as independent trials |
| Continuous outcome such as log latency | Repeated-measures model or Friedman/paired permutation based on prespecified scale and diagnostics | Paired t-test only if paired differences justify it; otherwise Wilcoxon/permutation | Latency model and transformation must be locked before timing results |

The exact primary method for co-primary endpoint variables must be frozen once annotation scales, missingness policy, and endpoint cutoff are known, before test data access. Do not choose between parametric/non-parametric methods based on which is significant.

### 26.2 Model-based alternative

Mixed-effects models may be used if the number of observations, question clustering, repeated runs, and data structure require covariate or random-effect handling. A candidate model includes fixed retrieval condition and random intercepts for question, with source-paper/evidence cluster effects where estimable. Binary outcomes may use a logistic GLMM; ordinal outcomes an ordinal mixed model; continuous outcomes a linear mixed model with justified residual structure.

Model family, link, random-effects structure, convergence criteria, and fallback must be prespecified before test outcomes. Do not fit increasingly complex models until a favorable result appears. If a mixed model is selected as primary, use the paired nonparametric/permutation approach as sensitivity, not as a significance-driven replacement.

## 27. Assumption checks

Check and record before interpreting inferential results:

- pairing and question-ID alignment across conditions;
- independence across question units; identify shared source-paper/question-family clustering;
- outcome scale and validity of aggregation;
- paired-difference distribution/normality for paired t-tests or linear models;
- sphericity for repeated-measures ANOVA if considered; apply a prespecified correction or avoid the method if unsuitable;
- homoscedasticity for models where relevant;
- sparse cells/separation and convergence in generalized models;
- influential observations and floor/ceiling effects;
- missingness patterns and reasons by arm/question/category;
- rater agreement and score reliability.

Assumption checks are not a menu for choosing whichever method yields significance. If the prespecified model assumptions fail, apply the predeclared fallback in Section 26 or label the model-based result non-estimable; retain the primary analysis rule and report deviations.

## 28. Multiple-comparison correction

### 28.1 Confirmatory family

There are three co-primary domains. The confirmatory family contains exactly twelve hypotheses: one omnibus condition test and three pairwise contrasts for each domain (three omnibus plus nine pairwise). Apply one Holm procedure across all twelve p-values. The procedure does not gate pairwise tests on omnibus results and no p-value is interpreted under a second, incompatible family scheme. Report raw and Holm-adjusted p-values, exact family membership, effect sizes, and confidence intervals. Pairwise interpretations must identify their endpoint/domain; a significant omnibus result does not by itself identify a differing pair.

This family must be frozen before test analysis. If the project instead selects a single primary endpoint by amendment, revise the family definition before outcome access.

### 28.2 Secondary and exploratory families

Secondary outcome families use Holm correction within predeclared construct families if confirmatory claims are intended; otherwise label results descriptive/secondary and avoid confirmatory language. Exploratory subgroup/correlation analyses use false-discovery-rate control (e.g., Benjamini-Hochberg) within a clearly declared exploratory family or report unadjusted exploratory estimates with explicit multiplicity caveat. The choice is set before analysis, not based on significance.

Family-wise error controls false positives across confirmatory claims; false-discovery-rate control limits the expected proportion of false discoveries among a larger exploratory set. Do not mix the purposes.

## 29. Effect sizes

Report effect sizes matched to outcome type:

| Outcome | Effect size |
|---|---|
| Bounded continuous/proportion question score | Paired mean difference and median paired difference on original scale; optionally paired standardized difference with clear definition |
| Ordinal outcome | Rank-biserial correlation for pairwise contrast; Kendall's W for Friedman omnibus where appropriate |
| Binary outcome | Paired risk difference in percentage points and matched odds ratio; discordant-pair counts |
| Citation/claim proportions | Question-level paired difference; avoid treating claims as independent; claim-weighted pooled figures only as descriptive |
| Latency/resource | Median and mean paired difference or ratio on original scale/log scale, with method stated |
| Correlation | Spearman rho (exploratory); report CI and unit of analysis |

Do not force Cohen's d onto ordinal/binary or nested outcomes. Define direction so positive differences consistently indicate the named first condition minus the second. Statistical significance is not practical significance; no smallest effect threshold is specified here and it is **OPEN**.

## 30. Confidence intervals

**Confidence level: PROVISIONAL.** A 95% confidence interval is the candidate convention for primary effects and proportions, but it must be confirmed before test evaluation alongside the inferential error threshold and multiplicity plan. For paired condition differences, use a question-level paired bootstrap:

1. resample question IDs with replacement;
2. keep all three condition observations and all nested annotations for each sampled question together;
3. recompute the question-level endpoint and matched contrast;
4. calculate the prespecified interval (method, e.g., percentile or BCa, must be selected before test analysis).

Never bootstrap individual chunks, claims, tokens, citations, or answer sentences as independent observations. The question is the resampling unit because it is the matched experimental unit. If multiple questions share source-paper/evidence groups, those questions may have dependent outcomes; where the number of independent groups supports it, a cluster-level bootstrap may be used as a prespecified sensitivity, resampling whole source-paper/evidence groups and retaining all associated questions and arms together. Exact interval algorithm, replicate count, seed, and multiplicity-compatible intervals are **OPEN** before test access.

Unless a multiplicity-compatible interval procedure is selected before test analysis, label the reported 95% intervals as pointwise intervals; do not interpret them as simultaneous coverage for the twelve-test confirmatory family.

### Precision and power

No sample size, minimum detectable effect, or power target is selected here. Before final test access, perform a prospective precision/power assessment using the planned matched design, benchmark question count and strata, primary outcome scale, plausible within-question dependence, co-primary multiplicity procedure, and a substantively justified effect threshold. Document the assumptions and show sensitivity to plausible effect sizes. If the available benchmark cannot support a meaningful precision target, state that limitation and treat estimates as imprecise rather than inventing a post-hoc power justification. Exact target, effect threshold, and calculation method are **OPEN — requires methodological decision**.

## 31. Correlation analysis

Retrieval quality versus downstream answer/faithfulness/attribution relationships are **EXPLORATORY**. The primary descriptive association is question-level Spearman correlation between per-question retrieval score and per-question downstream score within each retrieval arm. Do not pool all arm-question rows as independent; report arm-specific association and account for repeated questions.

An exploratory repeated-measures model may include retrieval score, condition, and question-level dependence if the estimand and model are specified before use. Pearson correlation is used only if linearity, scale, and distribution support it; do not choose by stronger correlation. Correlation does not establish that better retrieval caused better answers.

## 32. Retrieval-to-answer analysis

Explore whether question-level retrieval quality is associated with:

- correctness;
- completeness;
- faithfulness;
- evidence-attribution completeness.

Use matched question-level records and preserve condition. Possible analysis: arm-specific Spearman correlations and descriptive plots, followed by a prespecified mixed model if justified. Report uncertainty and multiplicity handling. Label all findings exploratory unless a causal mediation/confirmatory design is formally justified in advance; the current design does not by itself identify causal mediation from retrieval score to answer quality.

## 33. Category-level analysis

Predeclared descriptive/secondary subgroup dimensions:

- primary question type;
- answerability;
- single-document vs multi-document;
- quantitative vs non-quantitative;
- difficulty profile.

For each, report per-arm estimates and denominators. Inferential interaction tests are exploratory unless adequately justified and powered before test. Avoid testing many sparse intersections. Do not interpret a subgroup contrast as confirmed solely because one subgroup p-value is significant and another is not; test interaction if formal subgroup claims are intended.

## 34. Topic-level analysis

Potential PV topics follow Phase 3/4 taxonomy (materials/cells, modules, systems/performance, degradation/reliability, diagnostics, forecasting/resources, emerging technologies, environmental/lifecycle, techno-economic).

Topic analyses are descriptive/exploratory unless the final benchmark has sufficient independent questions per topic and a prespecified interaction analysis. The minimum cell size/precision criterion is **OPEN** and must be set before test analysis using benchmark counts and desired uncertainty, not observed outcomes. Multi-label topic questions may appear in multiple descriptive strata but cannot be treated as independent across inferential tests without modeling overlap.

## 35. Difficulty analysis

Use Phase 4 difficulty descriptors assigned independently of model performance. Do not derive difficulty from retrieval/answer success.

Report performance across the frozen dimensions or an approved derived ordinal difficulty label. If easy/moderate/hard bins are used, thresholds must be set before final test results. Difficulty interaction analyses are secondary/exploratory and require adequate counts; no post-hoc regrouping is allowed.

## 36. Missing-data handling

Every planned question-condition row must have an explicit status:

- valid completed;
- retrieval returned no candidates;
- retrieval returned candidates but no relevant evidence;
- generation failed;
- evaluator/annotation missing;
- excluded due to a documented benchmark/protocol defect;
- technical infrastructure failure pending retry.

Do not silently delete failed observations. Distinguish **true zero performance** from **missing observation**:

- no retrieved relevant evidence after valid execution is a true retrieval outcome;
- no evidence returned is not a missing retrieval score;
- an infrastructure/API failure is a failure status, not automatically a zero retrieval value;
- human scoring unavailable is missing evaluator data pending adjudication, not zero answer quality.

Report missingness by condition, question category, and reason. Complete-case analyses are acceptable only if the missingness is described and justified; no imputation is used unless a method is predeclared and defensible. If missingness differs by arm or is substantial, perform a prespecified sensitivity analysis and qualify inference.

## 37. Retrieval-failure handling

When a valid retrieval run returns no candidates or no relevant evidence:

- Recall@k = 0 for answerable questions;
- MRR reciprocal rank = 0 if no relevant result occurs within evaluated depth;
- nDCG@k = 0 when IDCG is defined and positive but no relevant item is retrieved;
- unanswerable questions are handled separately and do not receive standard relevance metrics.

If the retrieval service/index fails technically, including a retrieval timeout, record an execution failure, retry only under the common frozen retry policy, and do not conflate it with a valid empty result. A valid but empty result remains in the primary intention-to-evaluate dataset.

## 38. Generation-failure handling

Before evaluation, freeze one shared retry policy for API failure/timeouts. Apply identically to all arms. Preserve raw error/timeout logs.

- **Transient API failure/timeout:** apply the same bounded retry/backoff; if unresolved, mark generation failure.
- **Malformed output:** score as output-format failure and no answer; retain raw response.
- **Empty response:** generation failure, not an implicit abstention unless it explicitly communicates evidence insufficiency.
- **Invalid citation format:** answer content may still be scored for correctness/relevance/completeness, but attribution is scored as absent/invalid under the rubric; record format failure.
- **Persistent failure:** include in end-to-end reliability denominator. For primary end-to-end answer/attribution endpoints, count as zero successful answer/attribution credit under an intention-to-evaluate rule and report a separate failure rate. Also provide a successful-run conditional analysis as sensitivity, not replacement.

Exact retry count and timeout values are OPEN and must be frozen before test execution.

## 39. Evaluator agreement

Use Phase 4 annotation and disagreement procedures. Human evaluators score independently and blinded. At minimum, double-score a predeclared proportion or all primary-outcome outputs depending on workload; exact coverage is **OPEN** and must be set before scoring.

Report agreement by outcome type:

- binary labels: raw agreement and an appropriate chance-corrected coefficient (e.g., Cohen's kappa for two raters or Krippendorff's alpha nominal for multiple/missing raters);
- ordinal scales: weighted kappa for two raters or Krippendorff's alpha ordinal;
- claim/evidence spans: claim-alignment agreement and evidence-support agreement using Phase 4 matching rules;
- continuous/numeric scoring: ICC only where its assumptions/design fit; also report absolute agreement and differences.

Do not calculate agreement only after adjudication. Preserve pre-adjudication scores, agreement, disagreements, adjudicator decision, and rationale. Thresholds and exact coefficients depend on final rater design and are OPEN.

## 40. Automated evaluation

Deterministic metrics may be automated only with pinned code, version, and validation tests. If an LLM judge is used:

- pin evaluator model/provider/version and prompt;
- blind arm identity and randomize answer order;
- provide the same rubric and evidence visibility across conditions;
- prohibit access to system identity and retrieval strategy;
- log full evaluator inputs/outputs and decoding settings;
- validate against independently human-scored calibration items;
- report LLM and human-validated results separately;
- measure agreement and analyze disagreement;
- do not treat the LLM judge as unbiased or as ground truth.

Whether LLM evaluation is used, its version, prompt, and acceptance criterion are **OPEN**. Human validation is required before it can support a primary claim. If validation is inadequate, use human scoring for that endpoint.

## 41. Blinding

Human answer and evidence-attribution evaluators receive randomized anonymized system labels (e.g., A/B/C), not BM25/dense/hybrid identities. Remove condition-revealing metadata where feasible while preserving evidence required for scoring. The benchmark/corpus gold annotations are prepared independently of outputs.

Analysts should receive masked condition labels for primary scoring/cleaning where feasible; unmask only after data validation and analysis code is frozen. Complete blinding may be impossible because contexts or output styles reveal a method; record limits.

## 42. Order effects

If evaluators compare multiple system answers for the same question, randomize condition order independently across questions or use a balanced counterbalancing scheme. Do not always show BM25, dense, then hybrid. Evaluators should score each answer against the same rubric/reference independently before comparative preference judgments, if any.

For LLM judges, randomize order and, where pairwise judging is used, counterbalance which system is presented first. Order policy, seed, and presentation format are logged.

## 43. Primary-analysis table

| Outcome | Hierarchy | Scale | Unit | Summary | Primary comparison/test | Effect size | CI | Multiplicity |
|---|---|---|---|---|---|---|---|---|
| Evidence Recall@k at frozen primary cutoff | Co-primary: retrieval | Bounded proportion per question | Question | Mean/SD and median/IQR; paired differences | Three-condition omnibus and all three pairwise matched contrasts per Sections 25–28; no gating | Paired mean/median difference; rank-based effect if applicable | Question-level paired bootstrap | One Holm family of 12 co-primary tests |
| Factual correctness rubric score | Co-primary: answer | Ordinal 0–2 candidate scale | Question | Category frequencies and median/IQR | Friedman omnibus and all three paired contrasts; if dichotomized by frozen rubric, Cochran Q and all three McNemar contrasts | Kendall's W / rank-biserial; binary risk difference | Question-level paired bootstrap or exact interval | Same 12-test co-primary family |
| Claim-attribution completeness | Co-primary: attribution | Bounded proportion per question | Question | Mean/SD, median/IQR, valid denominator | Friedman omnibus and all three paired contrasts | Paired difference; rank-biserial as appropriate | Question-level paired bootstrap | Same 12-test co-primary family |
| MRR | Secondary retrieval | Bounded [0,1] | Question | Mean and median/IQR | Friedman and paired follow-up | Paired difference / rank effect | Question-level paired bootstrap | Holm within predeclared secondary retrieval family if inferential |
| nDCG@k | Secondary retrieval | Bounded [0,1] | Question | Mean and median/IQR | As above; relevance scale reliability required | Paired difference | Question-level paired bootstrap | Same secondary family |
| Relevance | Secondary answer | Ordinal | Question | Category frequencies, median/IQR | Friedman; paired ordinal contrasts | Rank-biserial/Kendall's W | Question bootstrap | Secondary family |
| Completeness | Secondary answer | Bounded proportion | Question | Macro question-level mean/median | Friedman; paired contrasts | Paired difference | Question bootstrap | Secondary family |
| Faithfulness | Secondary answer | Bounded claim proportion aggregated per question | Question | Mean/median and unsupported-claim rates | Friedman/paired method | Paired difference | Question bootstrap | Secondary family |
| Attribution precision | Secondary evidence | Per-question proportion, undefined if no citations | Question | Precision plus citation-absence rate and denominators | Matched analysis on defined cases plus separate absence outcome | Paired difference/risk difference | Question bootstrap; undefined-case rule frozen | Secondary family |
| Correct abstention | Secondary (unanswerable subset) | Binary | Unanswerable question | Rate with denominator and CI | Cochran Q; paired McNemar | Risk difference/matched OR | Paired proportion interval/bootstrap | Holm within abstention family if confirmatory |
| Inappropriate abstention | Secondary (answerable subset) | Binary | Answerable question | Rate and denominator | Cochran Q/McNemar | Risk difference/matched OR | Paired interval | Same abstention family |
| Required-source coverage | Secondary multi-document | Binary/proportion | Question | Complete coverage rate and partial coverage | Cochran Q or Friedman according to score | Risk/mean difference | Paired CI | Secondary family |
| Numerical correctness | Secondary quantitative subset | Binary/ordinal per question | Question | Accuracy and tolerance/condition errors | Cochran Q or Friedman | Risk difference/ordinal effect | Paired CI | Secondary family |
| Retrieval/generation/end-to-end latency | Secondary efficiency | Continuous/skewed | Question-run | Median/IQR; mean/SD also | Paired log/robust model or Friedman per locked rule | Median/mean difference or ratio | Question-level paired bootstrap | Secondary efficiency family |
| Topic/type/difficulty subgroup outcomes | Exploratory | Inherits metric | Question; clustered as needed | Estimates, counts, CIs | Descriptive or prespecified interaction model | Outcome-appropriate | Question/cluster bootstrap | FDR or explicitly descriptive |
| Retrieval-to-answer associations | Exploratory | Correlation | Question within arm | Scatterplots, rho | Spearman by arm or prespecified repeated model | Spearman rho | Question bootstrap | FDR within exploratory family |

If an endpoint's scale or denominator changes before lock, revise this table before final test access and version the plan.

## 44. Analysis workflow

```text
Raw experiment outputs and manifests
        ↓
Integrity/schema validation and condition masking
        ↓
Data cleaning under frozen rules; failures retained with statuses
        ↓
Evaluator scoring, agreement, and adjudication
        ↓
Question-level metric calculation
        ↓
Descriptive statistics and denominator audit
        ↓
Assumption/missingness checks
        ↓
Co-primary omnibus analyses
        ↓
Prespecified pairwise contrasts and multiplicity correction
        ↓
Effect sizes and confidence intervals
        ↓
Secondary analyses
        ↓
Exploratory correlations/subgroups
        ↓
Prespecified sensitivity analyses
        ↓
Unmask conditions and interpret under Section 48
        ↓
Reproducible tables, figures, logs, and deviations
```

The analysis script must produce a flow/accounting table of all expected questions, all three arms, failures, exclusions, and denominators before performance summaries.

## 45. Analysis-plan lock

Before final test execution or access to test labels/results:

1. Resolve all OPEN endpoint, cutoff, scoring, missingness, model, effect-size, confidence-interval, multiplicity, and sensitivity-framework decisions. Freeze the primary/secondary/exploratory hierarchy, statistical tests and fallbacks, effect-size measures, confidence-interval procedure, and missing-data rules.
2. Approve a versioned analysis-plan file with date, authors, frozen corpus/benchmark versions, primary endpoints, contrasts, formulas, tests, fallback rules, multiplicity family, effect-size measures, confidence-interval procedure, missing-data rules, sensitivity framework, and scripts.
3. Commit the plan and code or deposit a timestamped immutable copy; record commit/hash.
4. Keep final test labels/reference annotations access-controlled.
5. Record all subsequent amendments with timestamp, reason, author, and whether results were already visible.

Changes after unblinding are deviations, not retrospective prespecification. They may be reported as exploratory but cannot replace the locked primary analysis. Do not amend because outcomes are unfavorable or inconclusive.

## 46. Sensitivity analysis

Limit sensitivity analyses to credible uncertainty:

1. **Retrieval cutoff:** compare prespecified secondary k values from Phase 2, not a post-hoc best k.
2. **Relevance encoding:** binary versus graded retrieval relevance only if Phase 4 agreement supports both.
3. **Unanswerable questions:** primary answerable-only retrieval metric plus a clearly separate analysis including unanswerable abstention outcomes; do not assign arbitrary zero recall to them.
4. **Generation failures:** intention-to-evaluate zero-credit/reliability analysis versus successful-generation conditional analysis.
5. **Human vs validated automated scoring:** compare only if LLM judge meets predeclared human agreement criteria.
6. **Multi-document items:** compare overall results with single-/multi-document strata descriptively or under prespecified model.
7. **Statistical robustness:** prespecified paired permutation/rank-based result versus selected model-based analysis, not whichever is more significant.
8. **Aggregation:** if a substantive dependency/weighting concern is identified before lock, compare the primary macro question-level summary with one justified alternative aggregation; retain question-level inference and do not treat pooled claims/passages as independent. Otherwise, do not add an alternative aggregation analysis.

Exact values and criteria are OPEN until Phase 2/4 decisions are locked. Do not create an unlimited set of alternative cutoffs, rubrics, or models.

## 47. Robustness analysis

Assess whether conclusions depend on one metric, one category, one evaluator, one k, or a specific analysis assumption using the finite sensitivity set in Section 46. Report when conclusions change, including direction, magnitude, and uncertainty. A robustness analysis does not mean every specification must produce the same p-value.

Do not claim robustness because multiple correlated metrics point in the same direction without acknowledging dependence. Do not manufacture a winner by choosing the specification with the most favorable result.

## 48. Interpretation rules

- Distinguish statistical significance, effect magnitude, uncertainty, and practical importance.
- A p-value below a threshold is not by itself evidence of practical importance.
- Report nonsignificant or inconclusive results as such; do not infer equivalence without a prespecified equivalence/non-inferiority margin and design.
- Do not interpret correlation as causation.
- Do not rank systems with an arbitrary composite score.
- Do not declare a universal winner if outcomes differ across retrieval, correctness, completeness, faithfulness, attribution, or abstention.
- Interpret each metric according to its denominator and subset.
- Qualify results by corpus, benchmark, question mix, and access limitations.
- Do not use unplanned subgroups to support confirmatory claims.

Smallest effect of practical interest, significance threshold, equivalence framework, and any decision rule for “meaningful” differences are **OPEN — requires methodological decision** before final test analysis.

## 49. Result-reporting requirements

For each primary domain report:

- BM25, dense, and hybrid estimates;
- sample/valid-question counts and failure/missing counts;
- absolute pairwise differences;
- outcome-appropriate effect sizes;
- confidence intervals;
- raw and multiplicity-adjusted p-values for prespecified tests;
- descriptive distributions, not means alone where skewed;
- category/subset denominators and analysis coverage;
- assumption checks and deviations.

For secondary/exploratory outcomes, label hierarchy and multiplicity status. Avoid statements such as “Hybrid achieved the highest score” without the numerical estimates, uncertainty, paired comparison, and outcome-specific qualification.

## 50. Reproducibility requirements

Preserve:

- raw per-question/per-arm retrieval results and generation outputs;
- run manifests, failure/retry logs, context IDs/tokens, and corpus/benchmark versions;
- cleaned analysis dataset plus transformation scripts;
- question-level metric calculations and unit tests;
- human annotation data, evaluator IDs/qualification or anonymized metadata, agreement and adjudication;
- LLM evaluator model/version, prompt, settings, inputs, outputs, and validation;
- statistical scripts, environment/package lock, software versions, seeds, and hardware;
- analysis-plan version/hash and all amendments;
- final tables, figures, and machine-readable result exports.

Restricted papers/answers must be handled according to licenses and privacy rules; preserve hashes, locators, and access-controlled references where redistribution is prohibited. Results must be reproducible from versioned inputs without access to mutable unlogged state.

## 51. Bias and validity

| Threat | Relevance | Mitigation | Residual limitation |
|---|---|---|---|
| Pseudoreplication | Treating claims/chunks/citations as independent inflates precision | Aggregate/model at question level; cluster nested data | Question/source clustering may remain |
| Multiple testing | Many endpoints/contrasts inflate false positives | Co-primary hierarchy and Holm; exploratory FDR/labels | Correction reduces power |
| Evaluator bias | Raters may favor known methods or styles | Blind labels, independent scoring, randomized order, rubric | Output/context may reveal arm |
| LLM-judge bias | Model may prefer fluency, verbosity, or familiar evidence | Pin judge, blind, human-validate, report separately | Judge training/behavior remain opaque |
| Benchmark leakage | Test questions/labels may influence tuning | Access control, separate splits, logs, no test tuning | Public facts may be in generator pretraining |
| Selective reporting | Favorable metrics/categories may be emphasized | Locked hierarchy, publish denominator and all planned outcomes | Space constraints may compress reporting |
| Outcome switching | Primary outcome changes after results | Versioned pre-registration-style lock | Protocol amendments may still be necessary for defects |
| Subgroup fishing | Sparse or selected strata yield chance findings | Limit subgroups, predeclare, exploratory/FDR | Small benchmark can limit precision |
| Missing-data bias | Failures may differ by arm/question | Status accounting, intention-to-evaluate, failure-rate reporting, sensitivity | Severe differential failure may limit inference |
| Difficulty imbalance | Performance reflects question mix | Independent multidimensional difficulty, matched questions, report distribution | Difficulty is partly judgment-based |
| Topic imbalance | Common topic dominates aggregate | Report topic counts and coverage; avoid unsupported quotas | Rare areas may be underpowered |
| Metric dependence | Correlated measures can look like replication | Preserve outcome domains and label metrics; no arbitrary composite | Constructs may still overlap |
| Ceiling/floor effects | Scores near bounds reduce sensitivity | Report distributions; use suitable paired models; note limited headroom | Benchmark may not discriminate for some metrics |
| Condition imbalance in exclusions | Arm-specific exclusions bias comparison | Common question set; retain failed outcomes; identical rules | Technical failures may still be differential |
| Rater disagreement | Noisy outcomes attenuate or distort effects | Calibration, reliability, adjudication, preserve raw judgments | Human interpretation remains uncertain |
| Stochastic generation | Run variability may affect paired outcomes | Common settings, repeat plan, retain seeds and runs | API nondeterminism may persist |
| Latency confounding | Cache/hardware/load can dominate timing | Common environment, warm-up, cache policy, decomposition | Provider/network conditions vary |
| Selective denominator | Undefined citations or invalid questions can be hidden | Publish numerator/denominator and undefined/missing counts | Denominator choices must be finalized before lock |

## 52. Decision-status table

| Decision | Status | Evidence/procedure and freeze deadline |
|---|---|---|
| Frozen RQ and retrieval arms | FROZEN | No change |
| Same questions run under all three conditions | FROZEN | Validate matched IDs before analysis |
| Question is primary statistical unit | FROZEN | Nested items aggregate/model under question |
| No chunks/claims/citations as independent `n` | FROZEN | Enforce in data schema and scripts |
| Distinct retrieval/answer/attribution domains | FROZEN | Report separately |
| Three co-primary domains/endpoints | PROVISIONAL | Confirm reliability/feasibility from Phase 2/4; before test access |
| Primary retrieval Recall@k cutoff | OPEN — requires methodological decision | Phase 2 cutoff and benchmark evidence mapping; freeze before test |
| Primary correctness rubric encoding | OPEN — requires methodological decision | Phase 4 calibration and evaluator reliability; freeze before test scoring |
| Attribution completeness denominator/claim policy | OPEN — requires methodological decision | Phase 4 claim/citation annotations; freeze before scoring |
| Binary/graded evidence relevance and nDCG gain | OPEN — requires methodological decision | Inter-rater reliability; freeze before test |
| Exact statistical test per endpoint | PROVISIONAL decision tree | Resolve endpoint scales/missingness; freeze before test access |
| Model-based random-effects structure | OPEN if needed | Benchmark clustering and pilot data structure; freeze before test analysis |
| Holm confirmatory family structure | PROVISIONAL | One Holm procedure across the complete family of three omnibus and nine pairwise tests; no omnibus gate or second incompatible family; approve before test |
| CI confidence level and algorithm/replicates/seed | OPEN — requires methodological decision | Confirm candidate 95% level and select interval method based on locked endpoint and sample structure; question-level resampling is fixed, with cluster-level sensitivity only where shared source/evidence groups induce dependence and enough independent groups exist |
| Practical effect threshold/significance level | OPEN — requires methodological decision | Study purpose/power assumptions; before test access |
| Missing generation failure rule | PROVISIONAL intention-to-evaluate zero credit + reliability report | Confirm retry policy and estimand before test |
| Human rater number/double-score fraction | OPEN — requires methodological decision | Workload, rater structure, Phase 4 agreement; before scoring |
| LLM judge use and validation criteria | OPEN — requires methodological decision | Decide before evaluation; human calibration required |
| Latency repeats/hardware/cache policy | OPEN — requires methodological decision | Freeze before timing runs |
| Exploratory correlation/subgroup models | PROVISIONAL | Register limited set, denominators, multiplicity before test |
| Statistical analysis and scripts lock | FROZEN requirement | Timestamp/hash before final test access |

Each OPEN decision must be recorded with: what is decided; why it matters; evidence required; decision procedure; owner/date; and exact freeze deadline. No OPEN item is resolved by convenience.

## 53. Phase 5 acceptance criteria

Phase 5 is complete only when an independent analyst can determine:

1. the primary, secondary, and exploratory outcomes;
2. metric formulas, denominators, relevance/evidence rules, and subset handling;
3. experimental, observational, statistical, and aggregation units;
4. matched comparisons and test-selection rules by outcome type;
5. assumptions, diagnostics, and predetermined fallbacks;
6. effect sizes, uncertainty intervals, and question-level bootstrap procedure;
7. confirmatory and exploratory multiplicity families;
8. handling of unanswerable questions, failures, invalid outputs, and missing annotations;
9. evaluator blinding, agreement, and automated-judge safeguards;
10. sensitivity analyses and interpretation boundaries;
11. result reporting and reproducibility artifacts;
12. all OPEN decisions and their evidence-based resolution/freeze deadlines.

13. explicit validation that no arm differs on a controlled component except retrieval strategy, or a documented pre-test protocol amendment explaining and addressing any deviation.

No final experiment or final analysis starts until Phase 2/4 dependencies, primary endpoints, metric denominators, statistical tests, multiplicity, effect sizes, confidence intervals, missingness, sensitivity framework, confounder review, and plan hash are approved and locked.

## 54. Phase 6 handoff

Phase 6 receives:

- the frozen RQ and approved Phase 1–4 documents;
- approved corpus and benchmark versions, stable IDs, splits, gold evidence, claims, and annotations;
- resolved Phase 2 retrieval settings, generation controls, and all arm manifests;
- resolved Phase 5 outcome hierarchy, formulas, scoring rubrics, endpoints, test-selection tree, assumptions/fallbacks, multiplicity family, effect sizes, CI method, failure/missingness rules, sensitivity set, and analysis-plan hash;
- evaluator instructions, blinding/randomization plan, agreement/adjudication protocol, and LLM-judge validation decision;
- reproducibility schema, scripts/environment requirements, access restrictions, and deviation/change-log template;
- a checklist of any remaining OPEN decisions, with a hard stop preventing final test execution until resolved.

Phase 6 may design/implement pilot and development components, acquire the corpus, construct the benchmark, implement retrieval arms and evaluation pipeline, and validate integrations only after Phases 1–5 have been reviewed and approved. It must not use final test outcomes to tune methods or alter this locked analysis plan.

### Phase 5 → Phase 6 Handoff

Carry forward the immutable analysis-plan version/hash; primary/secondary/exploratory outcome hierarchy; metric formulas and denominators; question-level matched estimands; statistical-test decision rules and assumption fallbacks; multiple-comparison families; effect sizes and question-level confidence-interval procedure; missing/failure policy; evaluator blinding/agreement procedures; sensitivity and robustness set; reproducibility artifact schema; and unresolved-decision stop list. Phase 6 implements and validates the frozen protocol, but does not make result-driven methodological changes.

## Phase 5 Audit and Amendment Record

- **Audit date:** 2026-10-08.
- **Sections reviewed:** frozen RQ/status and Sections 1–54, with focused checks of Sections 2–5, 19–20, 25–30, 36–46, 49–53, and the Phase 6 handoff.
- **Issues identified:** the confounder rule needed to enumerate the complete set of controlled components and explicitly bar an unamended claim that retrieval strategy was isolated; the confirmatory multiplicity narrative specified a single 12-test Holm family, but the primary-analysis table still described two different Holm families; the omnibus/pairwise wording did not explicitly say whether pairwise tests were gated; analysis-plan lock did not enumerate all requested frozen analysis components; unanswerable-answer outcomes needed explicit non-synonymous definitions; retrieval timeouts and pointwise-vs-simultaneous confidence-interval interpretation needed clarification.
- **Corrections made:** clarified the controlled-components/confounder rule without adding experimental variables; justified one co-primary endpoint per RQ domain; made the three omnibus and nine pairwise tests one ungated 12-hypothesis Holm family throughout the text and table; clarified unsupported vs hallucinated/contradictory answers and retrieval-timeout handling; explained question-level and conditional cluster-level resampling; added the limited, conditional aggregation sensitivity; strengthened the analysis lock and acceptance criteria; clarified that nominal 95% intervals are pointwise unless a family-compatible method is frozen.
- **Decisions that remain OPEN:** primary retrieval cutoff; final relevance representation and nDCG gains; correctness and attribution scoring/rubric calibration; exact endpoint test/fallback where measurement choices remain provisional; confirmatory error threshold and practical effect threshold; power/precision target and assumptions; confidence level and interval implementation/replicates/seed; any source-cluster model if supported by the final data structure; retry/timeouts and failure estimand details; rater design/agreement thresholds; LLM-judge use and validation criterion; latency protocol; final secondary/exploratory testing families and subgroup precision requirements.
- **Decisions that are now FROZEN:** the research question is unchanged; BM25, dense, and hybrid remain the only primary retrieval arms; retrieval strategy remains the principal manipulated variable; the same corpus/documents, preprocessing/chunking, benchmark/questions/evidence annotations, context controls, generator/prompt/generation settings, and evaluation conditions are required across arms; the question remains the matched primary inferential/resampling unit; nested passages, documents, citations, claims, and answer sentences are not independent observations; retrieval, answer quality, and evidence attribution remain distinct outcome domains; no arbitrary composite winner score is used.
- **Experiment/results confirmation:** no experiment was run, no system outputs or final performance results were inspected, and no result-driven plan change was made.
