# Interim Methodological Gap Assessment

**Scope.** This assessment synthesizes only the records currently present in `screening/screening_matrix.csv`, `screening/critical_papers.csv`, `notes/paper-notes/`, and `notes/research-gaps/research_gap_matrix.md`. No papers were searched for or added for this assessment. Findings are limited to what those screened records establish; a blank, preview-only, or metadata-only record is not treated as proof that a method is absent from a paper.

**Proposed study:** “Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Energy Scientific Literature.”

**Updated judgment after final registered-record retrieval:** IRPAPERS remains the direct retrieval-level precedent. RILS materially raises the overlap with system-level BM25+Generation, dense RAG, and hybrid conditions on a renewable-energy benchmark including 150 Solar-PV queries. PeerQA separately combines scientific evidence-retrieval benchmarks with answerability and generation evaluation, but downstream RAG uses SPLADEv3 contexts rather than matched BM25/dense/hybrid QA arms. Han et al.'s MDPI full text has now been screened as a review/framework with no author-run comparison. Wang et al.'s publisher abstract establishes a related scientific-literature QA/RAG system and >50,000-pair SciLitQA benchmark, but its full text remains unavailable after targeted retrieval; experimental arms and controls cannot be determined. That remaining uncertainty is material, so the research question should not yet be frozen.

# 1. What is unquestionably already established?

“Established” here means demonstrated by at least one of the screened studies, not universally effective or settled.

### A. Scientific literature RAG

RAG over scientific papers is established in the screened set. Solar Intelligence, Lit3R, SQuAI, OpenScholar, IRPAPERS, MuISQA, DeepEra, SciRerankBench, CG-RAG, HiPerRAG, and the verifiable scientific QA system all provide evidence of RAG or closely related retrieval-and-generation pipelines over scientific literature. They differ substantially in their corpora, question tasks, system configurations, and evaluation strength.

### B. Scientific QA

Scientific question answering over papers is established. The screened examples range from Lit3R's shared-task QA with single-paper and multi-paper questions, SQuAI's scientific QA and question-answer-evidence triplets, OpenScholar's expert-authored single- and multi-paper synthesis benchmark, to IRPAPERS' page-grounded scientific questions. Their question construction and evaluation are not interchangeable: for example, some use synthetic questions, some use expert-authored tasks, and some provide only abstract-level evidence in the screening record.

### C. Solar/energy RAG

Solar Intelligence and Solar GenAI demonstrate solar/PV RAG applications over research/technical and mixed grey-literature corpora. RILS provides stronger overlap than the earlier interim pass recorded: a mixed renewable-energy corpus, including 4,200 Solar-PV documents in Table 1, and a 900-query expert-grounded assessment benchmark with 150 Solar-PV queries. It compares BM25+Generation, standard dense RAG, and hybrid RILS at the system level, alongside retrieval and downstream metrics. Corpus counts conflict across sections, and the paper does not establish retrieval as the sole changed variable or matched generator/prompt and citation metric controls. Energy-domain RAG therefore exists in multiple forms, but those facts do not alone establish the candidate's controlled experiment.

### D. BM25 retrieval

BM25 is used in Solar Intelligence, Lit3R, SQuAI, and IRPAPERS, among other screened systems. Its use inside a hybrid pipeline or as one component of a system does not by itself constitute a BM25-only experimental arm.

### E. Dense retrieval

Dense retrieval is used in Solar Intelligence, Lit3R, SQuAI, OpenScholar, IRPAPERS, and multiple other screened systems. Models and representations vary, including BGE-small, Qwen3 embeddings, e5-base-v2, Contriever, and Arctic 2.0.

### F. Hybrid retrieval

Hybrid retrieval is implemented in Solar Intelligence (BM25 plus dense retrieval with RRF), Lit3R (sparse/dense ranked fusion in a larger retrieval pipeline), SQuAI (BM25 and e5-base-v2 with linear score interpolation), and IRPAPERS (BM25 plus Arctic 2.0 text search). CG-RAG combines sparse and dense signals in a citation-graph retrieval approach. These implementations establish use of hybrid methods, not necessarily a controlled comparison with each component retriever.

### G. Retrieval benchmarking

Retrieval is evaluated in several screened works, including IRPAPERS, PeerQA, Lit3R, MuISQA, DeepEra, SciRerankBench, and RILS. IRPAPERS directly compares BM25-only, dense-only, and hybrid text retrieval using the same scientific-page corpus and question benchmark. RILS reports BM25+Generation, standard dense RAG, and hybrid RILS system conditions, with retrieval metrics by technology family; those are not shown as clean matched retrieval-only arms. PeerQA compares BM25, dense, multi-vector, cross-encoder, and sparse evidence-retrieval systems, but does not carry those systems through as matched QA arms.

### H. Evidence/citation evaluation

Evidence and citation quality are evaluated in multiple, non-equivalent ways:

- Lit3R reports evidence precision, recall, and F1.
- OpenScholar reports sentence-level citation precision, recall, and F1, alongside correctness and expert/automated answer evaluation.
- SQuAI evaluates faithfulness and relevance and provides citation context/supporting sentences, but the screened evidence does not establish citation precision/recall.
- The verifiable scientific QA system uses claim/article verification, based on the screened abstract-level record.
- Solar Intelligence displays citations and discusses grounding qualitatively, without a formal citation attribution benchmark.
- IRPAPERS uses gold pages and oracle/hard-negative conditions and measures answer alignment, but does not report citation attribution metrics.

Consequently, “evidence-grounded QA,” “faithfulness,” “citation correctness,” and “retrieval recall” should not be treated as synonyms.

# 2. What has already been directly compared?

**Key distinction:** Retrieval-level comparison tests which items are found/ranked. Downstream RAG comparison tests what a generator answers given retrieved context. An experiment at one level does not establish the other.

| Paper | Corpus | BM25 | Dense | Hybrid | Same benchmark | Retrieval comparison | Same generator | Downstream QA comparison | Evidence evaluation |
|---|---|---|---|---|---|---|---|---|---|
| Solar Intelligence | 149 solar research papers/reports plus structured solar data; approximately 9,496 chunks | Used | Used (BGE-small) | Used (BM25+dense, RRF) | No fixed question benchmark reported | **No** separate BM25-only/dense-only/hybrid retrieval results reported | One system uses llama3.2:3b; no retrieval arms under that generator | **No** controlled strategy comparison; qualitative QA examples | Displayed citations and qualitative grounding; no formal citation precision/recall |
| Lit3R | 27,487 recent ML/CV/NLP papers; LitTraceQA | Used (chunk- and paper-level) | Used (Qwen3-Embedding-8B; SPECTER2 expansion) | Used (RRF within the system) | Yes for the LitTraceQA validation/test evaluation of Lit3R; not three retriever arms | **No** BM25-only vs dense-only vs hybrid comparison. Reports retrieval metrics and compares pipeline components, including paper expansion | GPT-5.4 used by Lit3R; no BM25/dense/hybrid arms to hold fixed | **No** three-way retrieval-strategy QA comparison | Evidence precision/recall/F1; answer task metrics |
| SQuAI | More than 2.3M arXiv full-text papers; LitSearch and synthetic unarXive QA tasks | Used | Used (e5-base-v2) | Used (linear interpolation, alpha 0.35) | Same benchmark(s) used for SQuAI/baseline system evaluation; not a three-retriever-arm experiment | **No** BM25-only vs dense-only vs hybrid experimental arms; sparse/dense/hybrid are pipeline configurations | Experimental answer generator not clearly specified in the screened source; user-selectable backend reported | **No** same-generator three-way retriever comparison; compares SQuAI with RAG baseline and conditions | Faithfulness, answer/context relevance; citations/supporting sentences; no attribution precision/recall in screened record |
| IRPAPERS | 166 information-retrieval papers, 3,230 pages, 180 questions | Used as a standalone condition | Used as a standalone condition (Arctic 2.0) | Used (BM25+Arctic 2.0) | **Yes**: same corpus and 180-question retrieval benchmark | **Yes**: direct BM25-only vs dense-only vs hybrid text retrieval comparison; retrieval metrics include Recall@1/5/20 | GPT-4.1 reader for TextRAG/ImageRAG comparisons; **not** a common generator across the three text-retrieval strategies as downstream arms | **Partial but not the requested comparison**: TextRAG vs ImageRAG and retrieval-depth/oracle conditions are compared; BM25, dense, and hybrid are not all carried into QA | Gold-page/oracle/hard-negative conditions and answer alignment; no citation precision/recall or evidence-attribution F1 |
| OpenScholar | 45M open-access papers in datastore; 234M passages in methods, 237M in abstract | Not reported | Used (Contriever pretrained on peS2o) | Dense datastore retrieval plus API/web candidates, but no BM25+dense hybrid is specified | Yes for system/model comparisons on ScholarQABench and adopted datasets; not retrieval-arm comparison | **No** BM25/dense/hybrid strategy comparison; component ablations are different experimental variables | Multiple generators/models evaluated; no fixed-generator comparison across BM25/dense/hybrid arms | **No** requested retrieval-strategy QA comparison | Sentence-level citation precision/recall/F1, answer correctness and human/automated quality evaluation |
| RILS (Orabi et al.) | Mixed renewable-energy corpus; 18,000/28,800 in Table 1 vs 21,000/32,800 in later sections; 150 of 900 questions are Solar PV | Yes as a system baseline, named BM25+Generation | Yes; standard dense RAG/global dense cosine is described | Yes; BM25+dense RILS with weighted score combination | 900 expert-grounded assessment queries; shared benchmark across system conditions reported | System-level comparison, not a clean retrieval-only comparison; per-arm retrieval results not established | Same 7B generator/prompt across all baselines not established | **Yes, system-level downstream conditions** include BM25+Generation, standard RAG, and RILS; components beyond retrieval differ | Retrieval, answer accuracy, hallucination, NLI claim verification, latency; no per-arm citation precision/completeness |
| PeerQA | 208 annotated scientific papers/579 QA items; one-paper questions | Yes, evidence retrieval only | Yes, several dense models | No BM25+dense hybrid arm reported | Same evidence queries for model retrieval evaluation; common downstream retriever not an arm comparison | **Yes** at evidence-retrieval level for BM25/dense/sparse model baselines; not BM25/dense/hybrid | Multiple generators for downstream tasks; not matched to each retrieval model | **No** matched retrieval-model QA arms; downstream RAG uses SPLADEv3 contexts | Gold evidence retrieval MRR/Recall@10, answerability, answer-quality metrics; no generated citation scores |
| Solar GenAI | Mixed policy/technical sources and selected solar research publications | Not reported | Yes, all-MiniLM-L6-v2 cosine | Not reported | Fixed benchmark not established | No | One RAG application; no strategy arms | LLM-only vs RAG, not retriever comparison | Hallucination/latency observations; no formal evidence/citation score |
| HySemRAG | Scientific literature synthesis, geospatial epidemiology | Keyword filtering; BM25 specifically not reported | Semantic search | Components combined in a hybrid synthesis pipeline | Corpus/session evaluation, but no matched retrieval benchmark established | No matched lexical/dense/hybrid arms | Not established across retrievers | No matched downstream retriever arms established | Citation verification is described; precision/completeness per generated citation not established |
| MuISQA | 10,000 arXiv documents; multi-intent scientific QA | Not reported | Used | No BM25+dense hybrid reported; RRF aggregates multiple generated-query rankings | Benchmark/system evaluation reported; not a sparse/dense/hybrid arm comparison | **No** BM25-only/dense-only/hybrid comparison | Not a fixed-generator three-way retriever test | QA method/system comparisons, not the requested retriever arms | Information Recall Rate and answer accuracy/coverage; no citation correctness |
| DeepEra | Approximately 10M scientific articles and 300K QA pairs | BM25 not established; SPLADE sparse baseline appears in reranking comparisons | Used for initial vector retrieval | No BM25+dense hybrid comparison established | Yes for its reranking/evidence experiments; not the requested retrieval comparison | Reranker/evidence ranking comparisons, not BM25/dense/hybrid arms | Llama-2-70B used; no three retriever arms | Downstream answer/evidence effects are studied for reranking, not the proposed retriever variable | HitRate@K, relative position, answer P/R/F1 and Logic Fidelity Score; no citation metrics |
| SciRerankBench | Scientific abstracts/full texts across five disciplines; synthetic QA | Not reported | Used | Not reported | Yes for reranker/noise benchmark conditions | Reranker/retrieval robustness comparisons, not BM25/dense/hybrid strategy comparison | Generator details do not establish the proposed controlled arms | Generation/robustness evaluated across reranker conditions, not requested retriever strategies | Ranking and factual-consistency evaluation; no citation attribution metric |
| Scientific QA System with Verifiable Answers | PubMed/biomedical articles (screened from abstract/preview) | Lexical component reported | Semantic component reported | Semantic + lexical search pipeline | Not established from the screened abstract | **Not established** | Not established | QA/claim verification pipeline, but no strategy arms established | NLI-based claim/article verification; exact citation precision/recall not established |
| CG-RAG | Scientific QA benchmarks and citation graph | Sparse graph signals reported | Dense graph signals reported | Graph-based lexical-semantic retrieval | Benchmark comparisons reported in the screened abstract | Compares graph retrieval/system baselines, not BM25-only vs dense-only vs conventional hybrid | Not established for the proposed arms | QA system comparison, not the requested retrieval arms | Retrieval accuracy/generation quality; citation correctness not established |
| HiPerRAG | More than 3.6M scientific articles | Not reported | Dense/late-interaction retrieval (ColTrast) | Not established | Scientific QA benchmark evaluation reported | Scaling/system evaluation, not BM25/dense/hybrid arms | Not established for proposed arms | QA accuracy and scaling, not three-way retrieval comparison | QA accuracy/scaling; citation metrics not reported |
| Graph-based RAG for Energy Efficiency QA | Energy-efficiency guidance/regulatory documents and websites | Not reported | Embeddings used in graph/entity retrieval | Graph retrieval, not the specified BM25+dense hybrid | Expert validation/evaluation reported; not a solar scientific-paper benchmark | No comparable lexical/dense/hybrid retrieval-arm comparison | Not reported for the proposed arms | Energy QA comparison/evaluation, not solar scientific-literature retrieval strategies | Expert/RAGAS faithfulness/relevance/context relevance and latency |

Entries marked “not reported” or “not established” in this table describe the available screened evidence, not necessarily the full underlying paper. Detailed records are in the [screening matrix](../../screening/screening_matrix.csv), [critical-papers register](../../screening/critical_papers.csv), [research-gap matrix](research_gap_matrix.md), and individual notes for [Solar Intelligence](../paper-notes/solar_intelligence.md), [Lit3R](../paper-notes/lit3r.md), [SQuAI](../paper-notes/squai.md), [IRPAPERS](../paper-notes/irpapers.md), and [OpenScholar](../paper-notes/openscholar.md).

# 3. What has NOT been established?

The following are gaps in the **screened evidence**, not claims about all published work:

1. **The joint controlled design:** Not established in the screened literature is one experiment that varies BM25-only, dense-only, and a specified hybrid retriever as the independent variable while holding one solar/PV scientific-paper corpus, question benchmark, preprocessing, generator, prompt, and evaluation protocol constant.
2. **Retrieval-to-answer propagation:** Not established in the screened evidence is a matched comparison that reports retrieval quality for those three arms and then carries each arm's retrieved evidence into the same generator for downstream answer evaluation.
3. **Joint evidence attribution:** Not established in the screened evidence is the requested three-arm comparison with formal claim/evidence attribution or citation precision and completeness evaluated under identical downstream QA conditions.
4. **Solar/PV scientific QA benchmark conditions:** Solar Intelligence demonstrates solar-domain retrieval/RAG, but its screened note reports no fixed question benchmark or formal retrieval/answer/citation comparison. The other closest QA/evidence studies use non-solar scientific domains or different energy-document corpora.
5. **Statistical comparison for this contrast:** Not established in the screened evidence is inferential statistical comparison of the three retrieval strategies on downstream scientific QA/evidence outcomes in a solar/PV corpus.
6. **Unanswerable handling:** A systematic unanswerable/insufficient-evidence solar scientific QA condition with abstention evaluation is not established in the screened records most relevant to the candidate design. This is an optional dimension in the candidate design, not a premise needed to state the core gap.

The gaps do **not** include:

- scientific literature RAG generally;
- scientific QA generally;
- solar or energy RAG generally;
- use of BM25, dense, or hybrid retrieval individually;
- retrieval benchmarking over scientific papers;
- evidence/citation evaluation in scientific QA;
- BM25-only vs dense-only vs hybrid retrieval at retrieval level over scientific literature.

Those components are demonstrated by the screened records, with scope and quality varying by study.

# 4. Candidate methodological gap

Candidate:

> “A controlled comparison of lexical, dense, and hybrid retrieval as the independent variable in evidence-grounded scientific QA, using the same solar-PV corpus, benchmark questions, generator, and evaluation protocol, with retrieval quality and downstream evidence grounding evaluated jointly.”

**Assessment: supported as a defensible gap in the screened literature, with a necessary qualification.**

- **The broad retrieval-comparison claim needs narrowing.** IRPAPERS directly compares BM25-only, Arctic 2.0 dense-only, and hybrid text retrieval on one scientific-paper corpus and one 180-question benchmark. The proposed study should not imply that such a scientific-literature retrieval comparison has not been done.
- **The downstream controlled comparison remains distinct, but the nearest neighbor is stronger than previously recorded.** IRPAPERS's three retrieval conditions are retrieval-level conditions. RILS evaluates BM25+Generation, standard dense RAG, and hybrid RILS as downstream system conditions on an expert-grounded renewable-energy benchmark including a Solar-PV subset, but does not establish that retrieval alone varies or that generator/prompt/citation outcomes are matched across arms. PeerQA evaluates evidence retrieval and downstream QA separately, with SPLADEv3 contexts for RAG generation.
- **Scientific QA and evidence metrics are established separately.** Lit3R, SQuAI, and OpenScholar establish scientific QA and varying forms of evidence/citation evaluation. Their screened designs do not isolate the three retrieval strategies as a common independent variable.
- **Solar domain coverage is established in more than one form.** Solar Intelligence and Solar GenAI provide solar-PV RAG applications. RILS includes a substantial Solar-PV assessment subset in a mixed corpus and is a direct system-level comparator. It does not establish a solar-PV-only scientific-paper corpus or a retrieval-only controlled comparison with formal per-arm evidence/citation metrics.
- **Therefore:** a defensible distinction must explicitly be the *retrieval-only controlled variable* and the joint matched retrieval/downstream evidence-grounding evaluation on one solar-PV scientific-paper corpus. This distinction remains clear in the screened evidence, but Wang et al.'s inaccessible full text still needs resolution before freezing.

# 5. Threats to the proposed study

This section records screened studies with methodological overlap that could constrain a contribution claim.

| Paper | Exact overlap | Partial overlap | Remaining difference relative to candidate |
|---|---|---|---|
| **IRPAPERS** | Same-corpus/same-question BM25-only vs dense-only vs hybrid text-retrieval comparison on scientific papers; retrieval metrics; downstream QA under other controlled conditions | Scientific paper QA, gold-page/oracle/hard-negative conditions, same GPT-4.1 reader in TextRAG/ImageRAG comparison | The three text retrievers are not carried as three same-generator QA arms; information-retrieval domain, not solar/PV; no citation attribution precision/recall |
| **Solar Intelligence** | Solar/PV papers/reports; BM25 and dense implemented; BM25+dense RRF hybrid; generator-backed cited QA | Most direct domain overlap; retrieval is used within one integrated platform | No separate retrieval arms, fixed benchmark question count, formal retrieval/answer/citation metrics, or statistical comparison |
| **Lit3R** | Scientific-literature QA with BM25, dense, hybrid fusion, reranking, retrieval metrics, and evidence precision/recall/F1 | Strong methodological overlap for retrieval and evidence-grounded QA | No solar/PV domain; BM25/dense/hybrid are components of one system, not isolated strategy arms; no strategy-wise downstream QA comparison |
| **SQuAI** | Scientific QA over arXiv; BM25, dense, hybrid; citations and faithfulness/relevance evaluation | Strong pipeline and evidence-grounding overlap | No solar/PV domain; the retrievers are not compared as matched experimental arms; generator details and citation precision/recall are not established in the screened record |
| **OpenScholar** | Large-scale scientific literature synthesis QA, multi-paper tasks, citations and sentence-level citation precision/recall/F1 | Strong downstream answer/evidence evaluation and expert benchmark | No solar/PV corpus; dense-plus-API/web pipeline, not a BM25/dense/hybrid comparison; no standalone retrieval metrics for that comparison |
| **RILS (Orabi et al.)** | Renewable-energy assessment including 150 solar-PV queries; system-level BM25+Generation, standard dense RAG, and hybrid RILS conditions; retrieval and downstream answer metrics | Closest domain/system-level overlap; expert-grounded benchmark; NLI claim verification and resource/latency figures | Does not establish retrieval-only independent-variable control, same generator/prompt across every condition, or per-arm formal citation/evidence scores; corpus counts conflict |
| **PeerQA** | Scientific-paper QA with BM25 and dense/sparse evidence retrievers, author-annotated evidence, unanswerable cases, retrieval metrics, and downstream generation | Human peer-review questions and author-annotated answers/evidence | Single-paper and non-solar; retrieval-model comparisons do not continue as matched downstream QA arms; downstream RAG uses SPLADEv3 contexts and has no generated citation-quality evaluation |
| **Solar GenAI** | Solar-PV RAG with dense retrieval over mixed policy/technical sources and selected research publications | Direct domain application and answer/hallucination observations | No matched retriever arms, retrieval metrics, or formal evidence/citation attribution |
| **Graph-based RAG for Energy Efficiency QA** | Energy-domain QA; formal answer/context/faithfulness evaluation | Energy QA and evaluated answer grounding | Energy-efficiency guidance/web corpus rather than solar scientific literature; graph retrieval rather than the specified retrieval arms |
| **MuISQA** | Multi-intent scientific QA with retrieval metrics and answer accuracy/coverage | Scientific multi-document evidence coverage | Dense multi-query retrieval/RRF, not BM25/dense/hybrid arms; not solar/PV; no citation attribution benchmark |
| **DeepEra** | Scientific QA and retrieval/evidence ranking metrics linked to answer/evidence outcomes | Demonstrates that retrieval/reranking evidence quality can be studied jointly with downstream quality | Reranking-focused; sparse baseline is not a demonstrated BM25/dense/hybrid comparison; no solar/PV citation evaluation |
| **SciRerankBench** | Scientific RAG benchmark with retrieval/reranking and generation/robustness evaluation | Useful precedent for evidence noise and reranker comparisons | Dense/reranker study, not BM25/dense/hybrid strategy arms; synthetic benchmark and no solar/PV citation attribution |
| **Scientific QA System with Verifiable Answers** | Biomedical scientific QA with semantic and lexical retrieval and claim verification | Supports scientific claim-level verification as an evaluation concern | Screened evidence is abstract-level; no retrieval-arm comparison, solar domain, or established citation precision/recall experiment |
| **CG-RAG** | Scientific QA with sparse and dense retrieval signals and retrieval/generation evaluation | Hybrid scientific retrieval and citation-graph setting | Graph-based method; no demonstrated BM25-only/dense-only/conventional-hybrid matched arms; no solar/PV corpus or established citation correctness metric |
| **HiPerRAG** | Large-scale scientific literature retrieval and QA | Scientific corpus scale and QA accuracy | Dense/late-interaction and HPC focus; no BM25/dense/hybrid arms or solar/PV evidence attribution in screened record |

### Threat interpretation

IRPAPERS is the principal threat to a broad retrieval-level claim. RILS is the closest energy-domain system-level threat: it reports BM25+Generation, standard dense RAG, and hybrid RILS on an expert-grounded renewable-energy benchmark that includes Solar-PV questions. PeerQA is a close scientific QA/evidence-retrieval threat with separate answerability and generation tasks. Lit3R and SQuAI constrain broad claims about scientific evidence-grounded QA using hybrid retrieval; OpenScholar constrains broad claims about scientific synthesis and citation evaluation; Solar Intelligence and Solar GenAI constrain broad claims about solar/PV RAG. The candidate remains differentiated in the screened evidence only where retrieval itself is isolated, matched downstream conditions are maintained, and evidence attribution is measured in a solar-PV scientific-paper setting. Wang et al. remains unresolved: its abstract indicates scientific RAG/QA and retrieval experiments but does not disclose the arms or controls. This does not support a field-wide absence claim.

# 6. What would NOT constitute a contribution?

Based on the screened records, a contribution should not be framed as:

- introducing RAG for scientific papers;
- introducing scientific question answering over a literature corpus;
- using BM25 for scientific-paper retrieval;
- using dense embeddings for scientific-paper retrieval;
- using sparse and dense retrieval together;
- applying BM25, dense, and hybrid retrieval to the same scientific corpus/questions at **retrieval level** (IRPAPERS already demonstrates this);
- using hybrid retrieval for solar/PV papers (Solar Intelligence reports this);
- generating cited scientific answers or evaluating citation/evidence quality in general;
- evaluating retrieval metrics, answer correctness, faithfulness, citation precision/recall, multi-paper synthesis, or reranking as isolated ideas.

The methodologically relevant contribution, if supported by execution, would be the controlled *joint comparison* and its domain-specific empirical results—not the individual components.

# 7. What could constitute a genuine contribution?

These are dimensions a completed study could contribute if the methods and results substantiate them; they are not claims that the study already does so.

### Methodological contribution

A clearly specified, reproducible comparison with retrieval strategy as the independent variable; shared corpus, question set, preprocessing, generator, prompt, and evaluation conditions; and explicit separation of retrieval effects from generator/model effects. IRPAPERS makes it especially important to identify the downstream QA/evidence component as the distinction.

### Empirical contribution

Measured evidence about whether BM25-only, dense-only, and a specified hybrid strategy change retrieval results, answer quality, or evidence/citation support on the evaluated solar/PV tasks. Report uncertainty and statistical comparisons appropriate to the benchmark; avoid treating a retrieval metric improvement as proof of better answers.

### Benchmark contribution

A documented solar-PV scientific-paper corpus and question set with reproducible inclusion dates, preprocessing, question provenance, answerability/ground-truth evidence, and evaluation annotations. Its added value would depend on demonstrated coverage and annotation quality, not merely on being domain-specific.

### Domain contribution

Evidence about how lexical and semantic retrieval behave for solar/PV scientific questions and terminology on the actual corpus, including whether domain-specific vocabulary, acronyms, named materials, performance metrics, or methodological descriptions affect retrieval and downstream evidence use.

### Evaluation contribution

A linked evaluation that reports retrieval quality separately from answer correctness and evidence/citation attribution, and analyzes their relationship. If unanswerable questions are included, evaluate abstention distinctly; it is not necessary to claim that abstention is part of the central contribution if it is outside the final design.

# 8. Recommended research question — ONLY IF JUSTIFIED

**The methodological distinction remains plausible but should not yet be frozen.** RILS requires explicit separation between system-level BM25/RAG/RILS outcomes and a retrieval-only experimental variable; PeerQA requires separating its evidence-retrieval benchmark from downstream SPLADEv3-context QA. Han et al. is screened and does not present a matching experiment. Wang et al.'s full text remains unavailable after targeted retrieval; its abstract makes it sufficiently relevant that no rewritten RQ is recommended until its detailed methods can be checked.

# 9. Confidence assessment

| Confidence | Assessment | Evidence and limits |
|---|---|---|
| **High confidence** | IRPAPERS directly compares BM25-only, dense-only, and hybrid text retrieval on the same scientific corpus and question benchmark at retrieval level. RILS reports BM25+Generation, standard dense RAG, and hybrid RILS system-level conditions on a common renewable-energy assessment benchmark including Solar-PV questions. PeerQA compares evidence retrievers and separately evaluates answerability/generation. | Supported by the screened full texts. RILS does not establish retrieval-only controls; PeerQA does not carry retriever arms into downstream QA. Confidence concerns what these records report, not field completeness. |
| **Medium confidence** | The exact candidate intersection—retrieval as the isolated variable, matched solar/PV scientific-paper corpus/questions/generator, and jointly assessed retrieval and evidence-grounded downstream QA—is not established in the screened records. | RILS reports a close system-level renewable-energy comparison including a Solar-PV subset; PeerQA combines evidence retrieval and downstream QA as separate tasks. Wang et al.'s full text remains unavailable, so its exact experimental conditions cannot be checked. |
| **Low confidence** | Any statement that the candidate is absent from the wider literature or establishes field-wide priority. | The screening set is not exhaustive; a bounded screen cannot establish field-wide absence. |

**Overall confidence in the candidate gap as a defensible statement about the screened literature: Medium.** Confidence is high that IRPAPERS's three-way retriever comparison is retrieval-level and that RILS's three system conditions are not established as a retrieval-only factorial comparison. Confidence is medium that the exact matched downstream intersection remains unestablished because Wang et al.'s full text could not be inspected, despite its abstract-level scientific QA/RAG overlap. No field-wide absence is asserted.

# 10. Focused follow-up status and unresolved screening

The focused follow-up screened the ten already registered records named in the prior interim list. No records were added from external databases. Full texts or substantial text were inspected for Solar GenAI, Open Energy, RILS, PeerQA, HySemRAG, Solar-VLM, Retrieval-Guided PV Inventory, and Han et al. The registered Research on PV IOP abstract was inspected, but publisher full text was unavailable. Han's full text was obtained from an MDPI-hosted article asset PDF. Wang's ScienceDirect page provides publisher highlights, abstract, and limited snippets only; targeted publisher and legitimate discovery-source routes did not produce the full text.

Of the ten designated follow-up records, one full text remains unresolved:

- **Wang et al., “Multi-level Retrieval with Representation Alignment Enhances Cross-document Evidence Synthesis”** (`wang_multi-level_2026`) — full text unavailable after targeted retrieval attempt. Abstract-level scientific QA/RAG overlap is recorded, but matched retrieval arms and evaluation are not inferred.

Han et al. (`han_automating_2024`) was screened from full text as a review/framework and does not report an author-run controlled retrieval or QA experiment. Wang remains a required material uncertainty because the abstract describes scientific cross-document QA/RAG and retrieval experiments but does not reveal whether it contains the matched BM25/dense/hybrid downstream comparison under consideration. The interim decision therefore remains not to freeze the research question. Other metadata-only records remain in the project register but were not part of this ten-record follow-up and were not screened in this pass. No broad search is recommended.
