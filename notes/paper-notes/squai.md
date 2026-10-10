# SQuAI — Methodological Screening

Screened paper: Ines Besrour, Jingbo He, Tobias Schreieder, and Michael Faerber, "SQuAI: Scientific Question-Answering with Multi-Agent Retrieval-Augmented Generation," CIKM 2025.

Screening question: Does SQuAI substantially overlap with the proposed study, "Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Energy Scientific Literature"?

Overall determination: **PARTIAL overlap**. SQuAI demonstrates scientific-literature QA with multi-agent RAG, BM25, dense retrieval, hybrid sparse-dense retrieval, answer relevance, contextual relevance, faithfulness evaluation, in-line citations, and citation context. It does **not** study solar energy or solar-PV literature, and it does **not** report a controlled BM25-only vs dense-only vs hybrid retrieval comparison.

# 1. Research objective

Classification: **RELATED**

SQuAI's objective is to provide a scalable and trustworthy multi-agent RAG framework for scientific question answering over arXiv literature. It addresses complex open-domain scientific questions, evidence retrieval across millions of scientific documents, in-line citations, supporting sentences, answer relevance, contextual relevance, and faithfulness.

Overlap with proposed study: SQuAI is strongly related on evidence-grounded scientific QA, but its research objective is not a controlled retrieval-strategy comparison, and its domain is broad arXiv literature rather than solar energy scientific literature.

# 2. Corpus

- source: **EXACT** — unarXive 2024 / arXiv full-text corpus.
- domain: **RELATED** — broad scientific literature, including computer science, mathematics, and physics; not solar energy or solar PV.
- number of documents: **EXACT** — over 2.3 million full-text scientific publications.
- document type: **EXACT** — full-text arXiv papers with metadata, annotated citations, section boundaries, LaTeX equations, and citation network.
- date range: **EXACT** — arXiv papers from 1991 to 2024.
- preprocessing/indexing unit: **PARTIAL** — SQuAI primarily indexes paper abstracts for retrieval; full-text is also evaluated as a generation/evidence condition. The paper does not fully specify chunking or passage segmentation.

Corpus overlap assessment: **RELATED**. SQuAI has a scientific literature corpus at scale, but it is not a solar/PV corpus.

# 3. Question benchmark

- number: **EXACT** — 478 LitSearch questions, 500 unarXive Simple questions, and 500 unarXive Expert questions are reported; the abstract also says a 1,000 scientific question-answer-evidence triplet benchmark is released.
- source: **EXACT** — LitSearch plus two synthetic unarXive benchmarks.
- construction: **PARTIAL** — LitSearch questions come from GPT-4-generated prompts and author-written queries; unarXive Simple and Expert are generated using DeepEval and LLaMA 3.3 70B Instruct.
- question types: **PARTIAL** — long-form scientific QA; LitSearch literature-search questions; unarXive Simple is less complex/general; unarXive Expert is more technical/specific. The paper does not report a taxonomy like single-document vs multi-document, answerable vs unanswerable, or solar question types.
- human-created questions: **PARTIAL** — LitSearch includes author-written queries; unarXive Simple/Expert are synthetic.
- expert validation: **NOT REPORTED** — no expert validation of SQuAI benchmark questions or answers is reported.
- multi-document questions: **RELATED** — the system is designed for evidence aggregation across documents and complex/multi-faceted queries, but the paper does not explicitly label benchmark questions as multi-document.
- unanswerable/insufficient-evidence questions: **NOT REPORTED** — no unanswerable or insufficient-evidence benchmark is reported.

Question benchmark overlap assessment: **RELATED**. SQuAI has scientific QA benchmarks, but not solar/PV questions and not a benchmark for controlled retriever comparison.

# 4. Retrieval methodology

| Forensic item | Classification | Determination |
|---|---|---|
| 1. Does it use BM25? | EXACT | BM25 is explicitly used for sparse retrieval. |
| 2. Does it use dense retrieval? | EXACT | Dense retrieval uses intfloat/e5-base-v2 embeddings. |
| 3. Does it use hybrid retrieval? | EXACT | SQuAI combines sparse and dense retrieval. |
| 4. What exact lexical retriever? | EXACT | BM25. |
| 5. What exact dense retriever/embedding model? | EXACT | intfloat/e5-base-v2 embeddings. |
| 6. What fusion method? | EXACT | Linear interpolation of sparse and dense scores with alpha = 0.35. |
| 7. Does it use reranking? | PARTIAL | Agent-3 filters/ranks Q-A-E triplets using relevance confidence; no separate retrieval reranker such as cross-encoder is reported. |
| 8. What retrieval unit? | PARTIAL | Primarily paper abstracts for indexing; candidate papers/documents are retrieved. Full-text is used in an evaluated condition, but chunk unit is not specified. |
| 9. What top-k? | EXACT | top_k candidate papers per sub-query, adjustable from 3 to 10. |
| 10. Does it compare retrieval strategies experimentally? | ABSENT | It compares standard RAG vs SQuAI and abstract vs full-text settings, but not BM25-only vs dense-only vs hybrid retrieval strategies. |

Retrieval overlap assessment: **PARTIAL**. SQuAI explicitly uses BM25, dense retrieval, and hybrid fusion, but not as controlled experimental arms.

# 5. Generation methodology

Classification: **PARTIAL**

SQuAI uses a four-agent architecture:

- Agent-1 decomposes user queries into simpler sub-questions.
- Hybrid retrieval retrieves top-k documents for each sub-question.
- Agent-2 generates question-answer-evidence triplets for each candidate document.
- Agent-3 judges whether each triplet is relevant/supportive.
- Agent-4 synthesizes the final answer with in-line citations and citation context.

The paper reports that users can select the LLM backend. It does not clearly report the exact answer-generation model used for the experimental runs. The evaluation metrics use LLaMA 3.3 70B Instruct as the LLM judge, but this is not the same as the answer-generation model.

Common-generator comparison assessment: **ABSENT** for the proposed retrieval experiment. SQuAI does not compare BM25-only, dense-only, and hybrid retrieval systems under a common generator.

# 6. Evaluation methodology

| Forensic item | Classification | Determination |
|---|---|---|
| 25. Recall@k? | NOT REPORTED | No Recall@k metric is reported for SQuAI retrieval. |
| 26. MRR? | NOT REPORTED | No MRR is reported. |
| 27. nDCG? | NOT REPORTED | No nDCG is reported. |
| 28. Other retrieval metrics? | PARTIAL | Contextual Relevance evaluates use/relevance of evidence passages, but no standalone retrieval metric is reported. |
| 29. Answer correctness? | PARTIAL | Faithfulness and answer relevance are reported, but no reference-based correctness/accuracy metric is reported. |
| 30. Answer relevance? | EXACT | Answer Relevancy is a reported DeepEval metric. |
| 31. Faithfulness? | EXACT | Faithfulness is a reported DeepEval metric. |
| 32. Citation correctness? | PARTIAL | In-line citations and citation context are generated; faithfulness evaluates support against evidence, but no citation correctness metric is separately reported. |
| 33. Citation completeness? | NOT REPORTED | No citation completeness/recall metric is reported. |
| 34. Evidence attribution? | PARTIAL | Citation context and supporting sentences are provided; no evidence attribution precision/recall/F1 metric is reported. |
| 35. Abstention? | NOT REPORTED | No abstention or insufficient-evidence evaluation is reported. |
| 36. Latency? | NOT REPORTED | No latency metric is reported. |
| 37. Resource/cost evaluation? | PARTIAL | Lower computational overhead of abstract-based generation is claimed, but no explicit cost/resource metric is reported. |
| 38. Statistical significance testing? | ABSENT | No statistical significance testing is reported. |
| 39. Relationship between retrieval quality and answer/evidence quality? | RELATED | The paper argues hybrid retrieval and filtering improve contextual relevance and answer quality, but does not statistically link retrieval metrics to answer/evidence metrics. |

Evaluation overlap assessment: **PARTIAL**. SQuAI evaluates answer relevance, contextual relevance, and faithfulness, but it does not report classical retrieval metrics or citation correctness/completeness metrics.

# 7. Controlled retrieval comparison

| Controlled-comparison item | Classification | Determination |
|---|---|---|
| 11. BM25-only vs dense-only? | ABSENT | Not reported. |
| 12. BM25-only vs hybrid? | ABSENT | Not reported. |
| 13. Dense-only vs hybrid? | ABSENT | Not reported. |
| 14. All three under same experimental conditions? | ABSENT | Not reported. |
| 15. Same question set across retrieval systems? | ABSENT | The same benchmarks are used for standard RAG vs SQuAI, but not for BM25-only/dense-only/hybrid retrieval systems. |
| 16. Same generator across retrieval systems? | ABSENT | No retrieval-system comparison is reported. |

Explicit comparisons performed:

1. **Standard RAG vs SQuAI**: **EXACT** — Table 1 compares Standard RAG against SQuAI on LitSearch, unarXive Simple, and unarXive Expert.
2. **SQuAI Abstract vs SQuAI Full Text**: **EXACT** — Table 1 compares abstract-based and full-text variants.
3. **BM25 vs dense vs hybrid**: **ABSENT** — no such comparison is reported.

# 8. Evidence/citation evaluation

Classification: **PARTIAL**

SQuAI explicitly generates fine-grained in-line citations and citation context. Each factual assertion should be followed by a citation in the standardized `[X]` format, and the model is instructed that every factual sentence must include at least one citation.

However, SQuAI does not separately report:

- citation precision,
- citation recall,
- citation completeness,
- evidence attribution F1,
- source-level citation correctness,
- claim-level citation correctness.

Its closest relevant metrics are Answer Relevancy, Contextual Relevancy, and Faithfulness, judged directly against cited evidence.

# 9. Statistical analysis

Classification: **ABSENT**

No statistical significance testing is reported. Table 1 reports metric scores but no p-values, confidence intervals, standard errors, bootstrap tests, or pairwise significance tests.

# 10. Limitations

Explicit limitations are not presented in a separate limitations section in the screened paper.

Methodological limitations relative to the proposed study:

- No solar energy or solar-PV corpus.
- No controlled BM25-only vs dense-only vs hybrid comparison.
- No retrieval metrics such as Recall@k, MRR, or nDCG.
- No citation precision or citation recall/completeness metric.
- No abstention/unanswerable evaluation.
- No latency metric.
- No explicit resource/cost metric, despite discussing lower computational overhead for abstracts.
- No statistical significance testing.
- Answer-generation model used in experiments is not clearly specified in the paper.
- Retrieval unit is described mostly as abstracts/candidate papers, but chunking/passage unit is not fully specified.

# 11. Exact overlap

Exact methodological overlap with the proposed study:

- Scientific literature QA.
- RAG architecture.
- BM25 retrieval is used.
- Dense retrieval is used.
- Hybrid sparse-dense retrieval is used.
- Evidence-grounded answer generation.
- In-line citations.
- Citation context/supporting sentences.
- Answer relevance evaluation.
- Faithfulness evaluation.
- Contextual relevance evaluation.

Exact overlap with Solar Intelligence:

- Both use BM25.
- Both use dense retrieval.
- Both use hybrid sparse-dense retrieval.
- Both generate cited/evidence-grounded answers.
- Both are RAG systems intended to reduce unsupported answers.

Exact overlap with Lit3R:

- Both target scientific QA.
- Both use BM25 and dense retrieval.
- Both use hybrid retrieval.
- Both use multi-stage pipelines rather than a single simple RAG prompt.
- Both generate evidence-grounded/cited answers.
- Both evaluate evidence-related quality, though with different metrics.

# 12. Partial overlap

Partial overlap with the proposed study:

- Scientific corpus: SQuAI uses arXiv scientific literature, but not solar energy/PV literature.
- Retrieval evaluation: SQuAI evaluates context relevance but does not report classical retrieval metrics.
- Citation evaluation: SQuAI generates citation context and evaluates faithfulness, but does not report citation correctness/completeness.
- Question benchmark: SQuAI has scientific QA benchmarks, but not solar/PV questions and not a retriever-comparison benchmark.
- Resource evaluation: SQuAI discusses abstract-based generation as lower overhead, but does not provide explicit cost/resource metrics.

Partial overlap with Solar Intelligence:

- Solar Intelligence is solar-domain but lacks formal QA metrics; SQuAI has formal answer relevance/contextual relevance/faithfulness metrics but lacks solar domain.
- Solar Intelligence uses RRF; SQuAI uses linear score interpolation.
- Solar Intelligence uses BGE-small/ChromaDB; SQuAI uses intfloat/e5-base-v2.

Partial overlap with Lit3R:

- Lit3R reports classical retrieval and evidence metrics; SQuAI reports LLM-judge answer/context/faithfulness metrics.
- Lit3R uses chunk-level and paper-level retrieval plus paper expansion; SQuAI primarily indexes abstracts and uses candidate papers per sub-query.
- Lit3R has a fixed shared-task evidence benchmark; SQuAI uses LitSearch plus synthetic unarXive Simple/Expert benchmarks.

# 13. Components absent

Components absent from SQuAI relative to the proposed study:

- Solar energy scientific literature.
- Solar-PV-specific corpus.
- BM25-only vs dense-only comparison.
- BM25-only vs hybrid comparison.
- Dense-only vs hybrid comparison.
- All-three BM25/dense/hybrid controlled comparison.
- Same question set across BM25-only/dense-only/hybrid retrieval systems.
- Same generator across BM25-only/dense-only/hybrid retrieval systems.
- Recall@k.
- MRR.
- nDCG.
- Citation precision.
- Citation completeness/recall.
- Abstention/unanswerable evaluation.
- Retrieval latency.
- Explicit computational/resource metric.
- Statistical significance testing.
- Statistical link between retrieval quality and answer/evidence quality.

# 14. Components my proposed study adds

Relative to SQuAI, the proposed study would add or foreground:

- Solar energy / solar-PV scientific literature as the target corpus.
- A controlled retrieval-strategy comparison: BM25-only vs dense-only vs hybrid.
- Same corpus, same question set, and same generator across retrieval systems.
- Classical retrieval metrics such as Recall@k, MRR, and/or nDCG if adopted.
- Citation attribution metrics such as citation precision and citation completeness if adopted.
- Statistical comparison between retrieval strategies if adopted.
- Direct analysis of how retrieval strategy affects answer quality and evidence/citation grounding.

# 15. Impact on the proposed research question

SQuAI shows that scientific QA over a large arXiv corpus can be improved using multi-agent decomposition, hybrid sparse-dense retrieval, adaptive filtering, in-line citations, and faithfulness/contextual-relevance evaluation.

It does **not** close the remaining methodological gap for the proposed study because it does not:

- use solar energy / solar-PV literature,
- perform BM25-only vs dense-only vs hybrid retrieval comparisons,
- report retrieval metrics for those strategies,
- evaluate citation precision/completeness,
- evaluate unanswerable questions,
- report statistical significance testing.

Impact assessment: **SQuAI increases methodological prior art pressure for evidence-grounded scientific QA with hybrid retrieval and citations, but it does not demonstrate the proposed controlled solar-literature retrieval-strategy experiment.**

No novelty claim is made here.

# 16. Evidence table

| Claim | Page | Section/table/figure | Supporting quotation or precise paraphrase |
|---|---:|---|---|
| SQuAI is a multi-agent RAG framework for scientific QA. | 1 | Abstract | The abstract presents SQuAI as a scalable and trustworthy multi-agent RAG framework for scientific QA with LLMs. |
| SQuAI targets complex scholarly questions requiring citations and retrieval across millions of documents. | 1 | Abstract | The abstract says complex open-domain questions demand accurate answers, explicit claims with citations, and retrieval across millions of scientific documents. |
| Corpus size is over 2.3 million full-text arXiv papers. | 1 | Abstract | The abstract states SQuAI is built on over 2.3 million full-text papers from arXiv.org. |
| SQuAI uses hybrid sparse-dense retrieval. | 1 | Abstract | The abstract says four agents decompose questions, retrieve targeted evidence via hybrid sparse-dense retrieval, and filter documents. |
| SQuAI provides in-line citations and supporting sentences. | 1 | Abstract | The abstract says SQuAI integrates in-line citations for each generated claim and provides supporting sentences from source documents. |
| SQuAI reports improvement over a RAG baseline. | 1 | Abstract | The abstract reports improvements in faithfulness, answer relevance, and contextual relevance up to +0.088 (12%) over a strong RAG baseline. |
| SQuAI releases a 1,000 triplet benchmark. | 1 | Abstract | The abstract reports a benchmark of 1,000 scientific question-answer-evidence triplets. |
| SQuAI is built on unarXive 2024. | 1 | Introduction | The paper says the system is built on newly released unarXive 2024. |
| UI allows configuration of sparse, dense, or hybrid retrieval. | 1 | Introduction | The paper says users can configure retrieval systems such as sparse, dense, or hybrid. |
| SQuAI uses all arXiv publications up to 2024. | 2 | Contributions | The contributions state SQuAI is for scientific QA over all arXiv publications up to 2024. |
| SQuAI releases 1,000 Q-A-E triplets. | 2 | Contributions | The paper says it releases a synthetic dataset with 1,000 scientific question-answer-evidence triplets tailored to unarXive 2024. |
| The corpus spans arXiv papers from 1991 to 2024 and includes metadata/citations/sections/equations. | 2 | 3 System Overview | The paper describes unarXive 2024 as all full-text arXiv papers from 1991 to 2024 with metadata, annotated citations, section boundaries, LaTeX equations, and citation network. |
| Agent-1 decomposes queries into sub-questions. | 2 | 3 System Overview / 3.1.1 Agent-1 | The system overview and Agent-1 section describe decomposition of input queries into semantically distinct sub-questions. |
| The retrieval stage selects top-k documents per sub-question. | 2 | 3 System Overview / Figure 1 | The paper says a hybrid retriever selects top-k documents for each sub-question. |
| Hybrid retrieval uses BM25 and intfloat/e5-base-v2. | 3 | 3.1.2 Hybrid Retrieval | The paper states sparse retrieval uses BM25 and dense retrieval uses intfloat/e5-base-v2 embeddings. |
| SQuAI primarily indexes abstracts. | 3 | 3.1.2 Hybrid Retrieval | The paper says it primarily uses paper abstracts for indexing, citing LitSearch findings about marginal gains from full-text retrieval. |
| Hybrid fusion is linear score interpolation. | 3 | 3.1.2 Hybrid Retrieval / Equation 1 | The paper defines `S_hybrid(d) = alpha * S_sparse(d) + (1 - alpha) * S_dense(d)`. |
| Alpha is 0.35. | 3 | 3.1.2 Hybrid Retrieval | The paper sets alpha = 0.35 to slightly favor dense retrieval while preserving sparse signals. |
| top_k is adjustable from 3 to 10. | 3 | 3.1.3 Agent-2 | The paper says top_k candidate papers per sub-query is adjustable between 3 and 10. |
| Agent-3 filters documents using relevance confidence. | 3 | 3.1.4 Agent-3 | Agent-3 evaluates Q-A-E triplets and computes a relevance confidence score from Yes/No output probabilities. |
| Agent-4 generates final answers with citations and citation context. | 3 | 3.1.5 Agent-4 | The paper says Agent-4 synthesizes the final answer and requires precise citation placement. |
| Every factual sentence is instructed to include a citation. | 3 | 3.1.5 Agent-4 | The prompt instructs every factual sentence to include at least one citation and to use diverse sources. |
| UI supports choosing hybrid, sparse, or dense retrieval. | 3 | 3.2 User Interface | The UI allows selection of a retrieval model, such as hybrid, sparse, or dense. |
| Table 1 compares Standard RAG, SQuAI Abstract, and SQuAI Full Text. | 4 | Table 1 | Table 1 reports Answer Relevance, Contextual Relevance, Faithfulness, and average scores on LitSearch, unarXive Simple, and unarXive Expert. |
| Evaluation uses DeepEval LLM-as-a-judge. | 4 | 4 Evaluation | The paper says it uses DeepEval, an open-source LLM-as-a-judge framework with prompt-based metrics. |
| Evaluation uses three benchmarks. | 4 | 4.1 Benchmarks & Metrics | The paper reports LitSearch, unarXive Simple, and unarXive Expert. |
| LitSearch subset has 478 questions. | 4 | 4.1 Benchmarks & Metrics | The paper says it uses a subset of 478 LitSearch questions with at least one arXiv ID as ground truth. |
| unarXive Simple has 500 synthetic questions. | 4 | 4.1 Benchmarks & Metrics | The paper says unarXive Simple contains 500 long-form open-domain questions generated with DeepEval and LLaMA 3.3 70B Instruct. |
| unarXive Expert has 500 synthetic questions. | 4 | 4.1 Benchmarks & Metrics | The paper says unarXive Expert contains 500 more specific and technical questions generated similarly. |
| Metrics are Answer Relevancy, Contextual Relevancy, and Faithfulness. | 4 | 4.1 Benchmarks & Metrics | The paper defines all three metrics and says each outputs scalar scores in [0,1]. |
| Evaluation avoids synthetic reference answers. | 4 | 4.1 Benchmarks & Metrics | The paper says it avoids evaluating against synthetic reference answers and judges answers directly against cited evidence. |
| SQuAI is compared against Standard RAG. | 4 | 4.2 Results | The paper says SQuAI is compared against standard RAG without multi-agent orchestration or query decomposition. |
| SQuAI uses hybrid retrieval in Table 1 results. | 4 | 4.2 Results | The paper says Table 1 shows SQuAI, using hybrid retrieval, consistently improves upon the baseline. |
| Abstract-only variant has larger and more consistent improvements than full-text setting. | 4 | 4.2 Results | The paper reports abstract-only improvements of +0.068 to +0.088 versus full-text improvements of +0.016 to +0.071. |
| Faithfulness remains high. | 4 | 4.2 Results | The paper reports faithfulness scores exceeding 0.95 across all configurations. |
| Abstract-based generation is described as lower overhead. | 4 | 4.2 Results | The paper says abstract-based generation provides strong performance benefits with lower computational overhead. |
| No BM25-only vs dense-only vs hybrid controlled comparison is reported. | Not applicable | Whole paper | Precise paraphrase: the paper reports configurable retrieval modes and hybrid retrieval results, but the experiments compare Standard RAG vs SQuAI and abstracts vs full text, not BM25-only, dense-only, and hybrid retrieval systems. |
| No statistical significance testing is reported. | Not applicable | Whole paper | Precise paraphrase: Table 1 reports metric scores only; no p-values, confidence intervals, standard errors, or significance tests are reported. |
