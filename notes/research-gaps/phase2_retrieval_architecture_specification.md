# Phase 2 — Retrieval Architecture Specification

## Status and scope

**Status:** Phase 2 design specification; no final system implementation, final corpus collection, or final benchmark construction is authorized by this document.

This specification operationalizes the frozen research question without changing it:

> How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?

The principal manipulated variable is retrieval strategy: BM25, dense, or hybrid. This document defines shared interfaces and controls, records provisional positions, and specifies development-only procedures for resolving OPEN parameters. It does not select convenient defaults. An OPEN item must remain unresolved until its specified procedure and rationale are documented.

## Decision-status vocabulary

- **FROZEN:** fixed by the research question or experimental principle.
- **PROVISIONAL:** recommended architecture position for the primary experiment, subject to confirmation and documentation before final protocol lock.
- **OPEN:** no value or method is selected; the stated procedure must be used to decide it.
- **DEFERRED:** outside this phase and must be addressed in the named later phase.

## 1. Phase 2 objective

Specify a reproducible, comparable retrieval architecture for three RAG conditions over the same solar-PV scientific-paper corpus:

1. BM25 lexical retrieval;
2. dense semantic retrieval;
3. hybrid retrieval combining lexical and dense retrieval.

All non-retrieval system components are shared. The primary experiment does not include separately optimized prompts, chunking, context limits, generators, or rerankers by arm. Decisions that affect more than retrieval strategy must be flagged as potential confounders before they are incorporated.

## 2. Retrieval architecture overview

```text
One eligible solar-PV scientific-paper corpus and version
                         |
          Common extraction and normalization
                         |
      One shared chunk set, IDs, metadata, provenance
             /              |              \
       BM25 index       Dense index       BM25 + Dense
          |                 |             candidate lists
          |                 |                  |
          |                 |          pre-specified fusion
          \                 |                 /
            common result schema and deduplication
                         |
         common candidate/final-context constraints
                         |
          common context serialization and IDs
                         |
    same generator, prompt, decoding and answer schema
                         |
    answer plus evidence identifiers in every condition
                         |
  common, condition-blinded evaluation where feasible
```

The three arms may use different retrieval scoring mechanisms, because that is the treatment. They must not silently differ in corpus membership, source text, preprocessing, chunking, query wording, generation, context budget, or evaluation.

**Core distinction:** the identities of documents/chunks retrieved are expected to differ by strategy and are outcomes of the intervention. The rules and maximum resources available to retrieve and present evidence are controlled. Do not force all arms to receive the same evidence; doing so would erase the retrieval treatment. Do not permit one arm to receive a larger context allowance or additional non-retrieval processing.

## 3. Common pipeline

### 3.1 Shared corpus and document representation

All arms receive the same frozen corpus snapshot and the same document versions. Each source document must have a stable `document_id`, provenance/source record, version identifier, and extraction status. Each retrieval unit must have a stable `chunk_id`, `document_id`, section/path metadata where available, page/locator metadata where available, and exact source offsets or an equivalent traceable locator.

The corpus, eligibility policy, source acquisition, deduplication, version selection, extraction method, OCR policy, and metadata fields are **OPEN** and belong to the corpus/protocol phase. No documents or metadata are to be selectively available to one arm.

### 3.2 Common preprocessing and chunk store

Construct one canonical chunk store and expose the same chunk text and permitted metadata to each retriever. Preserve:

- a canonical text representation used consistently for indexing and retrieval;
- source-faithful text and locators for evidence display and attribution;
- heading/section path, page or source locator, and source document ID;
- structured content provenance for tables, equations, captions, and supplements when included.

Normalization must not silently delete scientifically meaningful symbols, signs, decimal points, units, subscripts/superscripts, Greek letters, chemical/formula notation, or identifiers. Any retrieval-specific tokenization or query/document encoding required by a selected method must be documented as part of that retriever's method, not applied as undocumented corpus preprocessing.

### 3.3 Query path and result contract

Every arm receives the same benchmark question string and same fixed question metadata. The default architectural constraint is no query rewriting, expansion, decomposition, or LLM-generated search query in the primary comparison. This constraint is **PROVISIONAL** and must be confirmed in the Phase 3 protocol; if a transformation is later introduced, it must be the same transformation for all arms and its interaction with retrieval strategy must be justified.

Each retriever returns a ranked list conforming to a common result contract:

```text
question_id
rank
chunk_id
document_id
retrieval_score (native score; not assumed comparable across arms)
retrieval_method
index/model/configuration version
```

Retain native scores for audit, but do not compare raw BM25, cosine/dot-product, and RRF scores as if they shared a scale. Preserve per-arm logs of candidates, ranks, exclusions, duplicate removals, and tie-breaks.

### 3.4 Common downstream interface

After retrieval-specific ranking and the common selection/serialization rules are applied, each arm passes a context object with the same schema to one generator. It contains evidence text and stable evidence identifiers, plus only the same permitted metadata fields in the same format. The prompt, answer format, evidence/citation identifier format, generation configuration, and evaluation interface are shared.

## 4. BM25 specification

### 4.1 Method definition

The BM25 arm indexes the common chunk text and ranks chunks for the unchanged benchmark query using BM25 lexical matching. No dense scores, reranker, query-expansion model, graph traversal, or arm-specific post-retrieval semantic filtering is used in this arm.

### 4.2 Implementation choices and status

| Design item | Phase 2 specification | Status |
|---|---|---|
| Library/index implementation | Select one documented implementation after compatibility, stable-version, reproducibility, and licensing review. Record library, version, analyzer configuration, and index build. | OPEN |
| Tokenization/analyzer | Use a deterministic, versioned analyzer. Test preservation/handling of technical terms, hyphenated compounds, abbreviations, Greek letters, symbols, numbers, and units on development material. | OPEN |
| Text normalization | Use the common canonical text; retain source-faithful text separately. Any analyzer normalization must be versioned and shared across BM25 index/query processing. | OPEN |
| Stop words | Do not assume a generic stop list is appropriate for scientific queries. Evaluate with/without a specified list on development data; freeze one setting. | OPEN |
| Stemming/lemmatization | Do not enable by default. Evaluate no stemming versus a justified, language-compatible stemmer/lemmatizer on development data; freeze one. | OPEN |
| Scientific terminology | Preserve raw/canonical terms; assess term handling on a development lexicon/sample spanning abbreviations, compound terms, formulae and domain terminology. Avoid silently expanding abbreviations. | OPEN |
| Numerical terms | Preserve digits, decimal points, signs, ranges, and meaningful identifiers in the canonical representation; determine analyzer behavior through tests. | Constraint FROZEN; exact analyzer OPEN |
| Symbols and units | Preserve in canonical text; determine whether tokenizer emits, normalizes, or separates them and document the behavior. | Constraint FROZEN; exact analyzer OPEN |
| BM25 parameters | Select `k1`, `b`, and any implementation-specific parameters using development data only; do not import an unexplained default. | OPEN |
| Indexing unit | Shared chunk is the index unit, subject to final chunking decision. | FROZEN in architecture; chunk definition OPEN |
| Query formulation | Original benchmark question, unchanged. No arm-specific rewriting in the primary comparison. | PROVISIONAL |
| Ranking/ties | Descending native BM25 score; deterministic tie-break on stable `chunk_id`. | PROVISIONAL |
| Candidate depth | One common per-arm candidate budget is used for BM25, dense, and the final hybrid ranked list; exact value and counting rule are OPEN. | OPEN |

### 4.3 Development selection and reproducibility

Use only the designated development questions/documents and relevance/evidence judgments to assess analyzer and parameter alternatives. Specify the development objective and tie-breaking rule before tuning. Search or tune a bounded, documented candidate set; report all tried settings and selection results. Freeze the implementation, analyzer, and parameters before test evaluation. If no defensible superiority appears, use a predeclared simplicity/reproducibility rule rather than inspecting test outcomes.

Record exact software version, index schema, analyzer, BM25 formula/variant, parameter values, corpus/chunk snapshot hash, query text, candidate depth, tie-breaking rule, and index-build date.

## 5. Dense retrieval specification

### 5.1 Method definition

The dense arm encodes each shared chunk and each original benchmark question into vectors using a single selected embedding model and its documented query/document encoding procedure. It ranks chunks by one selected vector similarity/distance measure. It does not use BM25 scores or a hybrid fusion stage.

### 5.2 Model selection framework

No embedding model is selected in Phase 2. Construct a versioned candidate shortlist in the development phase. A candidate is eligible only if its identity/version and query/document encoding can be reproduced and its terms of use permit the planned research use. Evaluate candidates against these criteria:

1. retrieval suitability for short scientific questions and passage/document evidence retrieval;
2. evidence of performance on scientific or technical text, where relevant evaluation data are available;
3. reproducibility of model weights, tokenizer, inference code, and version;
4. access and licensing compatibility for the project;
5. computational feasibility for indexing and repeated query evaluation;
6. model/version stability and ability to pin exact artifacts;
7. appropriate context length and documented query/document encoding behavior;
8. known limitations or language/domain mismatches relevant to the eventual corpus.

Do not select a model solely because it is popular, has a large embedding dimension, or performs well on a benchmark unrelated to the study's task. Document candidate exclusions and evidence for selection. Use development retrieval performance only after eligibility screening; do not use final test data for model selection.

### 5.3 Dense settings and status

| Design item | Phase 2 specification | Status |
|---|---|---|
| Embedding model | One model/version selected from a documented eligible shortlist using the procedure above. | OPEN |
| Embedding dimension | Inherited from the pinned model; record exact dimension rather than choosing independently. | OPEN pending model |
| Query encoding | Use the model's documented query pathway/instruction, if applicable; original question text remains unchanged. Record prefix/instruction and tokenizer behavior. | OPEN pending model |
| Chunk encoding | Use the model's documented passage/document pathway and same shared chunks. Record truncation and pooling behavior. | OPEN pending model |
| Normalization | Select and record vector normalization behavior consistent with model guidance and similarity choice. | OPEN |
| Similarity metric | Select one metric compatible with the model and index; do not assume cosine, dot product, or Euclidean distance. | OPEN |
| Index | Choose exact or approximate nearest-neighbor search after feasibility/accuracy testing. | OPEN |
| Approximation | If ANN is used, quantify its retrieval agreement/recall relative to exact search on development queries; pin index parameters and random seeds where supported. | OPEN |
| Candidate depth | Use the same final candidate budget definition as other arms; exact value OPEN. | OPEN |
| Compute | Record hardware, accelerator, precision/quantization, batch size, memory, library/model versions, and latency measurement conditions. | OPEN |

### 5.4 Reproducibility

Pin model name, exact revision/hash, tokenizer revision, code/library versions, encoding instructions, truncation behavior, vector precision, normalization, similarity, index type/parameters, random seeds, and corpus/chunk snapshot. Cache vectors only with chunk/model/configuration keys and preserve checksums. A candidate model change after test evaluation begins creates a different experiment and must not overwrite the original run.

## 6. Hybrid retrieval specification

### 6.1 Proposed architecture

The working candidate is independent BM25 and dense ranked lists over the same chunk store, followed by deterministic rank fusion. Reciprocal Rank Fusion (RRF) is the provisional fusion candidate; it is not permanently frozen by Phase 2.

For a chunk \(d\), standard RRF is:

\[
\operatorname{RRF}(d) = \sum_{r \in \{BM25, Dense\},\, d \in L_r}
\frac{w_r}{c + \operatorname{rank}_{r}(d)}
\]

where \(L_r\) is a component's ranked list, \(w_r\) is its weight, and \(c\) is the rank constant. Equal component weights are a possible default design constraint, not a selected value; weights, rank convention, and `c` remain OPEN until specified and tuned on development data.

### 6.2 RRF assessment

**Why RRF is a reasonable working candidate:** BM25 and dense retrievers produce native scores with different scales and distributions. Rank fusion avoids directly treating those uncalibrated scores as commensurate and is straightforward to reproduce from saved component rankings.

**Limitations:** RRF discards score magnitude, can be sensitive to component candidate depth and rank constant, and may favor documents appearing reasonably high in both lists over a highly ranked result unique to one component. Unequal component weights introduce another tuning choice. RRF does not guarantee better retrieval or answer outcomes.

**Alternative:** score-based fusion may use more within-list score information but requires a normalization/calibration procedure. Such calibration can itself favor a method, require extra held-out data, or be unstable across queries. Compare a prespecified rank-fusion candidate against one justified score-normalization candidate on development data only if the comparison is needed to select the primary hybrid definition.

### 6.3 Hybrid choices and status

| Design item | Phase 2 specification | Status |
|---|---|---|
| Components | The BM25 and dense implementations selected for the other arms; no separate hybrid-only component model. | FROZEN |
| BM25/dense candidate depths | Predeclare per-component depths under one total candidate-generation budget. Do not give the hybrid arm an undocumented larger candidate budget. Exact depths and allocation OPEN. | OPEN |
| Fusion | RRF is the working candidate. Compare against a justified score-fusion alternative only on development data if needed; select and freeze exactly one primary method. | PROVISIONAL |
| RRF formula | Use the stated reciprocal-rank sum, with explicit rank origin, weights, candidate-list cutoff, and missing-item treatment. | PROVISIONAL |
| RRF rank constant `c` | Select from a bounded prespecified candidate set using development data; never select on final test. | OPEN |
| Weights | Prefer equal weights as the simplest initial candidate; if unequal weights are considered, tune only on development data and disclose the added degrees of freedom. | OPEN |
| Duplicate chunks across lists | Merge identical `chunk_id` entries before final ranking; retain both component ranks and compute one fused score. | PROVISIONAL |
| Duplicate/overlapping chunks in final list | Apply the same deterministic duplicate/overlap policy after fusion and in all arms. | OPEN (common policy) |
| Final ranking/ties | Descending fused score, then deterministic stable `chunk_id` tie-break. | PROVISIONAL |
| Final output depth | Subject to the common candidate and context limits used by all arms. | OPEN |

### 6.4 Candidate-budget fairness

Hybrid retrieval naturally executes two component searches. To prevent an unreported candidate-opportunity advantage, define a total candidate-generation budget before tuning. The rule for counting component list entries, overlap/duplicates, unique union candidates, and the allocation between BM25 and dense sublists is **OPEN**. Compare feasible allocations on development data under the same declared total candidate budget and computational accounting. The hybrid arm may return a different set of evidence; it must not receive a larger final context allowance.

## 7. Chunking specification

### 7.1 Shared chunking rules

One chunking pipeline creates the retrieval units for all three arms. There is no BM25-specific, dense-specific, or hybrid-specific segmentation.

The chunker should, where supported by source structure:

- preserve section headings and hierarchical section paths as metadata;
- prefer paragraph and section boundaries over arbitrary mid-sentence splits;
- retain stable source/page/offset locators;
- avoid splitting tables from their captions/headers when they are represented as a coherent evidence unit;
- preserve equations and adjacent explanatory text with traceable identifiers;
- keep figure captions attached to figure identifiers and relevant local context;
- handle references and supplementary material through one declared eligibility policy;
- retain provenance to the source PDF/page/table/figure or supplement for attribution.

Whether tables, equations, captions, references, and supplementary material are included in the searchable corpus is **OPEN** at corpus protocol stage. If included, their representations must be shared across all three arms.

### 7.2 Chunk parameters

Chunk unit, section-aware rules, token-counting tokenizer, maximum size, overlap, treatment of oversized tables/equations, boundary fallback, and metadata inclusion are **OPEN**. Do not pick conventional token counts or overlap percentages by assumption.

### 7.3 Pilot selection procedure

Before final test evaluation:

1. Define a small but structurally diverse pilot sample of eligible development documents.
2. Specify candidate chunking strategies and parameter ranges before observing test outcomes.
3. Check structural integrity: heading path retention, source locator accuracy, table/equation/caption integrity, and chunk traceability.
4. Compare development retrieval performance and evidence-boundary coverage across the candidate chunk configurations, using the same candidate pool and query benchmark across retrievers.
5. Select a common chunking configuration using a prespecified multi-criterion rule that includes retrieval/evidence performance, structural integrity, and computational feasibility.
6. Freeze the chunker and regenerate one canonical chunk store for all three arms.
7. Record all alternatives, outcomes, exclusions, and the selection rationale.

The pilot sample, candidates, metrics, and selection rule are **OPEN** and must be registered before the pilot. The final test set is not used.

## 8. Retrieval-depth specification

Keep two concepts separate:

1. **Candidate depth:** the maximum ranked candidates exposed by an arm before downstream selection or retrieval-metric computation.
2. **Generation context:** the smaller selected evidence payload actually supplied to the generator under the common context policy.

Retrieval evaluation may report a prespecified curve over multiple depths, but the values are **OPEN** and must be justified by benchmark size, common candidate budgets, and intended use. Do not select only the depth producing the most favorable result. All arms must be evaluated on the same question set and depth definition.

For the primary hybrid condition, component list depths and total candidate budget must be declared separately. Do not compare BM25 top-C and dense top-C to a hybrid union of up to 2C candidates without explicitly identifying that increased candidate opportunity. The development protocol must choose either a common total candidate-entry budget or another justified compute/opportunity constraint and apply it consistently.

## 9. Top-k specification

No numerical value of `k` is selected in Phase 2.

- For retrieval evaluation, predeclare one or more cutoffs and report each consistently across arms.
- For generation, use one shared maximum number of chunks and one shared context-token ceiling. Both are limits; neither arm may exceed them.
- If an arm has fewer eligible candidates than the common cap, pass fewer rather than padding with unrelated evidence.
- If passage lengths differ, a common top-k alone is insufficient; apply the context-token ceiling and deterministic packing rule in Section 10.
- Select candidate/final values using development data and a predeclared rule; freeze all values before final test evaluation.

## 10. Context-budget specification

### 10.1 Common evidence packing

Use the same context-construction function for each arm. It receives the arm's ranked, deduplicated candidates and applies:

1. the same duplicate and overlap policy;
2. the same maximum number of chunks;
3. the same maximum context-token budget, measured with the pinned generator tokenizer or another justified fixed tokenizer;
4. the same deterministic order rule, normally retrieval rank order, unless another common rule is justified;
5. the same truncation policy;
6. the same metadata and evidence-ID serialization;
7. the same rule for omitted items and source locators.

The exact numeric caps, tokenizer, ordering, truncation and overlap thresholds are **OPEN**.

### 10.2 Fairness interpretation

Do not force arms to receive identical chunk identities: returned evidence is an effect of retrieval strategy. Instead, equalize the maximum opportunity and downstream payload rules. Actual context lengths may be below the shared maximum because one arm has fewer eligible results or its ranked chunks pack differently. Log actual chunk count, token count, truncation, duplicates, and evidence coverage per question and arm.

If actual usable context differs systematically because of implementation choices rather than retrieval results—for example, arm-specific chunk size or a different serialization format—the comparison is **methodologically confounded**. If difference follows from which evidence each strategy retrieves under the same shared caps, it is a treatment outcome and must be reported, not corrected by manually substituting evidence.

## 11. Reranking decision

**Primary-experiment position: NO RERANKER (PROVISIONAL).**

A reranker adds a second retrieval mechanism and may materially alter rankings, interact differently with BM25/dense/hybrid candidates, add cost/latency, and obscure whether downstream differences are caused by the primary retrieval strategy or reranking. Adding it to one arm is a direct confound. Applying the same reranker to all arms is not automatically neutral because its candidate inputs differ by arm and it changes the estimand from first-stage retrieval to retrieval-plus-reranking.

The primary experiment should therefore omit reranking, post-retrieval filtering, and evidence compression unless a scientific justification is documented and the design is revised before final evaluation. Reranking may be evaluated as a separately labeled future extension or a separate factor, not silently merged into these three conditions.

## 12. Generator controls

All arms use the same:

- generator model and exact version/revision;
- runtime/API version and service configuration, if hosted;
- system and user prompt templates;
- generation parameters and stopping behavior;
- output schema and answer format;
- evidence/citation identifier convention;
- context serialization and evidence metadata;
- error, timeout, retry, and invalid-output handling;
- run/repeat policy and random-seed handling where supported.

Exact generator, version, temperature, maximum output tokens, decoding settings, seeds, repeat count, and retry policy are **OPEN** and deferred to the generator/evaluation protocol. Do not tune the generator separately for retrieval conditions. Preserve the raw request and response for each run, subject to privacy, licensing, and provider constraints.

## 13. Prompt controls

Use one common prompt family and the same exact production prompt version for all arms. The common prompt must instruct the generator to:

1. answer the scientific question using supplied evidence;
2. avoid unsupported claims;
3. state when supplied evidence is insufficient rather than fabricate;
4. attribute claims to supplied evidence identifiers where required;
5. follow one fixed answer and attribution format.

The exact wording, examples, answer length, citation syntax, and whether the prompt includes abstention rules are **OPEN**. Prompt development must use development data only; freeze the prompt before final test evaluation. No retrieval-specific prompt wording or per-arm prompt optimization is allowed.

## 14. Data-leakage controls

### 14.1 Controllable experimental leakage

The later protocol must prevent or document:

- test question, answer, or gold-evidence use in retriever, embedding, chunking, fusion, prompt, or threshold selection;
- access to final test judgments during system development;
- duplicate or paraphrased questions crossing development/test;
- accidental benchmark-answer insertion into corpus metadata, indexes, caches, or prompt examples;
- source-paper or version duplication that makes evidence available through a nominally distinct record;
- unequal tuning effort or number of trials across retrieval arms;
- evaluator access to arm labels before subjective scoring where blinding is feasible.

Document benchmark construction dates, data access roles, split assignments, tuning logs, and any exposure. Split logic and source-paper grouping are **OPEN**. If test evidence must be present in the retrieval corpus to answer test questions, retain the evidence corpus but withhold test labels/judgments and do not tune against them.

### 14.2 Model pretraining exposure

Public scientific papers may have appeared in a generator's pretraining data. This exposure may be difficult or impossible to determine or eliminate. Do not claim it is eliminated. Record model provenance/known data disclosures, acknowledge residual exposure, use the same generator in all arms, and assess answer dependence on retrieved context using the predeclared evidence-grounding evaluation. The precise audit is **OPEN**.

## 15. Reproducibility specification

Store an immutable per-run manifest (e.g. versioned JSON/YAML plus query-level result tables) with at least:

- experiment/run ID and timestamp;
- code revision/commit and dirty-worktree status;
- corpus ID/version, source inventory hash, document/version IDs;
- benchmark ID/version, split, question IDs, and label/evidence version;
- preprocessing and extraction versions/configuration;
- chunking code/version/configuration, tokenizer, chunk IDs and store hash;
- BM25 implementation/version, analyzer, fields, parameters, candidate depth;
- embedding model/revision/hash, tokenizer, query/document encoding, dimension, normalization, similarity;
- vector-index implementation/version/type/parameters, exact/ANN choice, seed, build metadata;
- hybrid fusion implementation/version/formula, weights, rank convention, component depths, RRF constant if selected;
- duplicate, overlap, tie-breaking, final-k and context-token packing rules;
- generator/model revision, provider/API version if applicable, prompt version/hash, generation settings;
- per-question ranked candidate IDs and scores/ranks for each component and arm;
- selected context chunk IDs, ordering, actual token/chunk counts and truncation;
- raw generated answer and evidence IDs, evaluation outputs and assessor/blinding metadata;
- hardware, operating system, runtime, libraries/dependencies, precision/quantization;
- failures, retries, timeouts, exclusions, manual interventions, and protocol deviations.

Store artifacts in a version-controlled or immutable research-data location with access control, integrity hashes, backup, and a documented retention/release policy. Exact repository, serialization schema, and public release scope are **OPEN**. Store only lawful corpus/evidence artifacts; if publisher terms prohibit redistribution, preserve identifiers, hashes, and reproducible acquisition instructions instead of unauthorized copies.

## 16. Fair-comparison matrix

| Component | BM25 | Dense | Hybrid | Controlled? | Potential confounder? |
|---|---|---|---|---|---|
| Corpus/documents/versions | Same corpus snapshot | Same corpus snapshot | Same corpus snapshot | Yes; invariant | Yes if membership or versions differ |
| Extracted canonical text | Shared representation | Shared representation | Shared representation | Yes; invariant | Yes if retrieval-specific preprocessing alters content |
| Chunk IDs and boundaries | Same chunk store | Same chunk store | Same chunk store | Yes; invariant | Yes if chunking differs by arm |
| Query wording | Original question | Original question | Original question | Yes; invariant | Yes if query rewriting differs |
| Primary ranking signal | BM25 lexical score | Dense-vector similarity/distance | Fused lexical and dense ranks/scores | No; intentionally manipulated | Not a confound if each is correctly implemented and other controls match |
| Analyzer/encoder | BM25 analyzer | Selected embedding encoder | Same BM25 analyzer and same dense encoder used in corresponding arms | Partly; method-specific representation is inherent | Yes if tuned unequally or corpus text is changed selectively |
| Candidate retrieval | BM25 ranked candidates | Dense nearest candidates | Two component lists and fused candidates | Equal opportunity rule OPEN | Yes if hybrid receives an undocumented larger candidate/compute budget |
| Raw score scale | BM25 native score | Model-native similarity | RRF score or selected fusion score | No common raw scale assumed | Yes if incomparable raw scores are directly added without justified calibration |
| Fusion | None | None | One frozen fusion rule | No; hybrid-defining operation | Fusion choice/weights tuned on test = leakage/confound |
| Reranker/filter/compression | None in primary experiment | None in primary experiment | None in primary experiment | Yes; excluded provisionally | Yes if present in only one arm; changes estimand if shared |
| Duplicate handling | Same stable-ID policy | Same stable-ID policy | Merge component duplicates and apply same final policy | Yes; common policy | Yes if arm-specific/different |
| Final chunk-count cap | Same maximum | Same maximum | Same maximum | Yes; invariant | Yes if caps differ |
| Context-token ceiling | Same maximum | Same maximum | Same maximum | Yes; invariant | Yes if caps, tokenizer, or packing rules differ |
| Context content/order | Returned ranking under same packing rule | Returned ranking under same packing rule | Fused ranking under same packing rule | Rule controlled; evidence varies by treatment | Evidence identity is intended outcome; serialization differences are confounders |
| Generator/prompt/decoding | Same | Same | Same | Yes; invariant | Yes if any are arm-specific |
| Evaluation | Same benchmark, rubric, and code | Same benchmark, rubric, and code | Same benchmark, rubric, and code | Yes; invariant | Yes if evaluator/scoring differs |
| Index execution resources | Record and budget consistently | Record and budget consistently | Account for both component retrievals | Controlled where feasible; exact policy OPEN | Potentially, especially for latency/cost outcomes |

### Fairness audit rule

Every between-arm difference must be tagged before implementation as one of:

1. **intended treatment difference** (retrieval strategy);
2. **necessary method-specific consequence** (e.g., sparse score versus vector similarity), documented and not independently interpreted as a treatment;
3. **controlled nuisance difference** (held constant by common data/policy);
4. **potential confounder** (must be removed, explicitly justified, or analyzed as a separate design change).

No component may be assumed fair merely because the question set is shared.

## 17. Threats to validity

| Threat | Risk | Mitigation/record |
|---|---|---|
| Embedding-model bias | Dense results can depend on training domain, language, query style, representation, or licensing/access constraints. | Eligibility screen; development-only selection; pin exact revision; report selection process and limitations. |
| Chunking effects | Boundaries may split a relevant claim, table, formula, or citation context; effects can differ by retrieval method. | One shared chunk store; structural pilot; preserve parent/locator links; freeze before test. |
| Retrieval-depth effects | Metrics and evidence available to generation vary with candidate depth. | Common depth definition/budget; prespecified cutoffs; development-only selection; report curves and final operating point separately. |
| Context-budget effects | Unequal evidence tokens can affect generated answer quality independently of ranking. | Common chunk and token caps, tokenizer, assembly, ordering, and truncation; log actual context size per query/arm. |
| Lexical/scientific terminology mismatch | BM25 may miss synonyms, abbreviations, morphology, or symbol variants. | Preserve technical forms; test analyzer on development set; report query/document vocabulary limitations. |
| Dense semantic mismatch | Embeddings may blur numerical distinctions, units, negation, or similar technical concepts. | Preserve source text and numerics; evaluate evidence retrieval and attribution; do not infer quality from semantic similarity alone. |
| Hybrid-fusion bias | Fusion formula, weights, candidate depths, and component imbalance can favor one list. | Prespecify candidate budget; development-only fusion selection; log component ranks and run sensitivity analyses without test tuning. |
| Generator sensitivity | Identical generator can react differently to context order, length, or formatting. | Common generator, prompt, formatting and decoding; control context budgets; retain actual payloads; use a predeclared repeat plan. |
| Benchmark contamination | Test labels may leak into development/tuning, or public questions may be memorized. | Separate access to labels; logs and split controls; no test tuning; disclose uncontrollable pretraining exposure. |
| Question difficulty imbalance | One question subset may disproportionately favor a retrieval method. | Matched within-question evaluation; stratify/report predeclared subgroups; assess difficulty and clustering at benchmark design. |
| Document duplication/version duplication | Duplicate papers or versions inflate retrieval hits and evidence counts. | Provenance-aware deduplication and version policy; preserve canonical document IDs and aliases. |
| Corpus composition bias | Included sources, publication venues, years, or paper types may not represent intended literature. | Define eligibility and sampling frame; report corpus profile and exclusions; limit inference to that frame. |
| Domain coverage bias | Solar-PV subfields, terminology, geographies, or publication types may be underrepresented. | Profile coverage; stratify where justified; document known omissions and avoid broad generalization. |
| Evaluation bias | Human raters or automatic metrics may favor answer style, citation formatting, or known conditions. | Common rubric; blind arm labels where feasible; adjudication and agreement plan; preserve raw evidence/answers. |
| Evidence-reference incompleteness | Gold evidence may omit valid supporting sources, penalizing otherwise correct retrieval/attribution. | Annotate multiple valid evidence spans where feasible; define adjudication; report annotation limitations. |
| Approximate-index error | ANN may introduce retrieval error unrelated to the embedding representation. | Compare against exact search on development data; quantify approximation agreement; freeze index settings. |
| Compute/latency asymmetry | Hardware, caching, or batched execution can distort resource comparisons. | Use stable hardware and repeated timing; separate algorithmic and end-to-end latency; report cache and batching policy. |
| Analysis multiplicity | Many metrics, cutoffs, and subgroups can yield selective conclusions. | Predeclare primary outcomes/contrasts and multiplicity handling before test evaluation. |

## 18. Frozen decisions

1. The frozen research question is unchanged.
2. The target task is evidence-grounded question answering over solar-PV scientific literature.
3. The primary conditions are BM25, dense, and hybrid retrieval.
4. Retrieval strategy is the principal manipulated variable.
5. One corpus, document-version policy, question benchmark, and evaluation protocol are shared across all three arms.
6. Preprocessing, chunking, generator, prompt, answer/evidence format, and generation settings are common.
7. All arms use one shared chunk store; arm-specific chunking is prohibited in the primary experiment.
8. Reranking is excluded from the primary architecture provisionally; it cannot be added to one arm.
9. The final test set is not used for tuning any component.
10. Retrieval quality, answer quality, and evidence attribution are separate outcome families.
11. A system difference beyond retrieval strategy is flagged as a potential confounder before incorporation.
12. No specific model, parameter, corpus size, chunk size, `k`, fusion constant, metric, or test is frozen by this Phase 2 specification.

## 19. Provisional decisions

| Position | Rationale | Confirmation required |
|---|---|---|
| Use one shared canonical chunk store and stable evidence IDs | Necessary for paired comparison and attribution | Confirm chunk architecture and provenance support during pilot |
| Use original question wording without arm-specific query rewriting | Avoids introducing query-processing differences | Confirm in Phase 3 protocol; if query rewriting is studied, it cannot vary by arm in this experiment |
| Use RRF as the working hybrid candidate | Avoids naïvely adding incomparable native BM25 and dense scores | Compare with one justified alternative on development data only if needed; freeze one method |
| Exclude reranking in the primary comparison | Better isolates first-stage retrieval strategy | Confirm before protocol lock; do not silently change after evaluation |
| Apply a common max chunk count and context-token ceiling | Prevents one arm receiving larger generation allowance | Determine operational values/tokenizer and report actual context used |
| Use within-question matched comparisons | Controls question difficulty in pairwise arm comparisons | Confirm analysis model for clustering/repeats |

Provisional does not mean frozen. Resolve and record each position before final protocol lock.

## 20. Open decisions

For all OPEN decisions, the general rule is: use pilot/development data only, prespecify candidate options and selection criteria before evaluating them, preserve the trial record, and freeze selected values before final test evaluation.

| OPEN decision | Why it matters | Evidence needed and evaluation | Before dev set? | Freeze before final test? |
|---|---|---|---|---|
| Corpus scope, sources, inclusion, versions, sampling | Defines target population and attainable evidence | Literature/domain rationale, licensing, coverage profile, deduplication audit | Eligibility frame before dev | Yes |
| Benchmark source, construction, size and splits | Determines validity, power, and leakage risk | Annotated questions, answerability, reference evidence, difficulty/domain coverage | Split plan and annotation protocol before tuning | Yes |
| Text extraction/OCR and canonical normalization | Errors alter all arms and evidence traceability | Pilot extraction audits against source pages; symbol/table/equation checks | Basic process before dev pilot | Yes |
| Chunk boundaries, size, overlap, structured elements | Affects candidate matches and context utility | Structural integrity and retrieval/evidence outcomes on development sample | Candidate set and pilot criteria before pilot | Yes |
| BM25 implementation/analyzer/stemming/stop words/parameters | Changes lexical matching and technical-term behavior | Reproducibility/licensing review; bounded development comparisons | Candidate options/criteria before tuning | Yes |
| Dense model, encoding, metric and index | Determines semantic representation, resource needs, and rankings | Model-card/license review, scientific-text suitability, dev retrieval results, exact-vs-ANN check | Eligibility criteria/shortlist before dev outcomes | Yes |
| Hybrid fusion/weights/RRF constant | Changes combined ranking and component influence | Component list diagnostics and development retrieval results under declared budget | Candidate rules before tuning | Yes |
| Candidate-depth budget and hybrid allocation | Changes opportunities and compute across arms | Development depth curves and retrieval-work accounting | Budget definition before tuning | Yes |
| Duplicate and overlapping-chunk policy | Affects ranking, context redundancy, evidence recall | Document/chunk provenance and structural inspection | Policy candidates before dev | Yes |
| Final top-k/context-token budget/packing | Controls downstream evidence quantity and costs | Development answer/evidence outcomes plus token/context diagnostics | Candidate ranges and criteria before tuning | Yes |
| Query rewriting and metadata use | May create additional treatment dimensions | RQ alignment and evidence of necessity; identical transformation requirement | Decide inclusion before tuning | Yes |
| Generator/prompt/output format/settings | Strongly affect QA and citation behavior | Availability, deterministic behavior, pilot prompt evaluation on dev | Freeze process before final benchmark test | Yes |
| Outcome metrics, raters, rubrics and blinding | Determines construct validity and measurement bias | Metric validity, annotation guide, calibration and agreement plan | Define primary outcome protocol before evaluation | Yes |
| Statistical estimand/model/power/multiplicity | Determines valid inference and uncertainty | Benchmark structure, pilot variance, paired/clustering considerations | Analysis plan before test access | Yes |
| Latency/resource protocol | Measurement depends on compute, batching, caching, and load | Hardware/services, timing plan, warm-up/repeat plan | Before resource measurement | Yes |
| Run repeats, seeds and failure treatment | Stochasticity and service failures can bias outcomes | Generator determinism, pilot variability, predeclared retry policy | Define before dev comparison | Yes |
| Artifact storage/release constraints | Reproduction depends on lawful access and retained provenance | Licenses, provider terms, repository/access policy | Before data acquisition | Yes |

Any selected values and rejected alternatives must be added to a versioned decision log with date, evidence, rationale, owner, and whether selection used development data.

## 21. Deferred decisions

These decisions belong to later phases and are intentionally not made here:

- **Phase 3 — Pilot and development protocol:** establish the development/test split and access controls; evaluate candidate preprocessing/chunking, retrievers, dense models, hybrid fusion, candidate depth, context packing, and generator/prompt feasibility using development data; lock the complete protocol before opening final test labels.
- **Phase 4 — Final corpus and benchmark construction:** apply frozen eligibility, extraction, versioning, annotation, deduplication, and split rules; preserve provenance and benchmark blinding.
- **Phase 5 — Implementation and integration:** implement only after Phase 3 choices are recorded; verify identical shared inputs and controls across arms before any final test evaluation.
- **Phase 6 — Final evaluation and analysis:** execute the frozen protocol; report deviations, paired outcomes, uncertainty, statistical tests, and all required outcome families.
- Final sample-size/power calculation, subject to a valid pilot variance estimate and chosen estimand.
- Final public artifact release, subject to corpus/model/provider license and privacy restrictions.

No final-corpus collection, final-benchmark construction, or final RAG implementation is part of Phase 2.

## 22. Phase 2 acceptance criteria

Phase 2 is complete when:

1. The common architecture and each arm's distinct retrieval operation are explicit.
2. All fixed invariants and method-specific differences are identified.
3. No model, parameter, chunk size, top-k, context budget, fusion constant, metric, or inferential test has been selected by convenience.
4. Each OPEN item has a rationale, evidence requirement, development-only decision process, and a point by which it must be frozen.
5. RRF and no-reranker positions are labeled provisional rather than silently frozen.
6. Candidate-depth and context-budget fairness risks are explicitly controlled or scheduled for resolution.
7. The comparison-validation rule below is retained in the implementation protocol.
8. Leakage controls and reproducibility metadata are specified.
9. The exact frozen RQ is reproduced unchanged.
10. No final implementation, final corpus collection, or final benchmark construction has begun.

### Comparison-validation rule

If BM25, dense, and hybrid use different context quantities, prompts, generators, chunking/preprocessing, or generation settings, classify the comparison as **methodologically confounded** unless the deviation is explicitly justified, isolated, and reported. Sharing questions alone does not make the comparison controlled.

If any proposed change affects more than retrieval strategy, flag it as a **potential confounder** before adoption. Do not silently fold it into the retrieval treatment. If the issue cannot be controlled, report it, assess its direction/likely impact without claiming certainty, and narrow interpretation accordingly.

## 23. Recommended next phase

**Phase 3 — Pilot and development protocol design.**

Before coding the final system, prepare a preregistered development-only decision protocol that:

1. defines the development/test split and protects final test questions, answers, and evidence judgments;
2. defines eligible candidate models/implementations and licensing/reproducibility checks;
3. prespecifies chunking and analyzer candidate sets and the pilot-document sample;
4. sets a common candidate-generation and compute-budget accounting rule, including hybrid component allocation;
5. compares RRF with a justified alternative only if needed, using development data;
6. establishes a shared top-k/context-token packing policy and generator/prompt control procedure;
7. defines primary retrieval, answer-quality, and evidence-attribution metrics and paired analysis plan;
8. states tuning limits, selection criteria, and freeze dates for every OPEN decision;
9. produces a signed/versioned decision log before final test evaluation.

### Phase 2 → Phase 3 handoff

Carry forward:

- the frozen RQ and three retrieval conditions;
- the common corpus/chunk/query/generator/prompt/evaluation invariants;
- the no-arm-specific-chunking and no-arm-specific-prompt rules;
- the provisional RRF hybrid candidate and provisional no-reranker primary position;
- the shared result schema and evidence-ID/provenance requirements;
- the confounder and comparison-validation rules;
- the complete OPEN-decision register and development-only selection requirements;
- the leakage safeguards, run-manifest fields, and fair-comparison matrix.

Phase 3 must return a documented, justified decision for every OPEN item or explicitly retain it as unresolved with a reason. No final test evaluation may begin until all parameters that can influence treatment or outcomes are frozen and the protocol is versioned.
