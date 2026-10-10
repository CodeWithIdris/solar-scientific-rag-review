# Lit3R — Methodological Screening

Screened paper: Akira Ise, Kotaro Kumagai, Yuta Yamaguchi, Hisanori Ozaki, Yukio Uematsu, and Ikuya Yamada, "Lit3R: Retrieve-Relate-Read for Evidence-Grounded Question Answering over Scientific Literature," arXiv:2609.16912v1, submitted 15 September 2026.

Screening question: Does the paper perform the proposed experiment: BM25 vs dense retrieval vs hybrid retrieval over solar energy scientific literature, using the same corpus, same question set, same generator, with controlled experimental comparison, retrieval metrics, answer quality, evidence/citation attribution, and statistical comparison?

Overall determination: **PARTIAL overlap**. Lit3R is a close methodological neighbor for evidence-grounded QA over scientific literature and explicitly uses BM25, dense retrieval, hybrid RRF fusion, reranking, evidence verification, retrieval metrics, answer metrics, and evidence attribution metrics. It does **not** evaluate solar energy or solar-PV literature, and it does **not** report a controlled BM25-only vs dense-only vs hybrid comparison.

## 1. Research objective

Classification: **RELATED**

Lit3R's objective is to build a system for the LitTraceQA shared task, which requires retrieving relevant papers, identifying supporting evidence, and generating evidence-grounded answers over scientific literature. This is closely related to the proposed study's evidence-grounded scientific QA goal, but Lit3R is not designed to compare lexical, dense, and hybrid retrieval strategies as the primary experimental question.

## 2. Corpus

- source: **RELATED** — recent machine learning, computer vision, and natural language processing conference/venue papers from 2024 and 2025.
- domain: **RELATED** — scientific literature, but not solar energy or solar PV.
- number of documents: **EXACT** — 27,487 papers are reported.
- document type: **EXACT** — scientific paper PDFs converted into structured content.
- date range: **EXACT** — 2024 and 2025 venues.
- preprocessing: **EXACT** — MinerU conversion; body text, tables, figures, equations, and title/abstract chunks; chunks stop at 2,000 characters.

Corpus overlap assessment: **RELATED**. Lit3R uses scientific literature, but the domain is ML/CV/NLP, not solar energy or solar-PV scientific literature.

## 3. Question benchmark

- number: **EXACT** — 55 validation questions and 71 test questions are reported.
- source: **EXACT** — LitTraceQA shared task.
- construction: **NOT REPORTED** — this system paper does not describe LitTraceQA construction in detail.
- question types: **EXACT** — hidden_source_single_paper and multi_paper; end-task output includes multiple-choice and table-answer formats.
- validation: **EXACT** — validation set used for configuration and retriever analysis; official test set used for final leaderboard evaluation.

Question benchmark overlap assessment: **RELATED**. Lit3R has a fixed scientific QA benchmark with evidence labels, but it is not a solar/PV benchmark.

## 4. Retrieval architecture

### BM25

Classification: **EXACT**

Lit3R uses chunk-level BM25 and paper-level BM25. Both BM25 indexes use `k1 = 1.5` and `b = 0.75`.

### Dense retrieval

Classification: **EXACT**

Lit3R uses a dense chunk index built with Qwen3-Embedding-8B. It also uses SPECTER2 for paper-to-paper expansion.

### Hybrid retrieval

Classification: **EXACT**

For each subquery, Lit3R combines chunk-level BM25, paper-level BM25, and dense chunk retrieval into a paper-level ranking with equal-weight RRF.

### Fusion

Classification: **EXACT**

Lit3R uses equal-weight reciprocal rank fusion for paper-level fusion, pseudo-relevance-feedback-expanded rankings, paper-to-paper expansion, and final A/B rank fusion.

### Reranking

Classification: **EXACT**

Lit3R reranks up to 200 chunks per subquery per round with Qwen3-Reranker-8B.

### Retrieval granularity

Classification: **PARTIAL**

The paper uses multiple retrieval granularities: chunk-level BM25, paper-level BM25, dense chunk retrieval, paper-level rankings, paper-to-paper expansion, and top-50 paper candidates. However, it does not report an experimental ablation of retrieval granularity effects.

### Top-k

Classification: **EXACT**

The retriever produces top-50 candidate papers for the reader. Candidate recall is reported at k = 1, 5, 10, 20, and 50. Reranking scores up to 200 chunks, top 20 chunks are pooled, top 20 papers are assessed by the verifier, and paper-to-paper expansion retains top 100 papers before final fusion.

## 5. Generation

Classification: **EXACT**

The system uses Azure OpenAI GPT-5.4 in JSON output mode. The reader receives top-50 candidate papers, the question, answer schema, paper text, figures, and tables. It performs paper-local reading and cross-paper synthesis to produce the answer, paper identifiers, and evidence locators.

Common-generator overlap with proposed experiment: **ABSENT** for retrieval-system comparison. Lit3R uses a common generator in its system, but it does not compare BM25-only, dense-only, and hybrid retrieval arms under that generator.

## 6. Evaluation

### Retrieval

Classification: **EXACT**

Lit3R reports macro recall@k for candidate-paper retrieval on the validation set and paper precision/recall/F1 on the official test set.

### Answer quality

Classification: **PARTIAL**

Lit3R reports multiple-choice accuracy and table-answer metrics. It does not report broad free-form answer correctness or answer relevance as separate general metrics.

### Faithfulness

Classification: **PARTIAL**

The task is evidence-grounded and reports evidence grounding metrics. The paper does not use a separate metric explicitly named faithfulness.

### Citation/evidence

Classification: **PARTIAL**

Lit3R reports evidence precision, evidence recall, and evidence F1. It produces paper identifiers and evidence locators. It does not report citation precision as citation correctness, nor citation completeness under that exact label.

### Efficiency

Classification: **NOT REPORTED**

The paper reports model/inference settings but does not report retrieval latency, generation latency, throughput, runtime, compute cost, or resource usage metrics.

### Statistical analysis

Classification: **ABSENT**

No statistical significance testing is reported for retrieval, answer, or evidence metrics.

## 7. Experimental comparisons

Explicit retrieval comparisons performed:

1. **BM25-only vs dense-only**: **ABSENT**.
2. **BM25-only vs hybrid**: **ABSENT**.
3. **Dense-only vs hybrid**: **ABSENT**.
4. **BM25-only vs dense-only vs hybrid all-three controlled comparison**: **ABSENT**.
5. **Common question set across retrieval systems**: **ABSENT** for BM25/dense/hybrid retrieval systems. The same 55 validation questions are used for final retriever analysis, but not for comparing BM25-only, dense-only, and hybrid arms.
6. **Common generator across retrieval systems**: **ABSENT** for retrieval-arm comparison. The same generator is used in Lit3R, but no retrieval-arm comparison is performed.
7. **Ranking A only vs final system (Ranking A+B)**: **EXACT**. Table 2 compares question-anchored retrieval against the final system with paper-to-paper expansion.
8. **Candidate recall by k and question type**: **EXACT**. Table 1 reports recall@1/5/10/20/50 for single-paper and multi-paper questions.

The controlled comparison in Lit3R is not BM25 vs dense vs hybrid. It is a comparison of Ranking A only against final Ranking A+B paper-to-paper expansion.

## 8. Main results

Classification: **RELATED**

Relevant results:

- Validation candidate recall@50 is 0.968 overall.
- Single-paper questions reach recall@5 of 1.000.
- Multi-paper recall@50 reaches 0.940.
- Adding paper-to-paper expansion improves multi-paper recall@50 from 0.647 to 0.940 and overall recall@50 from 0.814 to 0.968.
- Official test-set paper retrieval macro F1 is 0.992.
- Official test-set evidence F1 is 0.737.
- Multiple-choice accuracy is 1.000.
- Table-answer metrics are lower than retrieval and multiple-choice metrics.

These results are important for evidence-grounded scientific QA, but they do not answer whether BM25, dense, or hybrid retrieval is best over solar/PV scientific literature.

## 9. Limitations

Reported limitations:

- Evaluation is limited to LitTraceQA.
- The same 55 validation questions are used for configuration selection and retriever analysis.
- Generalization to other domains and question types remains untested.
- Experiments do not isolate the contributions of individual expansion signals.
- Experiments do not isolate reader-stage contributions to end-to-end performance.
- The causes of remaining evidence-grounding and table-answering errors are not identified.

Additional limitations relative to the proposed experiment:

- No solar energy or solar-PV corpus.
- No BM25-only arm.
- No dense-only arm.
- No controlled BM25 vs dense vs hybrid comparison.
- No citation precision metric.
- No statistical significance testing.
- No latency/resource evaluation.
- No retrieval granularity ablation.

## 10. Exact overlap with proposed study

| Proposed / requested component | Classification | Determination |
|---|---|---|
| BM25 retrieval | EXACT | Chunk-level BM25 and paper-level BM25 are used. |
| Dense retrieval | EXACT | Qwen3-Embedding-8B dense chunk index is used; SPECTER2 is used for paper expansion. |
| Hybrid retrieval | EXACT | BM25 and dense rankings are fused with RRF. |
| BM25-only vs dense-only comparison | ABSENT | No such comparison is reported. |
| BM25-only vs hybrid comparison | ABSENT | No such comparison is reported. |
| Dense-only vs hybrid comparison | ABSENT | No such comparison is reported. |
| All-three controlled comparison | ABSENT | No BM25-only/dense-only/hybrid three-way comparison is reported. |
| Common question set across retrieval systems | ABSENT | Common questions exist, but not across BM25/dense/hybrid systems. |
| Common generator across retrieval systems | ABSENT | One generator is used, but no retrieval-system comparison is made. |
| Retrieval metrics | EXACT | Recall@k and paper precision/recall/F1 are reported. |
| Answer correctness | PARTIAL | Multiple-choice accuracy and table metrics are reported; broad answer correctness is not separately reported. |
| Answer relevance | NOT REPORTED | No metric explicitly named answer relevance is reported. |
| Faithfulness | PARTIAL | Evidence grounding metrics are reported; no separate faithfulness metric is named. |
| Citation precision | NOT REPORTED | Evidence precision is reported, but citation correctness/precision is not separately reported. |
| Citation completeness/recall | PARTIAL | Evidence recall is reported; citation completeness under that label is not reported. |
| Evidence attribution | EXACT | Evidence precision, recall, and F1 are reported; outputs include evidence locators. |
| Abstention/unanswerable questions | RELATED | The verifier checks whether evidence is sufficient and may trigger more retrieval, but no unanswerable/abstention benchmark is reported. |
| Retrieval latency | NOT REPORTED | No latency metric is reported. |
| Computational/resource evaluation | NOT REPORTED | Model settings are reported, but no cost/resource evaluation metric is reported. |
| Statistical significance testing | ABSENT | No statistical testing is reported. |
| Retrieval-quality vs answer-grounding relationship | PARTIAL | Retrieval and evidence metrics are both reported, and retrieval analysis is component-level, but no statistical linkage is tested. |
| Retrieval granularity effects | PARTIAL | Multiple granularities are used; no granularity ablation is reported. |
| Solar energy scientific literature | ABSENT | Corpus is ML/CV/NLP literature, not solar energy. |

Final overlap classification: **PARTIAL**. Lit3R strongly overlaps on evidence-grounded scientific literature QA architecture and evaluation, but not on solar/PV domain or controlled lexical-vs-dense-vs-hybrid retrieval comparison.

## 11. Components not addressed

Lit3R does not address:

- Solar energy or solar-PV scientific literature.
- BM25-only retrieval evaluation.
- Dense-only retrieval evaluation.
- BM25-only vs dense-only comparison.
- BM25-only vs hybrid comparison.
- Dense-only vs hybrid comparison.
- Three-way BM25/dense/hybrid controlled comparison.
- Same-question/same-generator comparison across BM25-only, dense-only, and hybrid retrieval systems.
- Citation precision as citation correctness.
- Citation recall/completeness under a citation-specific metric.
- Answer relevance as a named metric.
- Unanswerable/abstention benchmark.
- Retrieval latency.
- Computational cost/resource evaluation.
- Statistical significance testing.
- Retrieval granularity ablation.
- Causal or statistical linkage between retrieval quality and answer/evidence grounding.

## 12. Evidence table

| Claim | Page | Section/table/figure | Supporting quotation or precise paraphrase |
|---|---:|---|---|
| Lit3R is a system for literature-grounded QA requiring retrieval, evidence identification, and answer generation. | 1 | Abstract | The abstract says LitTraceQA requires systems to retrieve relevant papers, identify supporting evidence, and generate answers. |
| Lit3R uses BM25, dense retrieval, reranking, and LLM verification. | 1 | Abstract | The abstract states the retriever combines BM25-based sparse and dense retrieval, cross-encoder reranking, and LLM-based verification. |
| Lit3R produces final answers and evidence traces. | 1 | Abstract | The reader identifies supporting evidence and synthesizes across papers to produce the final answer and evidence trace. |
| LitTraceQA evaluates stages separately. | 1 | Introduction | The paper says LitTraceQA evaluates retrieval, evidence identification, and answer generation separately, making evidence trace observable. |
| The system combines BM25 and dense retrieval into a unified candidate ranking. | 1 | Introduction | The paper says BM25-based sparse retrieval and dense retrieval are combined into a unified ranking of candidate papers. |
| The system uses a retrieve-relate-read pipeline. | 1-2 | Method / Figure 1 | Figure 1 shows query decomposition, hybrid retrieval, paper-level fusion, chunk reranking, evidence verification, paper-to-paper expansion, A/B rank fusion, local reading, and cross-paper synthesis. |
| Corpus size is 27,487 papers. | 2 | 2.1.1 Corpus preparation | The corpus contains 27,487 papers from ML, CV, and NLP venues held in 2024 and 2025. |
| The corpus is not solar/PV. | 2 | 2.1.1 Corpus preparation | The corpus is described as recent machine learning, computer vision, and natural language processing venues, not solar or energy literature. |
| PDF preprocessing uses MinerU and structured content extraction. | 2 | 2.1.1 Corpus preparation | The paper says each PDF is converted with MinerU into body text, tables, figures, equations, and title/abstract content. |
| Chunk count is 2,564,545. | 2 | 2.1.1 Corpus preparation | The paper reports 2,564,545 indexed chunks across five chunk types. |
| Chunking stops at 2,000 characters and respects boundaries. | 2 | 2.1.1 Corpus preparation | The paper says splitting respects paragraph, page, and heading boundaries and stops at 2,000 characters. |
| Query decomposition and evidence verification use Azure OpenAI GPT-5.4. | 2 | 2.1.2 Question-anchored retrieval | The paper says both LLM-based steps use the same Azure OpenAI GPT-5.4 model. |
| Retrieval runs for at most three rounds. | 2 | 2.1.2 Question-anchored retrieval | The paper reports iterative retrieval for at most three rounds. |
| First-round query decomposition generates four subqueries. | 2 | 2.1.2 Question-anchored retrieval | The first round generates four subqueries; later rounds generate at most four. |
| Hybrid retrieval uses three indexes. | 2 | 2.1.2 Question-anchored retrieval | For each subquery, the hybrid retrieval step uses chunk-level BM25, paper-level BM25, and dense chunk index. |
| Dense retrieval uses Qwen3-Embedding-8B. | 2 | 2.1.2 Question-anchored retrieval | The dense chunk index is built with Qwen3-Embedding-8B. |
| BM25 parameters are reported. | 2 | 2.1.2 Question-anchored retrieval | Both BM25 indexes use k1 = 1.5 and b = 0.75. |
| Paper-level fusion uses equal-weight RRF. | 2 | 2.1.2 Question-anchored retrieval | The paper-level fusion combines three paper rankings using equal-weight RRF with k = 60. |
| Pseudo-relevance feedback retrieves again with the same three indexes. | 2 | 2.1.2 Question-anchored retrieval | The paper appends title/abstract text from the top-ranked paper, retrieves again with the same three indexes, and fuses original and expanded rankings. |
| Reranking uses Qwen3-Reranker-8B. | 2 | 2.1.2 Question-anchored retrieval | Up to 200 chunks are scored with Qwen3-Reranker-8B. |
| Top 20 chunks enter the pool after reranking/pinning. | 2 | 2.1.2 Question-anchored retrieval | The paper says top 20 retrieval-ranking chunks are pinned and the 20 highest-scoring chunks go to the pool. |
| Evidence verification checks sufficiency but is not an unanswerable benchmark. | 2 | 2.1.2 Question-anchored retrieval | The verifier reports which papers contain evidence, whether the pool contains sufficient evidence, and what is missing. |
| Paper-to-paper expansion uses SPECTER2, bibliographic coupling, and BM25. | 2-3 | 2.1.3 Paper-to-paper expansion | The expansion retrieves neighbors using SPECTER2 title/abstract embeddings, bibliographic coupling, and paper-level BM25. |
| Paper-to-paper expansion uses RRF and retains top 100 papers. | 3 | 2.1.3 Paper-to-paper expansion | The three source-specific lists are fused using equal-weight RRF with k = 60 and top 100 papers are retained. |
| Final A/B fusion returns top 50 papers. | 3 | 2.1.3 Paper-to-paper expansion | Rankings A and B are fused using equal-weight RRF with k = 10; top 50 papers are passed to the reader. |
| Reader outputs paper IDs, evidence locators, and final answer. | 3 | 2.2 Reader | The reader receives top 50 candidate papers and produces paper identifiers, evidence locators, and final answer. |
| Local reading assesses relevance, sufficient evidence, and supporting chunks. | 3 | 2.2.1 Local reading | Each query-paper pair is processed to assess relevance, evidence presence, and supporting chunks. |
| Cross-paper synthesis generates answer and evidence locators. | 3 | 2.2.2 Cross-paper synthesis | The reader extracts facts, source papers, and supporting chunks, and generates the answer in the required format. |
| The validation set has 55 questions. | 4 | 3 Experiments | The paper says 55 validation questions are used to set configuration/hyperparameters and for retriever analysis. |
| The test set has 71 questions. | 4 | 3 Experiments | The paper says 71 test questions are used for final evaluation. |
| Question types are single-paper and multi-paper. | 4 | 3 Experiments | The task defines hidden_source_single_paper and multi_paper questions; validation has 26 and 29 respectively. |
| Retrieval metric is macro recall@k. | 4 | 3 Experiments | The paper reports recall@k as macro average of the fraction of gold evidence papers in top-k candidates. |
| Component-level experiments focus only on retriever. | 4 | 3 Experiments | The paper states component-level experiments focus only on the retriever. |
| Table 1 reports recall@k by question type. | 4 | Table 1 | Table 1 reports candidate recall for k = 1, 5, 10, 20, and 50 for Single, Multi, and All. |
| Table 2 compares Ranking A only vs final system. | 4 | Table 2 | Table 2 reports multi-paper recall@50 improving from 0.647 to 0.940 and all-question recall@50 from 0.814 to 0.968. |
| Table 3 reports official paper retrieval, evidence grounding, and answer metrics. | 5 | Table 3 | Table 3 reports paper precision/recall/F1, evidence precision/recall/F1, multiple-choice accuracy, and table answer metrics. |
| The official paper retrieval macro F1 is 0.992. | 5 | Table 3 / 3.2 Official test-set results | Table 3 reports paper_f1_macro = 0.992. |
| The official evidence F1 is 0.737. | 5 | Table 3 / 3.2 Official test-set results | Table 3 reports evidence_f1_macro = 0.737. |
| Multiple-choice accuracy is 1.000. | 5 | Table 3 | Table 3 reports multiple_choice_accuracy = 1.000. |
| Table answering is weaker than retrieval and multiple-choice. | 5 | Table 3 / 3.2 Official test-set results | Table row F1 is 0.529 and table cell accuracies are 0.309 macro and 0.332 micro. |
| The controlled comparison is paper expansion, not BM25 vs dense vs hybrid. | 5 | Conclusion | The paper says controlled comparison adding paper-to-paper expansion increases multi-paper recall@50 from 0.647 to 0.940. |
| Evaluation is limited to LitTraceQA. | 5 | Limitations | The paper says evaluation is limited to LitTraceQA and generalization to other domains/question types remains untested. |
| Contributions of individual expansion signals and reader stages are not isolated. | 5 | Limitations | The paper says experiments do not isolate individual expansion signals or reader-stage contributions. |
| Causes of evidence-grounding and table-answering errors are not identified. | 5 | Limitations | The limitations state this directly. |
| Model settings are reported, but resource/cost metrics are not. | 6 | Appendix A / Table 4 | Table 4 lists Qwen3-Embedding-8B, Qwen3-Reranker-8B, and Azure OpenAI GPT-5.4, but no latency, cost, or resource metric is provided. |
| No BM25-only vs dense-only vs hybrid comparison is reported. | Not applicable | Whole paper | Precise paraphrase: the method always uses fused hybrid retrieval for the main question-anchored retriever; experiments compare candidate recall by k and Ranking A vs A+B, not separate BM25-only, dense-only, and hybrid arms. |

## A. Exact methodological overlap

- Scientific literature QA.
- Evidence-grounded answer generation.
- Paper retrieval plus evidence identification.
- BM25 retrieval is used.
- Dense retrieval is used.
- Hybrid retrieval with RRF is used.
- Common corpus and question set exist for LitTraceQA evaluation.
- Retrieval metrics are reported.
- Evidence attribution metrics are reported.
- Answer metrics are reported for multiple-choice and table-answer formats.

## B. Partial overlap

- Faithfulness: evidence grounding metrics are present, but no metric explicitly named faithfulness is reported.
- Citation completeness/recall: evidence recall is present, but citation completeness is not separately evaluated.
- Retrieval-quality vs answer-grounding relationship: retrieval and evidence metrics are both reported, but no statistical relationship is tested.
- Retrieval granularity: several granularities are used, but no granularity-effect experiment is reported.
- Abstention/unanswerable: evidence sufficiency is checked inside the iterative verifier, but no unanswerable-question benchmark is evaluated.

## C. Components absent from Lit3R

- Solar energy or solar-PV scientific literature corpus.
- BM25-only vs dense-only comparison.
- BM25-only vs hybrid comparison.
- Dense-only vs hybrid comparison.
- All-three controlled BM25/dense/hybrid comparison.
- Same generator across BM25-only/dense-only/hybrid retrieval arms.
- Citation precision as citation correctness.
- Retrieval latency.
- Computational/resource evaluation.
- Statistical significance testing.

## D. Components present in Lit3R that my proposed study does not currently include

- Retrieve-Relate-Read architecture with paper-to-paper expansion.
- Iterative LLM query decomposition.
- LLM evidence verification before reading.
- Paper-to-paper expansion using SPECTER2, bibliographic coupling, and BM25.
- MinerU-based structured extraction of figures, tables, equations, and title/abstract chunks.
- Separate single-paper vs multi-paper evidence-grounding task structure.
- Table-answer evaluation metrics.

## E. Whether Lit3R makes my current research question substantially less novel

Classification: **PARTIAL pressure, not displacement**.

Lit3R substantially overlaps with the evidence-grounded scientific-literature QA side of the proposed study. It shows that hybrid BM25+dense scientific retrieval, evidence attribution, and single/multi-paper evaluation have already been implemented and evaluated in a non-solar scientific literature benchmark.

However, Lit3R does **not** perform the proposed controlled BM25-only vs dense-only vs hybrid retrieval comparison, and it does **not** study solar energy or solar-PV scientific literature. Therefore, based on screened evidence, it does not already perform the proposed experiment.

## F. What methodological distinction would still remain defensible

Without redesigning the study or claiming novelty, the defensible methodological distinction is:

Lit3R evaluates an evidence-grounded scientific QA system over ML/CV/NLP literature using a hybrid retrieval pipeline and paper-to-paper expansion, whereas the proposed study would evaluate retrieval strategy effects directly by comparing BM25-only, dense-only, and hybrid retrieval under a common solar energy / solar-PV scientific literature corpus, common question set, common generator, and shared evidence/citation evaluation protocol.
