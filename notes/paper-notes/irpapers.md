# IRPAPERS — Methodological Screening

Screened paper: Connor Shorten, Augustas Skaburskas, Daniel M. Jones, Charles Pierse, Roberto Esposito, John Trengrove, Etienne Dilocker, and Bob van Luijt, "IRPAPERS: A Visual Document Benchmark for Scientific Retrieval and Question Answering," arXiv:2602.17687v1, submitted 5 February 2026.

Screening question: Does IRPAPERS already perform or enable an experiment substantially equivalent to "Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Energy Scientific Literature"?

Overall determination: **PARTIAL overlap**. IRPAPERS evaluates BM25-only, dense-only, and hybrid text retrieval on the same scientific-paper page corpus and 180-question benchmark, alongside image and multimodal retrieval. It also evaluates downstream QA, but only compares hybrid TextRAG with image-based RAG and retrieval-depth/baseline conditions; it does not carry BM25-only, dense-only, and hybrid text retrieval through the same generator as three QA arms. Its corpus is information-retrieval literature, not solar/PV literature, and its answer metric is reference-answer alignment rather than evidence/citation attribution.

# 1. Research objective

Classification: **RELATED**

IRPAPERS evaluates visual document retrieval and question answering over scientific papers. Its central research question is how image-based document retrieval and QA compare with text-based methods, including OCR text, BM25, dense embeddings, hybrid text search, and multimodal hybrid search.

Overlap with proposed study: It overlaps strongly on retrieval strategy evaluation and scientific-document QA, but the objective is visual-vs-text/multimodal scientific retrieval, not solar-energy literature and not lexical-vs-dense-vs-hybrid text retrieval as the primary experimental variable.

# 2. Corpus

| Corpus item | Classification | Determination |
|---|---|---|
| 1. What scientific documents are used? | EXACT | 166 scientific papers focused on information retrieval, sourced from papers cited by "Large Language Models for Information Retrieval: A Survey." |
| 2. Corpus size? | EXACT | 166 papers, 3,230 pages. |
| 3. Domain? | EXACT | Information retrieval scientific literature. |
| 4. Document structure? | EXACT | Page images plus GPT-4.1 OCR/text transcription for each page; retrieval unit is page-level. |
| 5. Are documents peer-reviewed scientific papers? | PARTIAL | The corpus consists of scientific papers, but the paper does not verify peer-review status for each included document. |
| 6. Is corpus solar/PV-specific? | ABSENT | The corpus is information retrieval literature, not solar/PV literature. |

Corpus overlap assessment: **RELATED**. It is scientific literature, but not solar or PV literature.

# 3. Question benchmark

| QA item | Classification | Determination |
|---|---|---|
| 24. Number of questions? | EXACT | 180 curated questions. |
| 25. Question types? | PARTIAL | The 180-question set targets precise methodological details with needle-in-the-haystack queries. Separate visual-question analyses include 30 questions about visual elements and 10 about a t-SNE plot; this is not a complete taxonomy of the 180-question benchmark. |
| 26. Human-created? | PARTIAL | Questions are generated using Claude Sonnet 4.5 with a prompt; "curated" is reported, but human-authorship details are not fully specified. |
| 27. Expert validated? | NOT REPORTED | Expert validation is not reported. |
| 28. Multi-document? | PARTIAL | Questions are constructed with a single gold source page and are not labeled as multi-document; the paper reports that k=5 RAG exceeds the oracle single-page condition, suggesting additional retrieved pages can contribute. |
| 29. Scientific literature QA? | EXACT | The benchmark evaluates retrieval and QA over scientific papers. |
| 30. Unanswerable questions? | ABSENT | No unanswerable or insufficient-evidence question set is reported; no-retrieval and hard-negative baselines test difficulty, not abstention. |

Question benchmark overlap assessment: **RELATED**. It has a fixed scientific QA benchmark, but not solar/PV questions.

# 4. Retrieval methodology

| Retrieval item | Classification | Determination |
|---|---|---|
| 7. BM25? | EXACT | BM25 sparse retrieval is evaluated. |
| 8. Dense retrieval? | EXACT | Arctic 2.0 dense text embeddings and multiple image embedding models are evaluated. |
| 9. Hybrid retrieval? | EXACT | Hybrid text search combines BM25 and Arctic 2.0; multimodal hybrid search combines BM25, Arctic 2.0, and image retrieval. |
| 10. Exact embedding model? | EXACT | Arctic 2.0 for text; ColModernVBERT, ColPali, ColQwen2 for open-source image; Cohere Embed v4 images and Voyage 3 Large text for closed-source comparison. |
| 11. Exact lexical method? | EXACT | BM25. |
| 12. Fusion method? | EXACT | Relative Score Fusion and Reciprocal Rank Fusion are evaluated; Weaviate relative score fusion is used for hybrid text retrieval. |
| 13. Reranking? | PARTIAL | MUVERA retrieves approximate candidates and rescoring uses exact MaxSim over original multi-vector representations. No LLM/cross-encoder reranker is reported for text RAG. |
| 14. Retrieval granularity? | EXACT | Page-level retrieval over page images and OCR text transcriptions. |
| 15. Top-k? | EXACT | Retrieval reports Recall@1, Recall@5, and Recall@20; QA evaluates k=1 and k=5, plus oracle/hard-negative/no-retrieval baselines. |

Retrieval overlap assessment: **PARTIAL**. IRPAPERS directly evaluates BM25, dense, hybrid, and multimodal hybrid retrieval over scientific documents, but at page level and in an IR corpus.

# 5. Generation methodology

Classification: **PARTIAL**

IRPAPERS evaluates RAG with GPT-4.1 as the reader model. ImageRAG retrieves page images using ColModernVBERT and passes images directly to GPT-4.1. TextRAG retrieves OCR transcriptions using hybrid text retrieval and passes text to GPT-4.1. Both use identical generation prompts and evaluation protocols to isolate modality and retrieval-depth effects.

Overlap with proposed study: IRPAPERS has a controlled same-reader setup for ImageRAG vs TextRAG and k-depth comparison, but does not compare BM25-only, dense-only, and hybrid text retrieval through the same generator.

# 6. Evaluation methodology

| Evaluation item | Classification | Determination |
|---|---|---|
| 31. Recall@k? | EXACT | Recall@1, Recall@5, and Recall@20 are reported. |
| 32. MRR? | NOT REPORTED | MRR is not reported. |
| 33. nDCG? | NOT REPORTED | IRPAPERS explicitly contrasts its Recall@K with ViDoRe's nDCG@10 but does not report nDCG. |
| 34. Other retrieval metrics? | PARTIAL | Success@K is identified as equivalent to Recall@K in single-relevance settings; exclusive-success counts are also discussed. |
| 35. Answer correctness? | PARTIAL | Alignment score measures semantic equivalence to reference answer; not a broader correctness rubric. |
| 36. Answer relevance? | NOT REPORTED | No answer relevance metric is reported. |
| 37. Faithfulness? | NOT REPORTED | No faithfulness metric is reported. |
| 38. Citation precision? | ABSENT | Citation precision is not evaluated. |
| 39. Citation completeness? | ABSENT | Citation completeness/recall is not evaluated. |
| 40. Evidence attribution? | PARTIAL | Retrieval gold page and hard-negative/oracle baselines support evidence grounding, but no evidence attribution precision/recall metric is reported. |
| 41. Abstention? | ABSENT | No abstention evaluation is reported. |
| 42. Latency? | PARTIAL | OCR latency and preprocessing timing are reported; retrieval/query latency is not systematically reported. |
| 43. Resource/cost? | EXACT | Storage, token counts, OCR cost, MUVERA memory reduction, and token cost by k are reported. |
| 44. Statistical significance testing? | ABSENT | No significance testing is reported. |
| 45. Retrieval-quality vs downstream answer/evidence quality? | PARTIAL | Retrieval depth and modality are evaluated downstream in QA; k=5 outperforms k=1/oracle single-page in QA. No statistical model links retrieval quality to answer/evidence quality. |

Evaluation overlap assessment: **PARTIAL**. IRPAPERS is stronger than many screened papers on retrieval metrics and resource/cost, but it lacks citation/faithfulness/statistical testing.

# 7. Controlled retrieval comparison

| Controlled-comparison item | Classification | Determination |
|---|---|---|
| 16. BM25-only vs dense-only? | EXACT | Both are evaluated as retrieval systems on the same IRPAPERS page corpus and 180 questions; the paper reports Recall@K results. This comparison is retrieval-only, not a pair of downstream QA arms. |
| 17. BM25-only vs hybrid? | EXACT | BM25-only and hybrid text retrieval (BM25 + Arctic 2.0) are evaluated on the same retrieval benchmark. The paper does not separately pass these two result sets to the generator for an answer-quality comparison. |
| 18. Dense-only vs hybrid? | EXACT | Arctic 2.0 dense retrieval and hybrid text retrieval are evaluated on the same retrieval benchmark. The paper does not separately pass these two result sets to the generator for an answer-quality comparison. |
| 19. All three under identical conditions? | EXACT | BM25-only, Arctic 2.0 dense-only, and hybrid text retrieval are assessed against the same 166-paper/3,230-page corpus and 180-question benchmark at the retrieval level. They are not evaluated as three same-generator RAG arms. |
| 20. Same corpus? | EXACT | All retrieval systems operate on IRPAPERS pages. |
| 21. Same question set? | EXACT | Retrieval systems are evaluated on the same 180 questions. |
| 22. Same generator? | PARTIAL | ImageRAG and TextRAG both use GPT-4.1, but BM25-only/dense-only/hybrid text retrieval are not separately propagated as RAG generator arms. |
| 23. Is retrieval strategy itself treated as an experimental variable? | EXACT | Yes at the retrieval level: BM25, Arctic 2.0 dense, hybrid text, image, multimodal hybrid, fusion, model variants, and retrieval depth are varied. The downstream QA comparison varies modality/depth, not the three text-only retrieval strategies. |

Explicit comparisons performed:

1. Text-based retrieval vs image-based retrieval.
2. Hybrid text search vs ColModernVBERT image retrieval.
3. Multimodal hybrid search vs unimodal text/image retrieval.
4. RSF vs RRF fusion strategies across alpha values.
5. ColModernVBERT vs ColPali vs ColQwen2 image retrieval.
6. MUVERA encoding at ef=1024/512/256 vs no MUVERA.
7. Cohere Embed v4 image embeddings vs Voyage 3 Large text embeddings and their multimodal hybrid.
8. ImageRAG vs TextRAG at k=1 and k=5.
9. No Retrieval vs Hard Negative vs Oracle Retrieval vs retrieved RAG.

Not performed as central experiment:

- BM25-only vs dense-only vs hybrid text retrieval propagated to RAG answer/citation/evidence outcomes.

# 8. Evidence/citation evaluation

Classification: **PARTIAL**

IRPAPERS has single gold pages for retrieval and reference answers for QA. It evaluates whether a RAG answer semantically matches the reference answer, and it uses hard-negative and oracle retrieval to test whether retrieval actually matters.

It does not evaluate citation precision, citation completeness, citation correctness, claim-level attribution, source attribution F1, or evidence locator precision/recall.

# 9. Statistical analysis

Classification: **ABSENT**

No p-values, confidence intervals, bootstrap tests, standard errors, or statistical significance tests are reported. The LLM-as-judge is run three times with majority vote to reduce judgment variance, but this is not a statistical significance test.

# 10. Limitations

Reported/explicit limitations and future-work signals:

- IRPAPERS is constrained to the information retrieval community, not all scientific disciplines.
- Visual question analysis is limited by dataset scale and the rarity of abstract visualizations in IR papers.
- The paper leaves representation-level fusion to future work.
- It leaves alternative OCR transcription approaches to future work.
- It leaves testing whether ImageRAG/TextRAG gaps persist across reader models to future work.

Limitations relative to the proposed study:

- No solar/PV corpus.
- No citation attribution metrics.
- No answer faithfulness metric.
- No answer relevance metric.
- No unanswerable/abstention evaluation.
- No statistical testing.
- BM25/dense/hybrid text retrieval is not propagated as the central same-generator RAG comparison.

# 11. Exact overlap

There is no exact end-to-end match to the proposed study. Exact overlap exists at the component level:

- Scientific literature corpus.
- Fixed question set.
- Retrieval strategy is experimentally varied.
- BM25-only, dense-only, and hybrid text retrieval are compared on the same IRPAPERS corpus and questions at the retrieval level.
- Retrieval metrics are reported.
- Downstream RAG QA is evaluated.
- The same reader model is used for ImageRAG vs TextRAG, not for a three-way text-retrieval QA comparison.
- Retrieval depth is evaluated.
- Resource/cost tradeoffs are evaluated.

# 12. Partial overlap

Partial overlap with the proposed study:

- Domain: scientific literature, but information retrieval rather than solar/PV.
- Retrieval comparison: a BM25-only/dense-only/hybrid comparison exists at the retrieval level, but is not propagated as three RAG answer-generation arms.
- QA: scientific QA over paper pages, but primarily needle-in-the-haystack methodological questions.
- Evidence grounding: gold page and oracle/hard-negative baselines are used, but citation/evidence attribution metrics are absent.
- Retrieval-quality vs answer quality: retrieval depth and modality affect answer alignment, but no formal statistical linkage is reported.

# 13. Components absent

Components absent from IRPAPERS relative to the proposed study:

- Solar energy or solar-PV scientific literature.
- Citation precision.
- Citation recall/completeness.
- Claim-level citation correctness.
- Evidence attribution precision/recall/F1.
- Faithfulness metric.
- Answer relevance metric.
- Abstention/unanswerable evaluation.
- MRR.
- nDCG.
- Statistical significance testing.
- Same-generator BM25-only vs dense-only vs hybrid RAG answer comparison.

# 14. Components my proposed study adds

Relative to IRPAPERS, the proposed study would add or foreground:

- Solar energy / solar-PV scientific literature.
- A solar/PV-domain BM25-only vs dense-only vs hybrid comparison carried through same-generator QA outcomes, rather than only retrieval-quality evaluation.
- Evidence/citation attribution evaluation if adopted.
- Faithfulness and answer relevance/correctness evaluation if adopted.
- Statistical comparison between retrieval strategies if adopted.
- A focus on solar/PV scientific question types rather than IR-methodology needle-in-the-haystack questions.

# 15. Impact on the proposed research question

IRPAPERS materially strengthens prior art for controlled retrieval evaluation over scientific papers. It demonstrates that:

- BM25, dense, hybrid, image, and multimodal retrieval can be compared on a fixed scientific-paper corpus.
- Retrieval modality and depth affect downstream RAG answer alignment; the text retrieval strategies are not separately compared through the generator.
- Resource/cost and representation tradeoffs can be measured.
- Page-level scientific-paper retrieval is a viable benchmark design.

IRPAPERS does **not** close the proposed methodological gap because it does not study solar/PV literature and does not carry its BM25-only/dense-only/hybrid retrieval comparison through same-generator RAG arms with answer faithfulness and citation-attribution metrics.

Impact assessment: **IRPAPERS materially weakens any broad claim that controlled retrieval-strategy evaluation over scientific literature is unstudied, but it does not eliminate the narrower solar/PV evidence-grounded QA retrieval-comparison question.**

No novelty claim is made here.

# 16. Evidence table

| Claim | Page | Section/table/figure | Supporting quotation or precise paraphrase |
|---|---:|---|---|
| IRPAPERS is a visual document benchmark for scientific retrieval and QA. | 1 | Abstract | The abstract presents IRPAPERS as a benchmark for retrieval and question answering over scientific papers. |
| Corpus size is 166 scientific papers and 3,230 pages. | 1 | Abstract | The abstract reports 3,230 pages sourced from 166 scientific papers. |
| Question count is 180. | 1 | Abstract | The abstract reports 180 needle-in-the-haystack questions. |
| The benchmark includes image and OCR transcription for each page. | 1 | Abstract | The abstract says each page has both an image and OCR transcription. |
| Text retrieval evaluates Arctic 2.0 dense embeddings, BM25, and hybrid text search. | 1 | Abstract | The abstract states text retrieval evaluates Arctic 2.0 dense single-vector embeddings, BM25, and their hybrid combination. |
| Image retrieval evaluates ColModernVBERT. | 1 | Abstract | The abstract says image retrieval evaluates the ColModernVBERT multi-vector embedding model. |
| Multimodal hybrid search outperforms unimodal methods. | 1 | Abstract | The abstract reports multimodal hybrid search at 49% Recall@1, 81% Recall@5, and 95% Recall@20. |
| QA uses LLM-as-judge semantic equivalence. | 1 | Abstract | The abstract says QA evaluation uses an LLM-as-Judge for binary semantic equivalence between ground truth and system answer. |
| TextRAG and ImageRAG are compared. | 1 | Abstract | The abstract reports text inputs score 0.82 and image inputs 0.71. |
| Five retrieved documents outperform oracle single-document retrieval. | 1 | Abstract | The abstract states retrieving five documents outperforms oracle single-document retrieval. |
| Scientific papers are inherently visual documents. | 2 | Introduction | The paper notes scientific papers encode meaning through layout, figures, equations, and diagrams. |
| Corpus papers are sourced from citations of an LLM-for-IR survey. | 2 | Introduction | The benchmark uses papers from citations of a comprehensive survey of large language models for information retrieval. |
| Corpus domain is information retrieval. | 4 | 2 IRPAPERS Dataset | The paper introduces 166 scientific papers focused on Information Retrieval. |
| The corpus is constrained to a single research community. | 4 | 2 IRPAPERS Dataset | The paper contrasts IRPAPERS with broad corpora and says it is constrained to a single research community. |
| Questions are constructed from 19 query-writing papers. | 4 | 2 IRPAPERS Dataset | The paper says questions are constructed from 19 papers focused on Query Writing. |
| Questions are generated using Claude Sonnet 4.5. | 4 | 2 IRPAPERS Dataset | The paper says each paper is fed to Claude chat application using Claude Sonnet 4.5 with an appendix prompt. |
| One question is constructed per non-reference page. | 4 | 2 IRPAPERS Dataset | The paper says it constructs one question for each page, skipping reference-only pages. |
| Query discriminativeness is validated with hard negatives. | 4 | 2 IRPAPERS Dataset | The paper says hard-negative degradation suggests most questions require the specific source page. |
| Page images are stored as base64 strings and storage/timing are measured. | 4 | 2 IRPAPERS Dataset | The paper reports 1.3 MB/page, 4.2 GB total, 130 ms/page, and 420 seconds CPU work. |
| OCR transcription uses GPT-4.1 and cost is measured. | 4-5 | 2 IRPAPERS Dataset | The paper reports 25 seconds/page, token counts, and $54.08 transcription cost for the full corpus. |
| Text retrieval evaluates BM25, dense retrieval, and hybrid search. | 5 | 3.1 Text Retrieval | The paper states it evaluates sparse lexical retrieval, dense embeddings, and their combination with hybrid search. |
| BM25-only, dense-only, and hybrid text retrieval share the same retrieval benchmark conditions. | 5, 7-8 | 3.1 Text Retrieval; 3.6 Experimental Methodology; 4.1 Retrieval Results | The three text retrieval variants are evaluated against the same corpus and 180 benchmark queries, and retrieval results are reported using Recall@K; the comparison is not propagated into three QA generator arms. |
| Image retrieval uses late-interaction models. | 5 | 3.2 Image Retrieval with Late Interaction | The paper describes ColModernVBERT, ColPali, and ColQwen2 as multi-vector image embedding models. |
| MUVERA uses approximate candidate retrieval plus exact MaxSim rescoring. | 6 | 3.3 Efficient Late Interaction with MUVERA | The paper describes HNSW retrieval of top ef candidates followed by exact MaxSim rescoring. |
| Multimodal hybrid combines BM25, Arctic 2.0, and ColModernVBERT. | 7 | 3.4 Multimodal Hybrid Search | The paper says it combines BM25 sparse retrieval, Arctic 2.0 dense text embeddings, and ColModernVBERT image embeddings. |
| Fusion methods include RSF and RRF. | 7 | 3.4 Multimodal Hybrid Search | The paper describes Relative Score Fusion and Reciprocal Rank Fusion. |
| Hybrid text search uses equal weighting of BM25 and Arctic 2.0. | 7 | 3.4 Multimodal Hybrid Search | The paper says hybrid text search fuses BM25 and Arctic 2.0 with equal weighting. |
| ImageRAG and TextRAG use the same reader model/protocol. | 7 | 3.5 Question Answering with RAG | The paper says both configurations use identical generation prompts and evaluation protocols. |
| Recall@K is the retrieval metric. | 7 | 3.6 Experimental Methodology | The paper reports Recall@K, also known as Success@K in single-relevance settings. |
| Text embeddings use Arctic 2.0 and image embeddings use ColModernVBERT. | 7 | 3.6 Experimental Methodology | The paper reports Arctic 2.0 1,024-dimensional embeddings and ColModernVBERT multi-vector image embeddings. |
| HNSW ef is fixed for single-vector retrieval. | 7 | 3.6 Experimental Methodology | All HNSW-based retrieval systems with single-vector representations use ef = 160. |
| ImageRAG uses ColModernVBERT and GPT-4.1. | 7 | 3.6 Experimental Methodology | ImageRAG retrieves page images using ColModernVBERT and passes them to GPT-4.1. |
| TextRAG uses hybrid text search and GPT-4.1. | 7 | 3.6 Experimental Methodology | TextRAG retrieves OCR text with hybrid text search and passes text to GPT-4.1. |
| QA judge runs three times with majority vote. | 7 | 3.6 Experimental Methodology | The judge runs three times with independent sampling and takes majority vote. |
| Hybrid text achieves 46% Recall@1 and ColModernVBERT 43% Recall@1. | 8 | 4.1 Retrieval Results | The results section reports hybrid text at 46% Recall@1 and ColModernVBERT at 43% Recall@1. |
| Multimodal hybrid RSF reaches 49% Recall@1. | 8 | 4.1 Retrieval Results / Figure 3 | The paper says multimodal hybrid RSF achieves 49% Recall@1. |
| ColPali and ColQwen2 are compared. | 10 | Table 2 | Table 2 reports ColModernVBERT, ColPali, and ColQwen2 Recall@1/5/20. |
| MUVERA efficiency-quality tradeoff is evaluated. | 10 | Table 3 | Table 3 reports ColModernVBERT no-MUVERA vs MUVERA ef=1024/512/256. |
| Closed-source retrievers are evaluated. | 11 | Table 4 | Table 4 reports Cohere Embed v4 images, Voyage 3 Large text, and multimodal hybrid search. |
| QA baselines include no retrieval, hard negative, and oracle retrieval. | 10 | 4.2 Question Answering Results | The paper defines No Retrieval, Hard Negative, and Oracle Retrieval baselines. |
| TextRAG at k=5 scores 0.82 and ImageRAG at k=5 scores 0.71. | 10 | 4.2 / Table 5 | The paper reports TextRAG 0.82 and ImageRAG 0.71 alignment at k=5. |
| Token cost increases with k. | 10 | 4.2 / Table 5 | Input tokens rise from 1,366 to 6,022 for text and from 1,228 to 5,200 for images when k increases from 1 to 5. |
| Text and image representations have complementary failures. | 10-11 | 5 Limitations of Unimodal Representations | The paper reports text succeeds on 22 queries where image fails, while image succeeds on 18 where text fails. |
| BM25 contributes exact lexical matching. | 12 | 5 Limitations of Unimodal Representations | The paper says BM25 contributes meaningfully to hybrid text search by providing exact lexical matching. |
| Visual question analysis is limited. | 12 | 5 Limitations of Unimodal Representations | The paper says the visual question analysis is limited by dataset scale and the rarity of abstract visualizations. |
| Conclusion restates corpus, retrieval, and QA findings. | 14 | 7 Conclusion | The conclusion reports 166 IR papers, 3,230 pages, 180 questions, hybrid text 46% Recall@1, multimodal hybrid 49% Recall@1 and 95% Recall@20, and TextRAG 0.82 vs ImageRAG 0.71 at k=5. |

# A. What IRPAPERS already establishes

- A reproducible benchmark over scientific papers can compare retrieval representations and strategies.
- BM25-only, Arctic 2.0 dense-only, and hybrid text retrieval are evaluated on the same corpus and question set at the retrieval level, alongside image and multimodal retrieval.
- Recall@K is reported for retrieval over scientific-paper pages.
- Retrieval modality and retrieval depth affect downstream RAG answer alignment.
- Same-reader RAG comparisons can isolate context modality/depth effects.
- Storage, preprocessing latency, token usage, and OCR costs can be reported as part of retrieval/QA methodology.
- The retrieval-level three-way text comparison is not carried through to three same-generator RAG answer arms.

# B. What it does not establish

- It does not establish results over solar/PV scientific literature.
- It does not establish citation correctness/completeness.
- It does not establish faithfulness or answer relevance metrics.
- It does not establish unanswerable/abstention behavior.
- It does not establish statistical significance.
- It does not evaluate BM25-only, dense-only, and hybrid text retrieval as three same-generator RAG arms.

# C. Exact overlap with the proposed study

There is no exact end-to-end match to the proposed experiment. The following components overlap exactly at the methodological-component level:

- Scientific document retrieval.
- Scientific QA/RAG.
- BM25-only, dense-only, and hybrid text retrieval are each evaluated at the retrieval level on the same corpus and question set.
- Retrieval metrics.
- A fixed question set and common corpus are used for the retrieval arms within IRPAPERS.
- A shared reader model is used for its ImageRAG-vs-TextRAG comparison, not for three text-retrieval arms.
- Retrieval-depth effects.
- Resource/cost analysis.

# D. Partial overlap

- It includes a controlled BM25/dense/hybrid retrieval-level comparison, but the main downstream QA comparison is text-vs-image modality rather than retrieval strategy.
- It evaluates answer alignment, but not answer relevance, faithfulness, or citation attribution.
- It uses scientific literature, but not solar/PV literature.
- It uses page-level retrieval, whereas the proposed study may use papers/passages/chunks.

# E. Components that remain different

- Domain: information retrieval papers vs solar energy/PV papers.
- Corpus: 166 papers/3,230 pages vs a solar scientific literature corpus.
- Question target: precise IR methodological details vs solar/PV scientific questions.
- Downstream retrieval focus: visual/text/multimodal document representations; the lexical/dense/hybrid comparison is not carried into parallel QA arms.
- Evaluation: Recall@K and answer alignment vs potentially retrieval metrics plus correctness/relevance/faithfulness/citation attribution.

# F. Whether IRPAPERS materially weakens the proposed research question

Classification: **PARTIAL pressure, not displacement**.

IRPAPERS materially weakens any broad framing that BM25, dense, and hybrid retrieval have not been experimentally compared over scientific documents: it evaluates all three on the same retrieval benchmark. It does not establish the corresponding downstream RAG comparison, since its GPT-4.1 QA experiments compare hybrid TextRAG and image-based RAG, not BM25-only, dense-only, and hybrid text-retrieval arms.

It does not displace the narrower proposed question because it does not evaluate solar/PV scientific literature or compare the three text-retrieval strategies through the same generator with evidence/citation attribution. It also reports no significance testing. This assessment concerns methodological overlap only and makes no novelty claim.

No novelty claim is made here.
