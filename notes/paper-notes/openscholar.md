# OpenScholar — Forensic Methodological Screening

**Paper:** Akari Asai et al., “Synthesizing scientific literature with retrieval-augmented language models,” arXiv:2411.14199v1 (2024); subsequently published in *Nature* 650 (2026), 857–863, DOI 10.1038/s41586-025-10072-4.  
**Evidence version used here:** arXiv v1 full text and its PDF. The Nature publisher page was not accessible for page-level verification during this screening. Page citations below therefore refer to the arXiv PDF, not to the Nature pagination. The publisher citation is included for bibliographic identification only.  
**Screening question:** What does OpenScholar establish relative to “Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Energy Scientific Literature”?  
**Overall determination:** **PARTIAL overlap.** OpenScholar is a large-scale, multi-domain scientific-literature synthesis system with expert-authored QA, passage-linked citations, and downstream citation/answer evaluation. It does **not** report BM25-only, dense-only, and BM25+dense hybrid conditions as a controlled retriever comparison. Its datastore retriever is dense; external keyword/API and academic-web search results augment candidates and are reranked. Those sources do not establish a BM25+dense hybrid. The paper is not solar/PV-specific.

## Evidence and classification conventions

Every numbered item below is classified **EXACT**, **PARTIAL**, **RELATED**, **ABSENT**, or **NOT REPORTED** relative to what OpenScholar itself establishes for that item. “ABSENT” means the screened paper does not include the requested method/task; “NOT REPORTED” means a potentially relevant detail is not specified. Neither is filled by inference. Locations refer to the arXiv v1 PDF; the cited section/table/figure is the anchor for the claim.

## # 1. Research objective

OpenScholar studies retrieval-augmented language models for synthesizing scientific literature: retrieving relevant passages and producing answers with citations. It evaluates a large scientific datastore, expert-written synthesis tasks, model and system baselines, and components such as retrieval/reranking, feedback, and attribution. This is closely related to scientific evidence-grounded QA, but the experimental objective is not a controlled comparison of BM25-only, dense-only, and hybrid retrieval strategies for solar/PV literature.

**Evidence:** arXiv PDF pp. 1–3, Introduction and overview; pp. 4–6, system/retrieval methods; Fig. 1 system overview.

## # 2. Corpus

| # | Corpus question | Classification | Finding and evidence |
|---:|---|---|---|
| 1 | What scientific literature corpus is used? | EXACT | Open-access scientific literature from peS2o, constructed from S2ORC. For its main datastore OpenScholar uses peS2o v3; evaluation retrieval is performed against peS2o v2. **Evidence:** PDF pp. 4–5, “Datastore”/retrieval method and evaluation setup. |
| 2 | Corpus size? | EXACT | The training/main datastore is described as 45 million papers through October 2024. Methods give 234 million passages; the abstract reports 237 million passage embeddings. Preserve this reported discrepancy; the counts are not silently harmonized. **Evidence:** PDF p. 1, Abstract; pp. 4–5, datastore methods. |
| 3 | Number of papers/documents? | EXACT | 45 million papers for the peS2o v3 corpus. The separate peS2o v2 evaluation datastore has a different cutoff and should not be substituted for that corpus count. **Evidence:** PDF pp. 1, 4–5. |
| 4 | Sources? | EXACT | S2ORC/peS2o for the datastore, plus Semantic Scholar API search and You.com academic web search as additional retrieval sources. **Evidence:** PDF pp. 4–6, retrieval method; Fig. 1. |
| 5 | Date range? | PARTIAL | Main peS2o v3 datastore is described as current through October 2024; the evaluation peS2o v2 datastore is through January 2023. A per-document publication-year distribution/range is not reported in the cited methods. **Evidence:** PDF pp. 4–5. |
| 6 | Domain coverage? | EXACT | Broad scientific literature; the expert-curated benchmark covers computer science, physics, biomedicine, and neuroscience. It also includes multi-paper synthesis tasks. **Evidence:** PDF pp. 7–9, Section 3, Table 1 (`table:overview_dataset`), and the subject-distribution figure. |
| 7 | Is it solar/PV-specific? | ABSENT | No solar- or PV-specific corpus/benchmark is reported. **Evidence:** PDF pp. 7–9, evaluated domains and dataset description. |
| 8 | How are documents processed? | EXACT | Papers are split into 250-word blocks using whitespace word counts, with the paper title prepended to each passage. **Evidence:** PDF pp. 4–5, datastore/passage construction. |
| 9 | What retrieval unit is used? | EXACT | Passage-level dense retrieval over the 250-word blocks. **Evidence:** PDF pp. 4–6, retrieval method. |
| 10 | What evidence unit is used? | EXACT | Retrieved passages are supplied as evidence, and generated inline citations point to the associated passages/papers. **Evidence:** PDF pp. 5–6, generation/citation method; pp. 10–13, citation evaluation. |

**Corpus assessment:** OpenScholar provides broad scientific coverage and a very large passage datastore. The paper does not establish corpus coverage or performance for solar/PV papers in particular.

## # 3. Question benchmark

| # | QA question | Classification | Finding and evidence |
|---:|---|---|---|
| 11 | What QA tasks are evaluated? | EXACT | Expert-designed single-paper tasks and multi-paper literature synthesis, plus adapted SciFact, PubMedQA, and QASA evaluations. **Evidence:** PDF pp. 7–9, Section 3, Table 1 (`table:overview_dataset`), and Fig. `overview_multi_paper_qa`. |
| 12 | Number of questions? | PARTIAL | The abstract reports 2,967 expert-written queries: CS 100, Bio 1,451, Neuro 1,308, and Multi 108. Figure 1's benchmark teaser instead says “2.2k” expert-written questions. The paper does not reconcile these figures; report both, rather than choosing one. The 208 long-form expert answers are CS 100 plus Multi 108. Bio/Neuro contribute 2,759 questions-only, not long-form reference answers. Separately adapted evaluation subsets are SciFact 208, PubMedQA 843, and QASA 1,375. **Evidence:** PDF p. 1, Abstract; Fig. 1 caption; pp. 7–9, Section 3, Table 1 (`table:overview_dataset`) and question/answer collection table (`table:result_human_data`). |
| 13 | Question source? | EXACT | New ScholarQA questions are written by expert annotators; the three top rows in Table 1 are adapted single-paper datasets. Synthetic queries are for training, not the benchmark question source. **Evidence:** PDF pp. 7–9, Section 3, Table 1 and data-curation subsections. |
| 14 | Human-written or synthetic? | PARTIAL | Benchmark questions are expert-written/adapted, not described as synthetic benchmark questions. Synthetic queries/instructions are used in training-data construction. These are separate roles. **Evidence:** PDF pp. 5–6, training-data construction; pp. 7–9, benchmark construction. |
| 15 | Expert validation? | PARTIAL | PhD-level experts create new ScholarQA questions; CS has expert-annotated rubrics (average 4.4 per question), and Multi has expert-written long-form answers. Bio/Neuro are questions-only due to annotation cost. The adopted datasets are not all independently expert-validated by the OpenScholar authors. **Evidence:** PDF pp. 7–9, Section 3, Table 1, ScholarQA-CS example figure, and `table:result_human_data`. |
| 16 | Multi-document questions? | EXACT | Yes. The Multi task is explicitly a multi-paper literature synthesis task; its questions require synthesis across papers. **Evidence:** PDF pp. 7–9, multi-paper task description and dataset table. |
| 17 | Scientific synthesis? | EXACT | Yes. Multi-paper long-form answers synthesize scientific literature. **Evidence:** PDF pp. 7–9, task description; pp. 10–14, multi-paper results. |
| 18 | Unanswerable/insufficient-evidence questions? | NOT REPORTED | A systematic unanswerable/insufficient-evidence benchmark or abstention condition is not reported. **Evidence:** benchmark/task and evaluation descriptions, PDF pp. 7–14. |

**Question-set qualification:** The source reports both 2,967 (abstract) and “2.2k” (Figure 1 caption) expert-written questions, without reconciling the difference. The detailed dataset breakdown gives 100 CS, 1,451 Bio, 1,308 Neuro, and 108 Multi questions (2,967 total). Only 208 are accompanied by long-form expert answers: 100 CS and 108 Multi. Bio/Neuro questions are explicitly questions-only due to annotation cost. The top three rows of Table 1 are adopted single-paper datasets; do not conflate these counts with the newly curated set.

## # 4. Retrieval architecture

| # | Retrieval question | Classification | Finding and evidence |
|---:|---|---|---|
| 19 | What retrieval system is used? | EXACT | Dense passage retrieval over peS2o plus generated-keyword searches through Semantic Scholar and You.com; source candidates are reranked and then passed to the generator. **Evidence:** PDF pp. 4–6, Section 2 retrieval method; retrieval-pipeline panel in Fig. `overview_method_deatils`. |
| 20 | BM25? | ABSENT | BM25 is not reported as a core retrieval method or experimental condition. External keyword/API/web search must not be relabeled BM25. **Evidence:** PDF pp. 4–6, retrieval method. |
| 21 | Dense retrieval? | EXACT | Yes. A dense bi-encoder retrieves passages from the peS2o datastore. **Evidence:** PDF pp. 4–5. |
| 22 | Hybrid retrieval? | PARTIAL | Multiple candidate sources are used (dense datastore retrieval plus external API/web search), but the paper does not define or evaluate a BM25+dense hybrid retriever. **Evidence:** PDF pp. 4–6. |
| 23 | Exact embedding model? | PARTIAL | The retriever is Contriever, continually pretrained on peS2o. The exact released checkpoint identifier is not stated in the main method. **Evidence:** PDF pp. 4–5, Section 2 retrieval method; retriever-training details in the supplement. |
| 24 | Query/document representation? | EXACT | Query and 250-word passage are represented by the dense retriever; the passage includes the paper title prepended to its text. Generated keywords are also used to query the external sources. **Evidence:** PDF pp. 4–6. |
| 25 | Reranking? | EXACT | Yes. Candidates from the retrieval sources are reranked before selection for generation. **Evidence:** PDF pp. 5–6. |
| 26 | Reranker model? | PARTIAL | A fine-tuned BGE-reranker cross-encoder with 340M parameters is described; the exact checkpoint identifier is not reported in the main method. **Evidence:** PDF pp. 5–6, Section 2 retrieval method; reranker-training details in the supplement. |
| 27 | Fusion method? | NOT REPORTED | No explicit score-fusion method (for example, RRF or weighted score fusion) is reported for combining sources. Candidate pooling followed by cross-encoder reranking and citation-count adjustment is not evidence of a separately specified fusion algorithm. **Evidence:** PDF pp. 5–6. |
| 28 | Retrieval granularity? | EXACT | 250-word passage-level retrieval, with at most three passages per paper in the selected set. **Evidence:** PDF pp. 4–6. |
| 29 | Top-k? | EXACT | Dense retrieval returns top 100 passages. Semantic Scholar returns up to 10 papers per generated keyword; You.com returns top 10 results. Final context uses N=5 passages for single-paper tasks and N=10 for multi-paper tasks; iterative feedback can trigger further retrieval. **Evidence:** PDF pp. 5–6, retrieval and generation methods. |
| 30 | Are multiple retrieval strategies directly compared? | ABSENT | The paper does not compare BM25-only, dense-only, and hybrid retriever arms. It reports component/system ablations, not a controlled lexical-vs-dense strategy comparison. **Evidence:** PDF pp. 10–14, Section 4, results table (`table:result_multi`), component-ablation table (`tab:ablatioon`) and analysis/top-N figures (`fig:analysis`, `fig:top_n_ablations_accuracy`, `fig:top_n_ablations_citation`). |

**Critical distinction:** OpenScholar's dense-plus-external-source retrieval pipeline is not a reported BM25+dense hybrid condition. The source/API searches are not specified as BM25; no explicit score-fusion method is reported.

## # 5. Controlled retrieval comparison

| # | Controlled-comparison question | Classification | Finding and evidence |
|---:|---|---|---|
| 31 | BM25-only vs dense-only? | ABSENT | No BM25-only arm compared with a dense-only arm. **Evidence:** retrieval method/results, PDF pp. 4–6, 10–14. |
| 32 | BM25-only vs hybrid? | ABSENT | No BM25-only and BM25+dense hybrid conditions. **Evidence:** PDF pp. 4–6, 10–14. |
| 33 | Dense-only vs hybrid? | ABSENT | No controlled dense-only versus defined BM25+dense hybrid comparison. **Evidence:** PDF pp. 4–6, 10–14. |
| 34 | All three under identical corpus conditions? | ABSENT | No three-arm BM25/dense/hybrid retriever experiment. **Evidence:** PDF pp. 4–6, 10–14. |
| 35 | Same question set? | ABSENT | Because the three retrieval conditions are not present, there is no common question set for that three-way comparison. **Evidence:** evaluation design, PDF pp. 7–14. |
| 36 | Same generator? | ABSENT | No BM25/dense/hybrid QA arms using a common generator are reported. OpenScholar does compare generator/model configurations, but those do not instantiate the requested retriever comparison. **Evidence:** PDF pp. 9–14. |
| 37 | Same prompt? | ABSENT | No matched prompts across the three requested retrieval strategies are reported. **Evidence:** PDF pp. 9–14. |
| 38 | Retrieval strategy as independent variable? | ABSENT | The named independent variable is not BM25-only vs dense-only vs hybrid strategy. Retrieval/reranker, feedback, attribution, and context-size ablations test other system components. **Evidence:** PDF pp. 10–14, ablations. |

**Controlled-comparison assessment:** OpenScholar does not answer whether changing BM25/dense/hybrid retrieval—holding corpus, questions, generator, prompt, and other conditions fixed—changes downstream answer or evidence quality.

## # 6. Generation

| # | Generation question | Classification | Finding and evidence |
|---:|---|---|---|
| 39 | Generator model(s)? | EXACT | OpenScholar-8B is the specialized model; the system is also evaluated with Llama 3.1 70B and GPT-4o configurations. Baseline models include GPT-4o and other LLM systems. Llama 3.1 70B is also used in data generation/training workflows, which should be distinguished from its evaluation use. **Evidence:** PDF pp. 5–6 model/training methods; pp. 9–14 evaluation tables. |
| 40 | Same generator across retrieval conditions? | ABSENT | There are no matched BM25/dense/hybrid downstream QA conditions. Some model comparisons hold the system context/task fixed, but that is not a same-generator retriever-strategy experiment. **Evidence:** PDF pp. 9–14. |
| 41 | Prompting strategy? | EXACT | Retrieval-augmented answer generation with iterative self-feedback/self-critique, up to three feedback sentences, and optional additional retrieval/refinement. **Evidence:** PDF pp. 5–6, generation/feedback method; ablations pp. 11–14. |
| 42 | Citation generation? | EXACT | Generated answers include inline citations tied to retrieved passages/papers. **Evidence:** PDF pp. 5–6, generation method; Fig. 1 and example answers. |
| 43 | Citation verification? | EXACT | A post-hoc model-based citation verification/attribution step is described and evaluated. This is an automated model procedure, not an independent ground-truth guarantee. **Evidence:** PDF pp. 5–6, attribution method; pp. 12–14, attribution results/ablations. |

## # 7. Evidence/citation evaluation

| # | Evaluation question | Classification | Finding and evidence |
|---:|---|---|---|
| 44 | Retrieval metrics? | ABSENT | No standalone retrieval Recall@k, MRR, nDCG, or standard retrieval-precision evaluation is reported. Downstream ablations involving retrieval components do not substitute for retrieval metrics. **Evidence:** evaluation measures/results, PDF pp. 9–14. |
| 45 | Recall@k? | ABSENT | No standalone retrieval Recall@k reported. Citation recall is a separate sentence-level answer citation measure (item 53), not retrieval Recall@k. **Evidence:** PDF pp. 10–14. |
| 46 | MRR? | ABSENT | Not reported. **Evidence:** PDF pp. 9–14. |
| 47 | nDCG? | ABSENT | Not reported. **Evidence:** PDF pp. 9–14. |
| 48 | Answer correctness? | EXACT | Evaluated using task-specific accuracy/correctness measures, including expert rubric scoring for long-form tasks; ROUGE-L is also reported for relevant answer evaluations. **Evidence:** PDF pp. 9–12, Sections 3–4, evaluation protocol and results table (`table:result_multi`). |
| 49 | Answer relevance? | EXACT | Prometheus-based evaluation includes relevance, alongside coverage and organization; human usefulness/preference evaluation is also reported. **Evidence:** PDF pp. 10–14, evaluation metrics and results. |
| 50 | Faithfulness? | PARTIAL | Citation support/precision/recall and hallucinated-citation analyses bear on grounding, but the paper does not report a distinct metric explicitly named faithfulness. **Evidence:** PDF pp. 10–14. |
| 51 | Citation precision? | EXACT | Sentence-level citation precision is reported as part of citation precision/recall/F1 evaluation. **Evidence:** PDF pp. 12–14, attribution evaluation and results. |
| 52 | Citation completeness? | PARTIAL | Sentence-level citation recall measures supported/citation-worthy claims that receive citations and thus bears on completeness; the paper does not name a separate “citation completeness” metric. **Evidence:** PDF pp. 12–14. |
| 53 | Evidence attribution? | EXACT | Inline citations are associated with retrieved evidence; sentence-level attribution/support is evaluated, including citation precision, recall, and F1. **Evidence:** PDF pp. 5–6, 12–14, Sections 2–4; citation-accuracy evaluation and results (`table:result_multi`). |
| 54 | Citation verification? | EXACT | Model-based post-hoc verification is part of the system and is assessed in the attribution analyses/ablations. **Evidence:** PDF pp. 5–6, 12–14. |
| 55 | Abstention? | NOT REPORTED | No systematic abstention or insufficient-evidence evaluation is reported. **Evidence:** PDF pp. 7–14. |
| 56 | Latency? | NOT REPORTED | No systematic retrieval or end-to-end latency evaluation is reported in the screened evaluation. **Evidence:** PDF pp. 9–14. |
| 57 | Computational/resource cost? | PARTIAL | Cost estimates/model or API cost comparisons are discussed, including per-query cost; this is not a comprehensive hardware/resource or controlled retriever-cost evaluation. **Evidence:** PDF pp. 13–15, cost/efficiency discussion and supplement. |
| 58 | Statistical significance testing? | NOT REPORTED | Inferential tests comparing retrieval strategies are not reported. Descriptive use of “significant” is not a statistical test. **Evidence:** PDF pp. 9–14 and tables. |
| 59 | Effect sizes/confidence intervals? | NOT REPORTED | No effect sizes or confidence intervals for the requested retriever-strategy contrast are reported. Inter-annotator agreement and correlations are not confidence intervals/effect tests of retrieval arms. **Evidence:** PDF pp. 9–14. |
| 60 | Retrieval quality vs downstream answer/evidence quality? | PARTIAL | Retrieval/reranker, feedback, attribution, and context-size ablations show component changes associated with answer/citation outcomes. No standalone retrieval-quality metric is statistically linked to downstream quality, and no BM25/dense/hybrid strategy comparison is evaluated this way. **Evidence:** PDF pp. 10–14, ablation and attribution results. |

## # 8. Statistical evaluation

OpenScholar reports several downstream measures, expert assessments, annotator agreement/correlation information, and cost estimates. It does not report inferential significance tests or confidence intervals for a controlled BM25-vs-dense-vs-hybrid contrast, because that contrast is not an experiment in the paper. Descriptive differences and ablation results must not be promoted to significance claims.

**Evidence:** arXiv PDF pp. 9–15, Sections 3–5; results (`table:result_multi`), component ablations (`tab:ablatioon`), analysis/top-N plots (`fig:analysis`, `fig:top_n_ablations_accuracy`, `fig:top_n_ablations_citation`), human evaluation (`table:human_evaluation_results`), and cost discussion.

## # 9. Main findings

OpenScholar demonstrates a large scientific-paper datastore and a passage-retrieval-plus-reranking pipeline supporting citation-backed single- and multi-paper synthesis. The reported experiments compare OpenScholar with other systems/models and examine component ablations, including reranking, feedback, attribution, and context selection. Answer correctness, expert/automated answer quality, and sentence-level citation measures are downstream outcomes. These findings establish the value of the paper's system components within its tested setup; they do not establish the relative downstream effectiveness of BM25-only, dense-only, and hybrid retrieval.

**Evidence:** PDF pp. 9–14, Sections 4–5, results (`table:result_multi`), human evaluation (`table:human_evaluation_results`), component ablations (`tab:ablatioon`), and analysis figure (`fig:analysis`); system overview Fig. 1.

## # 10. Limitations

- Not a solar/PV-specific corpus or question benchmark.
- BM25-only, dense-only, and defined BM25+dense hybrid strategies are not compared.
- No standalone retrieval Recall@k, MRR, or nDCG is reported.
- Multi-source retrieval and reranking do not identify a lexical method or an explicit fusion algorithm.
- No systematic unanswerable-question/abstention benchmark is reported.
- No controlled retriever-strategy significance testing, confidence intervals, or effect-size analysis is reported.
- Corpus passage counts differ between the abstract (237 million passage embeddings) and methods (234 million passages); both numbers are retained here.
- Citation verification is model-based and should not be interpreted as independent ground truth.

**Evidence:** PDF pp. 1, 4–6, 7–15; the paper's discussion/limitations near p. 16.

## # 11. Exact overlap

- Scientific literature as the knowledge source.
- Passage-level evidence retrieval and citation-backed answer generation.
- Single-paper and multi-paper scientific QA/synthesis.
- Downstream evaluation of answer quality and citation attribution.
- Expert-written scientific QA tasks and human/expert evaluation.

This is exact at the broad task-component level, not at the proposed study's controlled retrieval-strategy comparison or solar/PV domain level.

## # 12. Partial overlap

- Retrieval plus generation is present, but the paper's datastore retriever is dense and the candidate pipeline adds external API/web results; it does not define the requested BM25+dense hybrid.
- OpenScholar evaluates retrieval/reranker and other system ablations, but not BM25-only vs dense-only vs hybrid as the independent variable.
- Citation recall is relevant to citation completeness, but no separately named completeness score is established.
- Citation support is relevant to faithfulness, but there is no separately named faithfulness metric.
- Component ablations connect system choices with downstream outcomes, but no standalone retrieval-quality metric is linked to answer/evidence quality for the three proposed retrieval strategies.

## # 13. Components absent from OpenScholar

- Solar/PV-specific scientific corpus and questions.
- BM25-only, dense-only, and BM25+dense hybrid three-way comparison.
- Matched three-way retrieval conditions on identical corpus/questions with fixed generator and prompt.
- Standalone retrieval Recall@k, MRR, and nDCG.
- Systematic unanswerable/insufficient-evidence benchmark and abstention evaluation.
- Inference latency comparison across the requested retrieval strategies.
- Inferential statistical tests, effect sizes, and confidence intervals for such a comparison.

## # 14. Components OpenScholar does better than the proposed study

This is a relative methodological comparison, not a recommendation or redesign. OpenScholar establishes a very large multi-domain datastore, expert-authored and multi-paper scientific synthesis questions, multiple generator/system baselines, model-based iterative feedback, passage-linked citation generation and verification, sentence-level citation precision/recall/F1, expert/automated answer evaluation, and cost estimates. These components are substantially broader than a narrowly scoped solar/PV retrieval-strategy study may include. The proposed study should not imply it is the first to perform scientific-literature QA or citation evaluation.

## # 15. Components the proposed study could legitimately investigate that OpenScholar does not establish

- Whether BM25-only, dense-only, and BM25+dense hybrid retrieval differ in retrieval metrics on one fixed solar/PV scientific corpus and question set.
- Whether any retrieval-level differences carry through a fixed generator/prompt into answer correctness and evidence/citation quality.
- Whether the retrieval/answer/evidence relationship varies by solar-PV question type or evidence need.
- Whether those strategy differences are statistically supported and have meaningful effect sizes.
- Whether conditions lacking adequate evidence are recognized and handled with abstention, if that is in scope.

These are descriptions of the methodological gap in this comparison, not a novelty claim and not a proposed redesign.

## # 16. Impact on the proposed research question

OpenScholar materially narrows any broad claim that scientific literature RAG, synthesis QA, or citation-grounded evaluation is unstudied. It does **not** establish the proposed controlled comparison of BM25-only, dense-only, and hybrid retrieval carried through downstream evidence-grounded QA in a solar/PV corpus.

The key distinction is between **retrieval-level** and **downstream RAG/QA** evidence:

- **Retrieval-level:** IRPAPERS already compares BM25-only, Arctic 2.0 dense-only, and hybrid retrieval on the same scientific-page corpus and question benchmark. Therefore the general scientific-literature retrieval comparison itself is not absent.
- **Downstream RAG/QA:** IRPAPERS does not carry all three text retrieval arms into a same-generator QA comparison. OpenScholar evaluates downstream scientific QA and citation attribution, but does not compare those three retrieval strategies.
- **Domain-specific:** Solar Intelligence uses hybrid retrieval for solar literature but does not provide a controlled three-way retrieval experiment.

**Conclusion:** OpenScholar does not eliminate the narrower methodological question of whether controlled retriever choice changes downstream answer/evidence-grounding outcomes, especially on solar/PV literature. This screening does not claim that the question is novel.

## Evidence source and scope note

Detailed method claims above were screened against the public arXiv full text, arXiv:2411.14199v1. The final Nature bibliographic record is noted, but the publisher full text was inaccessible for page-by-page verification during screening. Page references are therefore explicitly to the arXiv PDF. Supporting anchors include the abstract (p. 1), system overview (Fig. 1), datastore/retrieval/generation methods (pp. 4–6), benchmark and evaluation methods (pp. 7–9), results/ablations/citation evaluation (pp. 9–14), and discussion/limitations (around p. 16). Supplementary material is cited only for model/training details where noted; no unstated model checkpoint or fusion algorithm is inferred.
