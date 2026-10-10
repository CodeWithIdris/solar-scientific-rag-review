# Phase 4 — Solar-PV Scientific Question Benchmark and Evidence Annotation Protocol

## Status and scope

**Phase status:** benchmark design protocol only. No final question set is constructed or collected here, no final test benchmark is opened, and no final retrieval or QA experiment is run.

**Frozen research question (must remain unchanged):**

> How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?

Decision-status labels:

- **FROZEN:** fixed by the research question or prior approved phase.
- **PROVISIONAL:** recommended policy, not final until explicitly approved and logged.
- **OPEN — requires methodological decision:** unresolved; the protocol identifies what evidence and procedure are needed.
- **DEFERRED:** assigned to a named later phase.

Phase 4 defines the benchmark-to-corpus interface and annotation/evaluation-ready references. It must not use retrieval performance to design or revise the final test questions. The benchmark is paired: every test question is evaluated by BM25, dense, and hybrid retrieval under the same Phase 1/2 controls and the same Phase 3 corpus version.

## 1. Phase 4 objective

Design an auditable benchmark that independently establishes for each question:

- the question text and its validity;
- its topic, question type, and difficulty descriptors;
- whether it is answerable from the frozen corpus;
- the evidence sufficient to answer it, including alternate valid evidence;
- a scientifically faithful reference answer and required claims;
- numerical conditions/tolerances where applicable;
- scoring interfaces for retrieval, answer quality, attribution, and abstention.

The benchmark must support matched question-level and category-level comparison among the three retrieval strategies without preferring any method.

## 2. Benchmark purpose

The benchmark measures how retrieval strategy affects:

1. retrieval of relevant evidence;
2. downstream answer correctness, relevance, and completeness;
3. support and attribution of generated claims to retrieved corpus evidence;
4. appropriate uncertainty/abstention when corpus evidence is insufficient.

These outcomes are not interchangeable. Finding a gold passage does not prove that an answer is correct; a factually correct answer does not prove that it is supported by the retrieved context; a citation identifier does not prove that the cited passage supports the claim.

## 3. Relationship to Phases 1–3

- **Phase 1:** retrieval strategy remains the principal manipulated variable; corpus, benchmark, preprocessing, chunking, generator, prompt, context budget, and evaluation conditions are shared.
- **Phase 2:** the retrieval architecture and common context/generation interface are specified; all technical settings remain subject to their recorded FROZEN/PROVISIONAL/OPEN status.
- **Phase 3:** the corpus policy is defined, but corpus collection/freeze may still be pending. Phase 4 must use the approved immutable corpus version once available. It must not silently broaden or alter corpus scope.

If an intended benchmark question cannot be grounded in the approved corpus, do not add a document informally. Mark the question unsupported/invalid for this benchmark or request a documented corpus amendment that creates a new corpus version and triggers a protocol impact review.

## 4. Benchmark unit

The primary benchmark unit is **one scientific question**, with a stable question identifier such as `SPV-Q0001`. Do not use document IDs as question IDs. One document may support multiple questions; a question may require evidence from multiple documents.

Every question has one final adjudicated annotation record and is run under all three retrieval conditions. If a question contains separable subparts, either annotate the subclaims explicitly within one question record or split it into independently answerable question units before test freeze; the rule is **OPEN** and must be applied consistently.

## 5. Question taxonomy

Question types are multi-label where needed: assign one primary type and optional secondary tags. “Multi-document” is an evidence-structure tag that may co-occur with factual, comparative, causal, methodological, or quantitative types. “Unanswerable” is an answerability label, not a semantic question type.

| Type | Purpose and characteristics | Include when | Exclude when | Structural pattern | Evidence requirement / difficulty / evaluation considerations |
|---|---|---|---|---|---|
| Factual retrieval | Retrieve a specific scientific fact, material, condition, observation, or finding | Fact is scientifically meaningful and grounded in the corpus | Answer is trivial metadata only, ambiguous, or requires unsupported inference | “Under [specified condition], what [material/observation/outcome] did the study report?” | Usually one or a few evidence units; difficulty depends on lexicality, dispersion, terminology, and conditions; score fact accuracy and retrieval |
| Comparative | Compare technologies, materials, methods, conditions, studies, or outcomes | Both/all sides and comparison basis are explicitly supported | One side lacks evidence or comparison criterion is underspecified | “How did [A] and [B] differ in [outcome] under [conditions]?” | Requires evidence for each side and the comparison dimension; score each side and synthesis; may be multi-document |
| Causal/explanatory | Explain a mechanism, relationship, or reason stated by the source | Source evidence supports the strength of the explanation requested | Question presupposes causality where only association/speculation is reported | “What mechanism did the authors propose for [observation]?” | Evidence must distinguish demonstrated mechanism, proposed mechanism, association, and hypothesis; penalize overstated causal claims |
| Methodological | Retrieve study design, measurement, dataset, algorithm, evaluation, or laboratory condition | Details can be checked against source methods | Answer depends on unreported procedure or external assumptions | “How was [quantity/system] measured or evaluated?” | Usually methods/table evidence; score procedural details and conditions separately |
| Quantitative/numerical | Retrieve numerical value(s), units, and conditions | Number is stated or derivable by a predeclared transparent calculation | Value lacks condition/unit or requires undocumented conversion | “What [metric] was reported at [condition]?” | Store value, unit, condition, rounding/tolerance and source; score number+unit+condition, not number alone |
| Multi-document synthesis | Combine evidence across distinct papers rather than merely retrieve one passage | No single source document contains a sufficient complete answer under the protocol | One paper alone fully answers the question, making multi-document status cosmetic | “Across studies [specified relation], what common/differing findings were reported?” | Annotate required evidence from each required source and synthesis relationship; score partial source coverage separately |
| Unanswerable/insufficient evidence | Test calibrated refusal/uncertainty when the frozen corpus does not support the requested answer | The question is clear and valid but evidence is absent, insufficient, or does not resolve its premise | Ambiguous, malformed, or invalid question; those are excluded, not scored as unanswerable | “What [specific result] did the corpus establish?” where no eligible corpus evidence supports it | Annotate why unsupported and what search scope was checked; score abstention, uncertainty, and unsupported assertions |

Equal category allocation is **not required** and may distort the corpus/topic distribution. Category proportions must be justified from the study purpose, corpus support, annotation feasibility, and inferential needs; all categories intended for claims must have adequate coverage. Exact allocation is OPEN.

## 6. Factual-question protocol

Questions request specific findings, materials, operating conditions, measured effects, or scientific observations. Avoid questions answerable solely from title, author, venue, DOI, or publication year unless bibliographic retrieval is explicitly brought into scope by a protocol amendment.

The question must identify conditions needed to disambiguate the fact (e.g., device architecture or test condition) without copying the full evidence wording. The reference record identifies all valid evidence units and required answer elements. A single canonical wording is not required if scientifically equivalent formulations are accepted.

## 7. Comparative-question protocol

Specify comparison entities and comparison dimension. A question comparing two technologies, studies, or conditions must:

- identify each comparison side without retrieval-method-specific hints;
- identify the outcome or criterion to compare;
- specify relevant operating, experimental, or measurement conditions;
- have sufficient evidence for every side;
- distinguish differences in study setup from differences in the scientific property.

Mark as multi-document only if evidence from at least two distinct source documents is necessary for a complete answer. If a single source gives the complete comparison, it is not a multi-document item even if the question names two technologies.

## 8. Causal/explanatory-question protocol

Question wording must match the evidential strength:

- **demonstrated causal mechanism:** source provides appropriate evidence for causation;
- **proposed mechanism:** authors propose an explanation, not necessarily demonstrate it;
- **observed association:** variables co-vary, but causation is not established;
- **hypothesis:** explanation is explicitly conjectural.

Annotate the claim status and source language in the reference record. Do not reward answers that turn association into causation or a proposal into a demonstrated fact. Reject questions whose premise presupposes a mechanism not supported by the corpus.

## 9. Methodological-question protocol

Questions may address experimental design, measurement apparatus/procedure, simulation assumptions, datasets, algorithms, baselines, evaluation metrics, sample conditions, or laboratory settings. Reference annotations should capture the specific methodological element(s) requested and distinguish reported methods from interpretation. A method question must be answerable from the retained version and source locators.

## 10. Quantitative-question protocol

For every quantitative item, record:

- expected value(s) or acceptable value set;
- unit and any dimensional conversion;
- technology/sample/condition to which the number applies;
- measurement or calculation context;
- original precision and displayed precision;
- allowed rounding/tolerance and rationale;
- source evidence and locator;
- whether equivalent conversions are accepted.

Do not award full credit for a numerically similar result attached to the wrong cell type, temperature, irradiance, sample, baseline, time period, or metric definition. Tolerance policy is **OPEN** until the numeric annotation protocol is approved; it must not be selected after seeing system outputs.

## 11. Multi-document-question protocol

A question is genuinely multi-document only if its complete reference answer requires evidence from at least two distinct canonical `document_id`s. For each item record:

- required source documents;
- at least one sufficient evidence unit per required source;
- the role each source plays;
- the relation/synthesis operation (agreement, contrast, trend, boundary, or explanation);
- minimum source coverage for a complete answer;
- whether alternative eligible documents can substitute for a named source.

Questions should normally ask about findings rather than require knowledge that one paper cites another. The evidence must support the synthesis, not just the fact that sources discuss the same topic. Partial retrieval of only one necessary source cannot earn full retrieval or answer-completeness credit.

## 12. Unanswerable-question protocol

Distinguish these statuses:

1. **Answerable from corpus:** sufficient, non-contradictory or appropriately qualified evidence is present.
2. **Answerable in principle but unsupported by this corpus:** the question is meaningful, but eligible corpus evidence does not establish the requested information.
3. **Insufficient/indeterminate evidence:** evidence exists but is incomplete, conflicting without resolution, or does not support the requested level of certainty.
4. **Invalid question:** ambiguous, malformed, false-premised, out of scope, or not independently evaluable; exclude from final test and retain in the exclusion log.

For statuses 2 and 3, annotators must document the search/coverage basis used to determine insufficiency, including candidate corpus sections/documents reviewed, and why available evidence cannot answer the question. An unanswerable question must not merely be difficult or absent from one annotator's first search.

Whether status 2 and status 3 are combined or analyzed separately is OPEN. Preserve the distinction in the raw annotations even if later analysis groups them.

## 13. Abstention protocol

A correct abstention:

- clearly indicates that the supplied corpus evidence is insufficient to answer the specific question;
- does not assert unsupported factual content as if established;
- identifies uncertainty or the missing evidence dimension when useful;
- may report supported partial information while clearly labeling what remains unresolved.

A generic “I don't know” is not automatically correct. It receives credit only if it communicates evidence insufficiency for a question annotated as unanswerable/insufficient. On answerable items, generic refusal is an incorrect abstention. For partially answerable items, score supported claims and unsupported requested claims separately.

The exact response categories and scoring aggregation are **OPEN** for Phase 5. Phase 4 supplies gold answerability, rationale, and required/forbidden claims to enable that scoring.

## 14. Question-construction protocol

Construct questions from the frozen corpus and scientifically meaningful information needs, not from retrieval outputs.

1. **Corpus readiness:** use only the approved corpus version and stable text locators.
2. **Candidate evidence selection:** an annotator identifies a scientifically meaningful finding/method/comparison and records its source before drafting the question.
3. **Drafting:** write a natural information need without copying distinctive evidence phrases solely to help lexical retrieval or paraphrasing solely to help dense retrieval.
4. **Independent answerability and evidence check:** a second annotator, without retrieval-system outputs, attempts to verify answerability and identify sufficient evidence.
5. **Reference construction:** define required claims, accepted alternatives, conditions, numerical rules, and evidence roles.
6. **Validation:** independently assess scientific validity, question clarity, evidence sufficiency, method neutrality, and answerability.
7. **Pilot:** use only designated development items for pipeline checks; no final retrieval results may revise final test items.
8. **Freeze:** version questions, evidence, answers, annotations, and split assignments; compute hashes; seal final test labels/evidence.

Questions can be sourced from prose, methods, tables, or faithful text/caption representations included in the corpus. No benchmark question is accepted solely because a model or LLM generated it.

## 15. Difficulty framework

Do not define difficulty from system performance. Record a multidimensional profile for each question:

- lexical overlap between question and sufficient gold evidence;
- number of required evidence units;
- number of required source documents;
- reasoning/synthesis operation;
- numerical complexity (none, direct value, unit conversion, multi-step calculation);
- terminology complexity;
- evidence dispersion across the document(s);
- condition specificity and potential ambiguity.

Prefer retaining these dimensions as ordinal/continuous descriptors. A summary label such as Easy/Moderate/Hard may be derived only after a prespecified rubric is established and validated by annotators; it must not replace the component profile. Exact scales, thresholds, and composite rule are **OPEN**.

Difficulty rating should be assigned independently of retrieval/generation results by annotators using the documented rubric. If no reliable ordinal threshold scheme is justified, report multidimensional descriptors without a single overall label.

## 16. Gold-evidence protocol

For every answerable question, identify evidence independently of retrieval runs. Evidence can be one or more passages from one or multiple documents, or faithful text units derived from a table/caption under the Phase 3 corpus policy.

Each evidence record must include at minimum:

```text
evidence_id
document_id
version_id
chunk_id (when shared chunks exist)
page
section_path
start/end offsets or equivalent locator
source-faithful evidence_text or secure reference to it
evidence_role
relevance_grade
required/optional/contradictory status
annotation rationale
annotator/adjudication provenance
corpus_version
```

Gold evidence is not limited to one passage. Annotators should identify the minimum sufficient set and known alternative sufficient units/sets. Retrieval results must not be used to discover, expand, or prune final gold evidence. If an evidence annotation is revised after system evaluation begins, create a new benchmark version and disclose the timing and reason.

## 17. Evidence-role framework

Use a compact, multi-label role vocabulary only where it improves scoring:

- `primary_support`: directly supports a required answer claim;
- `secondary_support`: corroborates or qualifies a required claim;
- `context`: helps interpret the result or condition but is not sufficient alone;
- `numerical`: supplies a required value/unit/condition;
- `method`: supports a method/procedure claim;
- `comparative`: supports one side or relation in a comparison;
- `contradictory`: provides credible conflicting evidence;
- `background`: relevant context not required for the answer.

The evidence role is distinct from relevance grade and from whether it is required. To avoid unnecessary complexity, role labels are assigned only when needed for the question's scoring; use `primary_support` and `context` as the minimum core, adding labels for quantitative, methodological, comparative, or contradictory roles where applicable. Final vocabulary and whether all labels are required are **OPEN**.

## 18. Evidence-completeness protocol

For each question, annotate:

- **required evidence:** evidence needed to support every required claim;
- **sufficient evidence set(s):** one or more combinations that together support a complete answer;
- **optional support:** valid corroboration or qualification that is not required;
- **contradictory evidence:** eligible corpus evidence that conflicts or qualifies the result;
- **minimum source coverage:** especially for multi-document items;
- **alternative evidence:** passages that independently support the same required claim.

Do not assume one gold passage per claim or question. A question can have multiple sufficient evidence sets. Represent set logic explicitly where possible (e.g., evidence A **and** either evidence B1 or B2). Completeness is judged against the required claims/evidence structure, not exact text overlap alone.

## 19. Reference-answer protocol

Reference answers must be:

- scientifically accurate and faithful to the retained sources;
- directly supported by cited gold evidence;
- scoped to the question and relevant conditions;
- explicit about uncertainty, disagreements, and causal strength;
- tolerant of scientifically equivalent wording;
- clear about what the corpus does and does not establish.

Use a structured reference answer rather than one canonical sentence for open-ended or synthesis items. Record a concise reference synthesis, required claims, acceptable alternative formulations, values/units/conditions, caveats, and gold evidence links. Do not penalize stylistic differences that preserve the supported meaning. Do penalize invented details, omitted required claims, incorrect conditions, and overstatement.

## 20. Required-claim framework

Complex answers are annotated as atomic claims with:

```text
claim_id
claim_text/semantic proposition
requiredness (required, optional, caveat)
condition/scope
supporting evidence IDs or sufficient evidence-set logic
acceptable alternatives
contradiction/caveat notes
claim-level correctness criteria
```

The minimum complete answer is the set of required claims plus required conditions/caveats. Claim granularity should be sufficient to separately judge factual correctness and evidence support without fragmenting prose into trivial units. Claim segmentation guidance and adjudication rules are **OPEN**.

## 21. Expert-validation protocol

### 21.1 Expertise definition

Validators collectively need:

- demonstrated solar-PV subject expertise relevant to the questions (e.g., PV materials/devices, modules/systems, performance/reliability, forecasting/diagnostics, or directly related analysis); and
- competence to assess scientific evidence and the methods/claim strength in the source literature.

At least one validator for each item must be able to assess its substantive PV topic. A second validator should independently assess evidence and answer adequacy. A research-methodology/information-retrieval specialist may validate benchmark design and evaluation interfaces but does not substitute for PV-domain validation.

### 21.2 Number, independence, and conflicts

Use at least two independent judgments for critical fields (question validity, answerability, evidence sufficiency, reference answer) before adjudication. Exact total number of validators, qualifications threshold, allocation across topic areas, and whether a third adjudicator is required are **OPEN** and must be set based on benchmark size, topic breadth, and available expertise before annotation starts.

Collect relevant expertise declarations and conflicts (e.g., authorship, financial/organizational interest, strong involvement in a particular technology). Reassign or disclose conflicts; do not silently waive them. Validators first work independently and do not see retrieval-arm outputs or one another's judgments.

## 22. Annotation protocol

For each candidate question:

1. **Draft:** author records source and scientific information need.
2. **Validity screen:** independent reviewer checks scope, clarity, and method neutrality.
3. **Answerability:** annotators classify answerable, corpus-unsupported, insufficient/indeterminate, or invalid with rationale.
4. **Evidence annotation:** annotators independently identify required and alternative evidence units and locators.
5. **Reference answer:** create a scoped synthesis with required claims, conditions, caveats, and evidence.
6. **Question type/difficulty:** assign primary/secondary taxonomy and independent difficulty dimensions.
7. **Independent validation:** qualified reviewers assess validity, answerability, evidence sufficiency/completeness, answer fidelity, and numerical rules.
8. **Agreement and adjudication:** calculate field-appropriate reliability before adjudication; record disagreements and resolution.
9. **QC:** automated and manual checks; remove invalid questions only before final test freeze and log reason.
10. **Split and freeze:** assign development/test under the prespecified grouping/stratification rule, freeze version and hashes, and restrict test annotations.

No annotator sees which retrieval strategy found or missed the evidence during benchmark construction. Any post-freeze annotation change requires a new benchmark version and audit record.

## 23. Inter-rater agreement

Agreement is calculated on independent annotations before adjudication. Do not report one statistic for every field.

| Annotation field | Data type | Candidate agreement measure | Notes |
|---|---|---|---|
| Validity / answerability / primary question type | Nominal categorical | Krippendorff's alpha nominal for multiple raters or missing data; Cohen's kappa only for exactly two raters and suitable design; report raw agreement and category prevalence | Preserve detailed answerability statuses; sparse categories can destabilize chance-corrected coefficients |
| Ordinal difficulty or evidence relevance grades | Ordinal | Krippendorff's alpha ordinal or weighted kappa for two raters; report confusion matrix | Specify weights before annotation |
| Required claims | Structured/multi-label | Per-claim agreement after claim alignment; report precision/recall/F1 or Jaccard/overlap with adjudication; use alpha only if a defensible unitization scheme is defined | Claim segmentation itself requires agreement guidance |
| Evidence spans | Span/set agreement | Span-overlap precision/recall/F1 or intersection-over-union at a prespecified matching rule; additionally assess agreement on support sufficiency | Exact string equality is too strict for equivalent spans; threshold OPEN |
| Numerical values/tolerances | Mixed numeric/nominal | Agreement on value/unit/condition; ICC only for repeated continuous ratings with suitable assumptions; exact/within-tolerance agreement for numerical annotations | Do not use ICC for categorical units or status labels |
| Reference-answer adequacy | Ordinal rating plus qualitative rationale | Weighted ordinal agreement or alpha ordinal; report criterion-level disagreement | Define rubric and anchors first |

The specific coefficients, confidence intervals, matching thresholds, and minimum acceptable agreement are **OPEN — requires methodological decision.** Select based on rater count, data type, missingness, prevalence, and annotation structure; justify before final annotation. Low agreement triggers rubric clarification and calibration on development/draft items, followed by re-annotation where needed. Do not use post-adjudication agreement as if it were independent reliability.

## 24. Disagreement resolution

Maintain the sequence:

```text
Independent annotations
        ↓
Pre-adjudication agreement calculation
        ↓
Disagreement log and evidence review
        ↓
Adjudication by agreed qualified reviewer(s)
        ↓
Final annotation with rationale
```

Never overwrite an annotation silently. Preserve each initial label/span/answer, annotator ID, timestamp, disagreement type, adjudicator, evidence consulted, final decision, and rationale. If disagreement reveals ambiguity or inadequate corpus evidence, revise or exclude the question before test freeze; do not force consensus by assertion.

## 25. Question-validity checklist

A question enters the benchmark only if reviewers can answer “yes” to all applicable checks:

- Scientifically meaningful and within solar-PV scope?
- Clear, grammatical, specific, and independently interpretable?
- Does not contain a false or unsupported premise?
- Answerable from the frozen corpus when labeled answerable?
- For unanswerable items, is the question valid but genuinely unsupported/insufficient in that corpus?
- Gold evidence and source locators are sufficient and traceable?
- Reference answer is accurate, scoped, and faithful to evidential strength?
- Required claims and any numerical conditions are explicit?
- Category and answerability labels match the question?
- Does not depend solely on title/author/venue metadata outside scope?
- Not duplicated or near-duplicated with another benchmark question?
- Not worded to target BM25, dense, or hybrid retrieval?
- Does not reveal the expected answer or evidence in a way that invalidates evaluation?
- Can be scored using predeclared criteria without relying on evaluator intuition alone?

Any “no” requires revision and re-review or exclusion with a logged reason.

## 26. Retrieval-method neutrality audit

### 26.1 Principles

Do not deliberately repeat distinctive gold-evidence phrases to favor BM25, and do not deliberately paraphrase terminology to favor dense retrieval. Do not add artificial terms to favor hybrid retrieval. Questions should express realistic scientific information needs.

Natural lexical overlap is not grounds for removal. It is a benchmark characteristic to measure and report.

### 26.2 Audit procedure

For each question, compute descriptive lexical overlap with all sufficient gold evidence using a documented tokenization/measure that is independent of BM25 tuning. Also record exact distinctive phrase overlap and semantic paraphrase judgments where feasible. The statistic is descriptive, not an automatic inclusion threshold.

A reviewer who did not draft the question checks whether wording is natural and not derived by copying or adversarial rewriting. If suspicious overlap exists, ask the author to justify the wording against a realistic user need; revise only before test freeze and without viewing retrieval outcomes.

Overlap metric/tokenization, thresholds for manual review, and semantic audit process are **OPEN**. Freeze them before the neutrality audit. Do not remove a naturally occurring overlap solely because it appears to benefit a method.

## 27. Benchmark leakage controls

- Separate development and final-test question IDs, annotations, and gold evidence.
- Allow development questions for retrieval/model/chunking/fusion/prompt tuning only under the Phase 2 protocol.
- Do not allow final test question text, gold answers, evidence labels, or test metrics to inform system selection, tuning, or benchmark edits.
- Restrict access to final test annotations and keep an access log.
- Deduplicate question paraphrases and group related questions to avoid split leakage.
- Record whether question authors/annotators have seen benchmark candidates or system outputs.
- Do not use LLM-generated questions as accepted items without human source verification and independent validation.
- After benchmark freeze, any change creates a new version with reason, timestamp, changed IDs, and impact analysis.
- Do not remove difficult test items or replace them after observing system results.

Generator pretraining may have exposed public source papers or similar questions; this cannot be claimed fully eliminated. Record model/version and known exposure uncertainty. Controllable label, prompt, tuning, and result leakage must still be prevented.

## 28. Development/test split

### 28.1 Split structure

The benchmark requires at least:

- **Development set:** accessible for pipeline debugging, parameter/model selection, prompt development, and metric validation under the approved protocol.
- **Final test set:** held out from tuning; used once under the frozen protocol, with all three retrieval arms evaluated on every test question.

A separate validation set is optional and **OPEN**. It may be justified if model selection and final development decisions need distinct data, but it increases annotation burden and reduces items per split.

### 28.2 Grouping and stratification

Do not split near-duplicate questions or questions sharing the same core evidence/answer template across development and test without assessment. Group by underlying question family and, where feasible, source-paper/evidence clusters. Multi-document questions create connected groups; specify how overlapping source sets are assigned to prevent leakage without making the split infeasible.

Stratify or constrained-randomize on primary question type, answerability, difficulty profile, single-/multi-document status, and major PV topic so no category is concentrated in one split. Do not force exact equal percentages. Use a recorded random seed and preserve split membership.

Split proportions, grouping granularity, validation-set need, and stratification algorithm are **OPEN**. Resolve before question annotation is exposed for tuning; freeze before any retrieval/model optimization. Use pilot estimates of question counts and group structure, not system test performance.

## 29. Topic-balance strategy

Use the Phase 3 topic taxonomy and allow multi-label topics:

- PV materials/cells/devices;
- modules;
- systems/design/operation;
- performance/efficiency;
- degradation/reliability;
- diagnostics/fault detection;
- forecasting/resource assessment;
- manufacturing;
- emerging PV technologies;
- environmental/lifecycle;
- techno-economic PV research.

Report question counts by primary and secondary topic, question type, answerability, difficulty dimensions, and source documents. Do not impose equal quotas unsupported by corpus coverage. If a topic has insufficient eligible evidence/questions, report it as undercovered and limit interpretation; do not invent questions or add papers after seeing retrieval performance.

Topic annotation guide, minimum coverage targets (if any), and treatment of multi-topic questions are **OPEN**. Set based on the frozen corpus profile and study scope, before test freeze.

## 30. Benchmark-size/sample-size rationale

Do not automatically use a round-number target such as 200. Benchmark size is determined by:

- paired design: each question contributes results for all three arms;
- anticipated outcome variability and smallest effect of practical interest;
- primary contrasts and multiple outcome families;
- question/source-paper clustering and effective sample size;
- desired coverage of types, answerability, and topics;
- reliability of annotation and expert-validation workload;
- availability of sufficient gold evidence and multi-document cases;
- expected missing/invalid item rate;
- multiple-comparison and subgroup-reporting plan.

If a defensible formal power calculation can be made, it requires a prespecified primary outcome/contrast, target effect, variance or paired discordance estimate, type-I error/multiplicity plan, desired power, and clustering assumptions. Those inputs are not established in Phase 4; do not fabricate them.

If pilot data are needed, use a separately labeled development pilot to estimate annotation workload, agreement, question-family prevalence, paired outcome variance only if an approved non-final retrieval pilot is authorized, and missingness. Pilot items/results do not enter the final test unless the protocol explicitly permits and preserves that separation. Final size, pilot inclusion rule, power assumptions, and stopping rule remain **OPEN — requires methodological decision** and must be settled before final test collection/freeze.

## 31. Statistical compatibility

The benchmark must support matched observations:

- each final test question is run under BM25, dense, and hybrid;
- per-question outputs and annotations are retained;
- each score can be mapped to `question_id`, condition, and benchmark version;
- category/subgroup labels are fixed before test evaluation;
- multiple claims/evidence units are linked to parent questions to support clustered analysis.

The estimand, primary outcomes, paired statistical model, treatment of clustered questions, confidence intervals, effect sizes, multiplicity correction, and formal power analysis are **DEFERRED to Phase 5**. Phase 4 must not present a complete statistical analysis plan. It supplies the data structure and paired design needed by Phase 5.

## 32. Retrieval-evaluation interface

For answerable questions, define evidence relevance independently of system results. Each candidate gold evidence unit or sufficient evidence set receives:

- binary relevance for whether it supports any required claim; and, where reliable, a graded relevance level;
- required/optional/context/contradictory status;
- claim and source links;
- alternative-sufficient-set logic.

### Candidate graded scale — OPEN

A possible scale for Phase 5 consideration:

- `0`: not relevant or does not support the question;
- `1`: contextual/background only;
- `2`: partially supports a required claim or one component;
- `3`: directly supports a required claim or is part of a sufficient evidence set.

This scale is not frozen. Relevance grades must be defined so that alternatives and multi-document evidence are scored consistently. Binary scoring may be preferable if annotators cannot reliably distinguish grades.

The benchmark annotation schema supports Recall@k, MRR, and nDCG@k by linking retrieved shared chunk IDs to gold evidence. Metric formulas, k cutoffs, gain mapping, treatment of multiple sufficient evidence sets, and whether chunk- or document-level retrieval is primary are **DEFERRED/OPEN for Phase 5**. Preserve enough annotation detail to calculate both binary and graded variants without re-annotating.

## 33. Answer-evaluation interface

For every generated answer, preserve per-question scores for separate dimensions:

- **Factual correctness:** whether stated claims agree with corpus-supported scientific facts and conditions.
- **Relevance:** whether the response answers the question and avoids irrelevant material.
- **Completeness:** whether all required claims, comparisons, values, conditions, and caveats are present.
- **Faithfulness/support:** whether claims are entailed or adequately supported by the supplied retrieved context, not merely present somewhere in the corpus.

Use the required-claim table and structured reference answer to score each dimension. Do not collapse dimensions into one score unless Phase 5 justifies a composite, defines its weighting, and reports component scores separately. Metric choice, automation/human mix, rubric anchors, and aggregation are **DEFERRED to Phase 5**.

## 34. Evidence-attribution interface

Attribution should be annotated at **claim level** for complex answers, with answer-level summaries derived from claim/citation records. Preserve:

- generated claim ID/text;
- required/reference claim mapping;
- generated evidence/citation identifiers;
- cited corpus chunk/document/span;
- whether the cited evidence supports the claim fully, partially, not at all, or contradicts it;
- whether a correct claim has no attribution;
- whether the attribution points to the wrong source or condition.

Definitions:

- **Supported claim:** cited retrieved evidence directly supports the stated claim at the claimed scope/strength.
- **Partially supported claim:** evidence supports only part of the claim, omits a condition, or is weaker than the assertion.
- **Unsupported claim:** no supplied evidence supports the claim.
- **Incorrect attribution:** cited evidence is irrelevant, misquoted, attached to the wrong claim, or supports a materially different condition/result.

The Phase 5 evaluation design should be able to derive citation/evidence precision and completeness/recall, but exact denominator definitions, handling of uncited claims, claims with multiple valid citations, and aggregation are **DEFERRED**. Evidence-passage retrieval is not the same construct as answer-claim attribution.

## 35. Contradictory-evidence policy

Scientific disagreement is not automatically an annotation error. For each question where eligible documents conflict:

- annotate each relevant finding with its source, date/version, sample, technology, conditions, metric definition, and evidential strength;
- determine whether findings are genuinely comparable or differ because of conditions/methods;
- preserve unresolved disagreement in the reference answer;
- state conditions and avoid a forced single consensus answer;
- include contradictory evidence as a tagged evidence role where relevant;
- score whether generated answers acknowledge material disagreement and avoid cherry-picking.

If disagreement cannot be summarized without substantial unsupported interpretation, revise the question or classify it as indeterminate/insufficient. Adjudication rules and whether particular contradiction types are included in the primary benchmark are **OPEN**.

## 36. Numerical-evaluation policy

A numerical item is fully correct only when value, unit, condition, and metric identity are correct. Store original reported number and precision; distinguish direct reported values from derived values and document any allowed conversion.

Tolerance hierarchy:

1. **Exact categorical/unit/condition match:** required unless an approved conversion is allowed.
2. **Rounding tolerance:** based on source precision and a documented rounding rule.
3. **Scientific range/tolerance:** allowed only when supported by measurement uncertainty, source-reported interval, or a predeclared domain/methodological justification.

Do not select a universal percentage tolerance by convenience. If the source provides uncertainty or range, retain it. If no justified tolerance can be established, use exact value to stated precision after allowed rounding, or exclude the item if scoring cannot be reliable. Phase 5 final scoring implementation is deferred; tolerance rules per item must be frozen before test responses are scored.

## 37. Multi-document evidence policy

For every multi-document question:

- specify the minimum number of distinct source documents required for a complete answer (at least two);
- annotate sufficient evidence from every required source;
- identify the relationship or synthesis operation;
- define which required claims depend on each source;
- list substitutable valid sources/evidence sets if more than one source combination is acceptable;
- identify whether all required sources must be attributed in a complete answer.

Score retrieved-source coverage and synthesized-answer completeness separately. If only some necessary sources are retrieved, award partial rather than full credit according to the claim/evidence mapping. Do not let one paper that happens to summarize the others count as multi-document unless the question truly requires cross-source evidence and the protocol explicitly treats that synthesis document as sufficient.

## 38. Unanswerable evaluation

For unanswerable/insufficient questions, expected outcomes are annotated as:

1. correct, specific abstention;
2. appropriate partial answer with explicit unresolved portion;
3. vague uncertainty without clear recognition of missing evidence;
4. unsupported asserted answer;
5. contradictory answer;
6. fabricated citation/evidence.

Credit is given to outcome 1 when the item is genuinely unanswerable and to outcome 2 only when supported partial information is present and uncertainty is clear. Generic refusal is not full credit on answerable items. Unsupported claims or fabricated evidence receive no support/attribution credit and are separately flagged. Exact scoring and whether statuses 2/3 are analyzed together are **DEFERRED to Phase 5**, with item-level answerability rationale preserved here.

## 39. Benchmark quality control

### Automated checks

- exact and near-duplicate question detection;
- question-ID uniqueness and schema validation;
- missing/invalid document, version, chunk, evidence, or question IDs;
- source/corpus version consistency;
- missing reference answers or required claims for answerable questions;
- answerability/reference contradictions;
- malformed numeric values, units, conditions, and tolerances;
- duplicate evidence records and invalid locators;
- question/evidence lexical overlap statistics and flagged distinctive phrase matches;
- answer leakage in question text, metadata, or examples;
- split leakage across duplicate questions, source/evidence groups, and paraphrase clusters;
- inconsistent taxonomy/status labels;
- detection of exact copied evidence text in question wording.

### Manual checks

- scientific relevance and solar-PV scope;
- clarity, premise validity, and independent evaluability;
- answerability and evidence sufficiency/completeness;
- reference answer and required claim fidelity;
- numeric condition/unit correctness;
- comparative/multi-document structure;
- causal-strength preservation;
- neutrality and realism of wording;
- contradiction treatment and abstention rationale.

Thresholds for duplicate similarity, lexical overlap flags, and QC escalation are **OPEN**. Calibrate on draft/development data, document false positives/negatives, and freeze before final test lock. Automated flags trigger review; they do not automatically invalidate natural scientific wording.

## 40. Question and benchmark versioning

Use immutable benchmark releases and retain draft history:

```text
benchmark_v0.x  question/evidence drafts
benchmark_v0.y  validation and development pilot
benchmark_v1.0  approved frozen evaluation benchmark
benchmark_v1.1+ documented correction/revision; new evaluation version
```

The exact numbering convention is **OPEN**; immutability and traceability are FROZEN:

- never silently edit or delete a frozen test question;
- do not remove difficult items because a system performs poorly;
- do not replace a question after viewing final retrieval results;
- preserve question/evidence/answer/split hashes and change log;
- any correction creates a new version, identifies affected IDs, and records whether results are comparable.

## 41. Provenance

For every question preserve:

```text
question_id
question_text
primary_question_type
secondary_question_tags
difficulty_profile and any derived label
answerability status and rationale
source_document_ids and version_ids
gold_evidence_ids and source locators
reference_answer
required_claims and claim/evidence links
numerical requirements, conditions, units, tolerance
topic labels
creator and creation date
annotator/validator IDs or anonymized references
independent annotation records
agreement and adjudication status
validation status/date
development/test split and grouping key
creation protocol version
benchmark version
corpus version
revision/exclusion history
```

Also store model-assisted drafting metadata if used (model/version, prompt, date, raw suggestion, human changes, verification). Protect expert identities where required while retaining auditable anonymized IDs and qualifications.

## 42. Bias and validity assessment

| Threat | Likely impact | Mitigation | Residual limitation |
|---|---|---|---|
| Question-author bias | Selects topics/findings familiar to authors or expected to be retrievable | Use structured drafting guide, multi-author/topic coverage, independent validation, audit creator/topic distribution | Human selection remains |
| Expert-selection bias | Validators may overrepresent subfields, institutions, geographies, or technologies | Define expertise criteria, disclose coverage/conflicts, recruit across relevant topic areas where feasible | Available expert pool may be narrow |
| Topic imbalance | Aggregate results dominated by common corpus subfields | Report topic distribution and subgroup outcomes; do not force unsupported quotas | Rare PV topics may remain underpowered |
| Difficulty imbalance | One split or category may contain systematically harder items | Multidimensional difficulty annotation; grouped stratified split; report profile | Difficulty is partly judgment-based |
| Lexical-overlap bias | Wording may favor lexical retrieval or make overlap unlike natural questions | Neutrality audit and descriptive overlap measures; no result-driven pruning | Natural vocabulary overlap cannot and should not be eliminated |
| Answerability bias | Too many answerable/unanswerable items distort abstention evaluation | Define statuses and rationale; report split and category prevalence | Corpus coverage determines feasible unanswerable cases |
| Source-document bias | Many questions may depend on a few prolific/easy-to-extract papers | Track question counts per source; group source clusters in splits; report concentration | Benchmark may still reflect corpus availability |
| Publication bias | Corpus itself may overrepresent positive published findings | Preserve null/negative results when found; reflect Phase 3 limitations | Published literature remains selected |
| Open-access bias | Evidence set favors accessible full texts | Record acquisition attempts and exclusions; use lawful repository versions | Full-text requirement constrains coverage |
| Benchmark contamination | Questions/answers may be known to models or used during tuning | Test-label access control, no test tuning, versioning, pretraining caveat | Public source facts may be in model training |
| Annotation bias | Annotators may prefer particular interpretation or source | Independent annotations, rubric, evidence-based adjudication, preserve disagreement | Expert interpretation can still differ |
| Evaluator bias | Scores influenced by condition labels or answer style | Blind condition labels where feasible; randomize output order; use criterion-level rubric | Some outputs may reveal retrieved evidence/condition |
| Model-assisted generation bias | LLM drafts may hallucinate, favor fluent/obvious formulations, leak answers | Human-only acceptance, source verification, preserve prompts/raw drafts, style/answer leakage audit | LLM training distribution can shape drafts |
| Multi-document construction bias | Named sources or synthesis framing may favor papers with clear comparisons | Explicit source-role mapping, alternate evidence sets, neutral review | Corpus connectivity limits possible questions |
| Numerical annotation bias | Rounding/condition choices may favor a result | Record exact source precision, units/conditions, item-specific rationale; freeze tolerance before scoring | Source reporting may itself be incomplete |
| Exclusion bias | Hard-to-annotate questions may be excluded disproportionately | Retain exclusion/revision log and reason counts; inspect exclusions by topic/type | Some complex evidence cannot be scored reliably |

The benchmark is a designed sample of questions over the frozen corpus, not a census of all PV scientific information needs.

## 43. Model-assisted question generation policy

LLMs may be used only as drafting assistants, not as authorities for question validity, reference truth, answerability, or gold evidence.

If used:

- record model/provider/version, date, complete prompt, settings, and raw outputs;
- label output as machine-assisted draft;
- require human verification against the frozen corpus source text;
- independently identify and validate gold evidence;
- audit hallucinated premises, unsupported answers, answer leakage, copied evidence phrases, and stylistic/method bias;
- retain human edits and reasons;
- never automatically accept or score generated questions as benchmark items.

Whether to use LLM assistance is **OPEN**. The default conservative option is human drafting from verified source evidence. If assistance is chosen, decide before drafting and apply a consistent, logged process across categories.

## 44. Decision-status table

| Decision | Status | Resolution requirement |
|---|---|---|
| Frozen RQ and three retrieval arms | FROZEN | Do not alter |
| One question evaluated under all three arms | FROZEN | Preserve paired IDs and outputs |
| Question is primary benchmark unit with stable ID | FROZEN | Implement schema before annotation |
| Solar-PV scope and Phase 3 frozen corpus interface | FROZEN | Use corpus/version IDs; no silent corpus changes |
| Required question categories and support for insufficient evidence | FROZEN at taxonomy level | Exact mix remains open |
| Gold evidence independent of retrieval results | FROZEN | Annotators do not see arm outputs |
| Final test unavailable for tuning or question edits | FROZEN | Access controls and logs required |
| Question/reference/evidence/split versioning | FROZEN | Use immutable release/change log |
| Claim-level attribution support | PROVISIONAL recommendation | Pilot annotation burden and reliability; confirm before annotation freeze |
| Multidimensional difficulty profile | PROVISIONAL recommendation | Define scales and test rater agreement |
| Two independent judgments for critical fields | PROVISIONAL | Confirm staffing and adjudication plan |
| English-only versus multilingual | DEFERRED from Phase 3 pending its approval; do not assume | Follow approved Phase 3 language policy |
| Category proportions and topic coverage targets | OPEN — requires methodological decision | Corpus profile and study aims; freeze before test construction |
| Answerability substatus grouping | OPEN — requires methodological decision | Preserve granular raw labels; Phase 5 decides analysis grouping |
| Number of questions and split proportions | OPEN — requires methodological decision | Workload, pilot prevalence, effect/power assumptions; freeze before test lock |
| Exact difficulty scale and thresholds | OPEN — requires methodological decision | Independent pilot ratings and agreement |
| Gold relevance grades and set-logic | OPEN — requires methodological decision | Annotator reliability and Phase 5 metric needs |
| Reference-answer and claim segmentation rubric | OPEN — requires methodological decision | Calibration and agreement pilot |
| Expert count/qualification thresholds/conflicts | OPEN — requires methodological decision | Topic coverage, availability, workload; before annotation |
| Agreement coefficients/matching thresholds/minimums | OPEN — requires methodological decision | Rater structure/data type; set before final annotation |
| Numerical tolerances/conversions | OPEN — requires methodological decision | Source precision/uncertainty and item-specific scientific rationale |
| Lexical overlap metric and audit threshold | OPEN — requires methodological decision | Neutral pilot and false-flag review; before final neutrality audit |
| Development/test grouping and split algorithm | OPEN — requires methodological decision | Question/source evidence graph and leakage risks; before tuning |
| Retrieval/evaluation metric definitions and cutoffs | DEFERRED to Phase 5 | Preserve evidence labels sufficient to derive candidates |
| Statistical tests, power, CIs, effect sizes, multiplicity | DEFERRED to Phase 5 | Define estimand and pilot assumptions there |
| LLM-assisted drafting | OPEN — requires methodological decision | Choose before drafting; document model/prompt and human validation |
| Benchmark format/serialization and access policy | OPEN — requires methodological decision | Schema, privacy, licensing, test-label control |

An OPEN decision is not resolved by this table. Log each final decision with date, rationale, evidence, owner, protocol version, pilot use, and freeze point.

## 45. Phase 4 acceptance criteria

Phase 4 is complete only when an independent researcher can determine:

1. what constitutes a valid question and which categories/tags are used;
2. what answerable, unsupported, insufficient, and invalid mean;
3. how questions are constructed without retrieval-result influence;
4. how every answerable question's sufficient evidence is independently established;
5. how evidence alternatives, roles, required claims, and source conditions are recorded;
6. how reference answers preserve uncertainty, causality, numerical conditions, and contradictions;
7. how answerability, question validity, evidence sufficiency, and answer adequacy are independently validated;
8. which agreement measures match each annotation field and how disputes are adjudicated;
9. how question neutrality, lexical overlap, leakage, duplicates, and answer leakage are audited;
10. how development and test items are grouped, stratified, and protected;
11. how question count and topic distribution are justified without arbitrary equal quotas;
12. how retrieval, answer, attribution, and abstention evaluations can be computed from the annotation schema;
13. how benchmark versions, provenance, annotations, and access are reproduced;
14. which questions remain OPEN, what evidence resolves them, and when they must be frozen.

No final test question collection starts until the Phase 3 corpus version is frozen, benchmark-generation/annotation decisions needed for construction are approved, and the split/leakage plan is registered. No final evaluation or retrieval-result-based question revision occurs in Phase 4.

## 46. Phase 5 handoff

Phase 5 receives:

- the frozen RQ, corpus version, and immutable benchmark version;
- paired development/test question IDs and split/grouping manifests;
- exact question text, taxonomy, answerability, difficulty profile, and topic labels;
- reference answers, required claims, numeric rules, contradictions/caveats;
- complete gold evidence IDs, sufficient-set logic, relevance grades/roles, source locators, and provenance;
- annotation instructions, independent judgments, agreement statistics, disagreement/adjudication logs, validator qualifications/conflict handling;
- leakage controls, access logs, neutrality/lexical-overlap audit results, and version hashes;
- all recorded OPEN/PROVISIONAL decisions relevant to outcome measurement and their resolution status.

Phase 5 will define the formal evaluation framework and statistical analysis plan, including metric definitions and cutoffs for retrieval, answer quality, evidence attribution, abstention, paired estimands, uncertainty, significance/effect-size reporting, multiplicity, and power assumptions where justified. Phase 5 must not alter the frozen benchmark silently or use test results to revise annotations.

### Phase 4 → Phase 5 Handoff

Carry forward the frozen corpus and benchmark versions; paired split manifest; question, answerability, topic, and difficulty annotations; reference answers and required claims; independent gold evidence and alternative-sufficient-set logic; numerical and contradictory-evidence rules; annotation rubrics, rater agreement and adjudication records; neutrality/leakage audits; provenance and hashes; and the decision log. Phase 5 defines how these records become metrics and statistical comparisons; it does not construct new questions or rewrite the benchmark.
