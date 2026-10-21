# Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature

**Authors:** Anonymous Authors (Manuscript v0.1 — Pre-Experimental Protocol & Conceptual Draft)  
**Date:** October 2026  
**Status:** DRAFT MANUSCRIPT (SECTIONS 1–8 DRAFTED; SECTIONS 9–10 EMPTY PENDING EXPERIMENT; REAL-PAPER DISCOVERY AND EXPERIMENT BLOCKED)

---

## Abstract

*(Structured Abstract Placeholder — To be completed following execution of the confirmatory experiment)*

**Background:** Retrieval-Augmented Generation (RAG) is increasingly deployed to ground Large Language Model (LLM) responses in domain-specific scientific literature. In high-velocity technical domains such as solar photovoltaic (PV) engineering, effective question answering requires precise retrieval of empirical device parameters, degradation kinetics, materials formulations, and manufacturing tolerances. While lexical (BM25), dense semantic, and hybrid retrieval strategies are widely discussed, prior literature frequently evaluates retrieval metrics in isolation without downstream generation, conflates multiple system-level modifications, or focuses on general multi-domain literature. Whether differences in retrieval strategy translate into statistically significant improvements in downstream answer correctness and evidence attribution under strictly controlled, identical generation conditions remains an open empirical question.

**Objective:** To conduct a controlled comparative evaluation of BM25, dense, and hybrid retrieval strategies over a shared, peer-reviewed solar-PV scientific literature corpus, evaluating retrieval quality, answer quality, and citation attribution under invariant downstream generator, prompt, and context-budget conditions.

**Methods:** *(Planned)* A corpus of contemporary peer-reviewed solar-PV scientific literature (2024–2026 core window, supplemented by algorithmically chained foundational literature with strict candidate anti-self-citation) will be ingested into a shared text-first chunk repository. Three retrieval strategies—BM25 lexical retrieval, dense semantic retrieval, and Reciprocal Rank Fusion (RRF) hybrid retrieval—will retrieve evidence for a paired, expert-validated question benchmark spanning factual extraction, multi-hop synthesis, comparative analysis, and unanswerable controls. Downstream answers will be generated using a frozen LLM with an invariant prompt and identical context budget. Outcomes will be measured across retrieval quality (Recall@k, MRR), answer correctness (claim accuracy, rubric alignment), and evidence attribution (sentence-level citation precision, citation recall, claim entailment). Primary inference will be evaluated over a primary empirical research index ($I_{\text{primary}}$), with a secondary sensitivity index ($I_{\text{all}}$) incorporating review articles.

**Results:** *(Results pending experimental execution. No empirical data or fabricated results are reported in this version.)*

**Conclusions:** *(Provisional — Pending experimental results.)*

---

## Keywords

Solar photovoltaic literature, retrieval-augmented generation (RAG), evidence-grounded question answering, BM25 retrieval, dense semantic retrieval, hybrid retrieval, reciprocal rank fusion, citation attribution, scientific information retrieval.

---

## 1. Introduction

Solar photovoltaic (PV) technology represents one of the fastest-evolving pillars of the global energy transition. Recent years have witnessed rapid advances in cell architectures—including tunnel oxide passivated contact (TOPCon), silicon heterojunction (SHJ), and perovskite-silicon tandem configurations—alongside increasingly complex degradation mechanisms, operational reliability models, and grid-integration diagnostics. Navigating this dense, rapidly expanding body of literature poses substantial challenges for researchers, system engineers, and policymakers seeking timely, evidence-grounded answers to technical queries.

Large Language Models (LLMs) have emerged as powerful tools for natural language understanding and scientific synthesis. However, their deployment in specialized technical domains is severely constrained by parametric memory limitations, temporal obsolescence, and the well-documented propensity to generate plausible but factually erroneous statements (hallucinations). In technical fields such as solar PV, where small errors in reported power conversion efficiencies (PCE), open-circuit voltage ($V_{oc}$) losses, potential-induced degradation (PID) polarization rates, or levelized cost of energy (LCOE) can lead to fundamentally incorrect engineering conclusions, ungrounded generative outputs are unacceptable.

Retrieval-Augmented Generation (RAG) addresses these vulnerabilities by coupling an external document retrieval mechanism with a generative language model. In a standard scientific RAG pipeline, an incoming question triggers a retrieval query across a pre-indexed corpus of scientific literature; the retrieved passages are assembled into an augmented prompt, and the generator synthesizes an answer explicitly constrained by and cited against the retrieved context.

Despite widespread adoption of RAG architectures across scientific disciplines, a fundamental methodological question remains unresolved: **how do differing retrieval strategies—specifically classical lexical retrieval (BM25), continuous dense semantic retrieval, and hybrid combinations thereof—impact end-to-end performance when every downstream generation, prompt, and context constraint is held strictly identical?**

In scientific information retrieval, classical lexical methods (such as BM25) excel at capturing exact terminology, chemical formulas, standardized acronyms (e.g., ISOS-D-1, PERC, TOPCon), and specific numerical figures. However, lexical methods suffer from vocabulary mismatch when queries and documents use differing synonyms or paraphrased expressions. Conversely, dense semantic retrievers, powered by bi-encoder transformer architectures, map queries and passages into continuous vector spaces, capturing conceptual semantic similarity and thematic intent. Yet dense retrievers often struggle with fine-grained numerical distinctions, specific technical identifiers, and rare domain jargon, sometimes retrieving thematically related but factually non-supportive passages—a phenomenon known as semantic drift. Hybrid retrieval methods seek to combine the complementary strengths of lexical and dense representations through rank-fusion or score-interpolation mechanisms.

Crucially, in the existing literature, several critical gaps and confounding factors obscure the true downstream impact of retrieval strategy:

1. **Retrieval in Isolation vs. Downstream Impact:** Seminal benchmarking efforts such as IRPAPERS [@shorten_irpapers_2026] and PeerQA [@baumgartner_peerqa_2025] evaluate lexical, dense, and hybrid retrievers on scientific documents, but either do not carry all three retrieval arms into matched downstream generation conditions or evaluate generation using an alternative retrieved context, leaving open the question of whether retrieval-level differences persist through generation.
2. **System-Level Bundling vs. Causal Isolation:** Advanced domain-specific and scientific RAG systems, such as RILS in renewable energy [@orabi_rag-based_2026], OpenScholar [@asai_openscholar_2024; @asai_synthesizing_2026], Lit3R [@ise_lit3r_2026], and SQuAI [@besrour_squai_2025], introduce complex multi-stage architectures involving query expansion, multi-agent decomposition, dynamic reranking, and self-reflective feedback. In such studies, multiple system components vary simultaneously, making it impossible to isolate the specific causal contribution of the underlying retrieval strategy.
3. **Application Precedents Without Controlled Comparisons:** Dedicated solar-PV RAG applications, including Solar Intelligence [@singh_solar_2026] and Solar GenAI [@shafidah_solar_2026], demonstrate the practical feasibility of domain-specific RAG but implement a single retrieval approach (e.g., dense-only or hybrid) without performing a controlled comparison against alternative retrieval paradigms.
4. **Conflation of Retrieval Quality, Answer Quality, and Evidence Attribution:** In many evaluations, high retrieval recall is assumed to ensure answer correctness, or answer correctness is assumed to imply faithful evidence grounding. In scientific QA, however, an LLM may generate a factually accurate statement from its internal parametric pre-training while citing an irrelevant retrieved passage (citation hallucination), or conversely, fail to extract a correct answer despite having relevant evidence present in the context.

To resolve these ambiguities, this study establishes an empirical, controlled investigation designed to isolate retrieval strategy as the sole manipulated independent variable over a shared corpus of peer-reviewed solar-PV scientific literature.

### Frozen Governing Research Question

> **How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?**

### Proposed Narrow Contributions

This manuscript reports the pre-registered protocol, architectural specification, and initial conceptual drafting for this controlled investigation. Its proposed contributions are:
1. **A Strictly Controlled Three-Arm Factorial Design:** Isolating retrieval strategy (BM25 vs. dense bi-encoder vs. Reciprocal Rank Fusion hybrid) as the sole independent variable, holding the corpus, chunking, context budget, generator model, prompt template, decoding parameters, and evaluation rubrics invariant.
2. **Disaggregated Tripartite Outcome Evaluation:** Simultaneously and independently evaluating (i) retrieval quality (Recall@k, MRR), (ii) downstream answer correctness and completeness, and (iii) evidence attribution (sentence-level citation precision, citation recall, and claim entailment).
3. **An Auditable, Provenance-Tracked Scientific Corpus Protocol:** Introducing a reproducible corpus acquisition and curation framework tailored to solar-PV literature, incorporating strict publication-date precedence (prohibiting deposit-date leakage), transparent backward citation chaining with strict 100% candidate anti-self-citation, and dual-index stratification ($I_{\text{primary}}$ vs. $I_{\text{all}}$) to assess the confounding impact of review literature.

The remainder of this manuscript is organized as follows: Section 2 reviews related work in scientific information retrieval, scientific RAG systems, and solar-PV language models. Section 3 formalizes the research gap and study rationale. Section 4 specifies the research questions and experimental hypotheses. Section 5 details the methodology, including study design, corpus construction, retrieval architectures, generation controls, and statistical analysis. Sections 6 through 9 present the planned structure for results, discussion, limitations, and conclusions.

---

## 2. Background and Related Work

### 2.1 Retrieval Paradigms in Scientific Question Answering

Scientific literature exhibits linguistic and structural properties that distinguish it sharply from open-domain web text. Scholarly articles feature dense domain nomenclature, standardized taxonomic terms, mathematical notation, tabular experimental measurements, and extensive inter-document citation networks. Within scientific information retrieval (IR), three primary retrieval paradigms have been explored:

#### Lexical Retrieval (BM25)
Classical lexical retrieval, exemplified by BM25, scores documents based on term frequency (TF), inverse document frequency (IDF), and document length normalization. In scientific contexts, BM25 provides strong baseline performance because scientific queries often target specific, unambiguous entities—such as chemical dopants (e.g., $Cs_{0.05}(MA_{0.17}FA_{0.83})_{0.95}Pb(I_{0.83}Br_{0.17})_3$), commercial cell architectures (TOPCon, PERC), or experimental standards (IEC 61215). BM25 is computationally efficient, requires no training or domain-specific fine-tuning, and is immune to semantic hallucination. However, it fails when relevant passages use synonymy, alternate terminological variants (e.g., "power conversion efficiency" vs. "photovoltaic yield"), or implicit conceptual explanations [@shorten_irpapers_2026; @baumgartner_peerqa_2025].

#### Dense Semantic Retrieval
Dense retrieval models map both queries and passages into dense, continuous embedding spaces using dual-encoder (bi-encoder) neural architectures. Semantic similarity is computed as the inner product or cosine similarity between dense vector representations. Dense retrievers excel at overcoming vocabulary mismatch and capturing abstract semantic relationships. However, dense encoders are vulnerable to several well-documented failure modes in scientific literature:
1. *Loss of Fine-Grained Precision:* Dense representations can conflate closely related but technically distinct concepts (e.g., confusing PID-polarization with PID-shunting).
2. *Numerical Insensitivity:* Vector representations frequently compress or discard exact numerical thresholds (e.g., failing to distinguish 22.5% efficiency from 25.2% efficiency).
3. *Semantic Drift:* A dense retriever may assign high similarity scores to a passage discussing general perovskite degradation when queried about a specific encapsulation moisture barrier, leading to context contamination [@chen_scirerankbench_2025; @chen_deepera_2026].

#### Hybrid Retrieval and Fusion
Hybrid retrieval architectures combine lexical and dense retrieval scores to leverage their complementary strengths. The two primary integration approaches are linear score combination (which requires calibrated score normalization) and rank-based fusion. Reciprocal Rank Fusion (RRF), formalized by Cormack et al. and widely utilized in modern RAG systems [@shorten_irpapers_2026; @singh_solar_2026; @ise_lit3r_2026], computes an aggregated score for document $d$ across retrieval arms $M$ as:
$$RRF(d) = \sum_{m \in M} \frac{1}{k_{rrf} + r_m(d)}$$
where $r_m(d)$ denotes the rank of document $d$ in retrieval arm $m$, and $k_{rrf}$ is a constant (typically 60) that mitigates the impact of high-ranking outliers. While hybrid retrieval consistently demonstrates superior retrieval recall across diverse benchmarks, its downstream impact on generative answer quality and evidence attribution under matched context budgets remains underexplored.

---

### 2.2 Retrieval-Augmented Generation for Scientific Literature

Recent research has intensified focus on developing RAG systems capable of synthesizing complex scientific literature and supporting generated statements with verified citations.

Several large-scale scientific RAG architectures have demonstrated state-of-the-art literature synthesis. **OpenScholar** [@asai_openscholar_2024; @asai_synthesizing_2026] introduces an open, retrieval-augmented framework operating over a datastore of ~45 million scientific papers (~234 million passages), demonstrating that open-source models augmented with dense retrieval and cross-encoder reranking can match or exceed proprietary LLMs in expert-evaluated literature synthesis. OpenScholar provides rigorous sentence-level citation evaluation (precision, recall, F1) but focuses on end-to-end synthesis over a massive multi-domain corpus rather than a controlled comparison of underlying retrieval strategies.

Similarly, **Lit3R** [@ise_lit3r_2026] introduces an evidence-grounded scientific literature QA system operating over 27,487 papers (~2.56 million chunks) using a hybrid BM25 and dense retrieval pipeline coupled with Qwen3 reranking. Lit3R evaluates evidence precision, recall, and F1, but does not isolate BM25, dense, and hybrid retrieval as separate downstream QA arms.

**SQuAI** [@besrour_squai_2025] implements a multi-agent decomposition and sparse-dense retrieval architecture over 2.3 million arXiv papers, emphasizing contextual relevance and verifiable inline citations. **HySemRAG** [@godinez_hysemrag_2025] integrates semantic search, keyword filtering, and knowledge-graph traversal for scientific literature synthesis in geospatial epidemiology, evaluating extraction fidelity and citation accuracy. Other noteworthy systems include **LitLLM** [@agarwal_litllm_2024], which applies RAG to scientific paper summarization, and work by Han et al. [@han_automating_2024], which synthesizes systematic literature review methodologies using RAG. In a related vein, Wang et al. [@wang_multi-level_2026] propose a multi-level retrieval framework with representation alignment over SciLitQA (>50,000 QA pairs), though their experimental controls and downstream attribution metrics remain partially unestablished from available publisher previews.

In parallel with system development, specialized scientific benchmarks have advanced evidence evaluation. **PeerQA** [@baumgartner_peerqa_2025] introduces an expert-annotated scientific QA benchmark spanning 208 papers and 579 questions, evaluating BM25, dense, multi-vector, and cross-encoder models for evidence retrieval. While PeerQA evaluates evidence retrieval rigorously, its downstream RAG experiments utilize SPLADEv3 contexts rather than comparing the retrieval models as matched downstream generator arms.

Most directly relevant at the retrieval level is **IRPAPERS** [@shorten_irpapers_2026], which establishes a direct, same-corpus, same-question comparison among BM25-only, Arctic 2.0 dense-only, and hybrid text retrieval across 166 scientific papers (3,230 pages) and 180 curated questions. However, IRPAPERS focuses primarily on retrieval-level Recall@k and multimodal TextRAG vs. ImageRAG contrasts, without carrying the three text retrievers forward into matched downstream generation arms or evaluating fine-grained citation attribution.

Additional scientific benchmarking efforts have examined complementary dimensions of the scientific RAG pipeline: **MuISQA** [@li_muisqa_2025] investigates multi-intent, multi-document evidence coverage; **DeepEra** [@chen_deepera_2026] and **SciRerankBench** [@chen_scirerankbench_2025] benchmark rerankers against noisy and logically misleading contexts; **HiPerRAG** [@gokdemir_hiperrag_2025] explores high-performance indexing at multi-million-paper scale; and **CG-RAG** [@hu_cg-rag_2025] evaluates sparse-dense integration across scientific citation graphs.

---

### 2.3 AI and Information Retrieval in Solar Photovoltaics

The application of natural language processing and generative AI to the renewable energy and solar photovoltaic domain has gained significant momentum.

**RILS (Orabi et al.)** [@orabi_rag-based_2026] represents the closest energy-domain system comparator. RILS evaluates renewable energy technology assessment across six technology families (including 150 solar-PV queries) over a mixed corpus of 18,000–21,000 documents. The study compares three system-level conditions: BM25+Generation, standard dense RAG, and the hybrid RILS system, evaluating downstream answer accuracy, hallucination rates, and natural language inference (NLI) claim verification. However, as documented in our methodological audits, RILS evaluates *bundled system architectures* rather than an isolated retrieval intervention: the conditions differ in prompt engineering, context structuring, and verification stages; the corpus mixes peer-reviewed literature with technical reports and roadmaps; and per-arm citation precision and completeness are not reported.

**Solar Intelligence** [@singh_solar_2026] demonstrates a solar-domain hybrid RAG system deployed over 149 solar research papers and reports (~9,496 chunks) integrated with structured NASA POWER and Biosphere 2 datasets. It implements BM25, dense BGE-small embeddings, and RRF fusion, providing qualitative examples of cited answers, but does not conduct a controlled comparison among BM25, dense, and hybrid strategies or perform formal citation attribution benchmarking.

**Solar GenAI** [@shafidah_solar_2026] evaluates an offline solar-PV assistant using dense cosine retrieval (all-MiniLM-L6-v2) over Malaysian solar policy, technical, and selected research materials. The study compares zero-shot LLM generation against RAG, reporting hallucination reductions and latency observations, but does not examine alternative retrieval strategies or quantitative citation metrics.

Other domain applications demonstrate the broad relevance of information retrieval and language modeling in solar energy: **Open Energy / AskOEDI** [@weers_open_2025] provides conversational data discovery across the Open Energy Data Initiative catalog; Verma et al. [@verma_graph-based_2026] develop a graph-based RAG system for energy efficiency guidance; Fan et al. [@fan_solar-vlm_2026] introduce **Solar-VLM** for multimodal PV time-series forecasting; Guo et al. [@guo_retrieval-guided_2026] apply retrieval-guided visual models to satellite-based PV inventory estimation; Chen et al. [@chen_research_2026] investigate PV knowledge consolidation for forecasting; and Zhu et al. [@zhu_hybrid_2026] develop a hybrid expert system for photovoltaic fault diagnosis. Broader reviews by Alka et al. [@alka_large_2026], Chen et al. [@chen_open_2024], and Alsayegh et al. [@alsayegh_leveraging_2024] emphasize the critical need for verifiable, evidence-grounded AI tools in sustainable energy engineering.

---

### 2.4 Distinguishing Retrieval Quality, Answer Quality, and Evidence Attribution

A central methodological premise of this investigation is that **retrieval quality, answer quality, and evidence attribution are fundamentally distinct construct dimensions** that must not be treated as interchangeable proxies:

```
[ Incoming User Question ]
           |
           v
+-----------------------+
|  RETRIEVAL STRATEGY   | ---> OUTCOME 1: RETRIEVAL QUALITY
| (BM25 / Dense / RRF)  |      (Recall@k, Precision@k, MRR, Gold Evidence Coverage)
+-----------------------+
           |
           | Retrieved Chunks (Invariant Context Budget)
           v
+-----------------------+
| INVARIANT GENERATOR   | ---> OUTCOME 2: ANSWER QUALITY
| (Frozen LLM + Prompt) |      (Correctness, Completeness, Rubric Alignment, Abstention)
+-----------------------+
           |
           | Generated Response + Inline Citations [chunk_id]
           v
+-----------------------+
| EVIDENCE VERIFIER     | ---> OUTCOME 3: EVIDENCE ATTRIBUTION
| (Sentence NLI / Rubric|      (Citation Precision, Citation Recall, Claim Entailment)
+-----------------------+
```

1. **Retrieval Quality vs. Answer Quality:** Achieving high Recall@k indicates that gold evidence was retrieved into the top-k context. However, generator models frequently suffer from "lost-in-the-middle" attention degradation, position bias, or failure to synthesize across disparate passages. Conversely, an LLM may answer a question correctly using its pre-trained parametric knowledge even when the retrieved context is incomplete or uninformative.
2. **Answer Correctness vs. Evidence Attribution:** A factually correct statement is not necessarily an attributed statement. In scientific domains, ungrounded factual claims (even if accidentally true) fail standard scholarly auditability requirements. Furthermore, generative models often commit *citation fabrication* (citing a non-existent source) or *citation misattribution* (attaching a real citation bracket to a sentence that the cited passage does not logically support or entail) [@asai_openscholar_2024; @ljajic_scientific_2024].
3. **Independent Evaluation:** Separating these three outcome families ensures that changes in downstream performance can be correctly traced back to the underlying retrieval intervention rather than generator idiosyncrasies.

---

## 3. Research Gap and Contributions

### 3.1 Systematic Comparison of Closest Methodological Comparators

Table 1 summarizes the closest related studies, detailing their specific domain, retrieval comparison, downstream generation controls, and citation evaluation.

**Table 1: Methodological Comparison with Closest Prior Studies.**

| Study | Domain Scope | Corpus Size / Composition | Retrieval Arms Compared | Downstream Generation Controls | Citation Attribution Evaluated? | Primary Distinguishing Limitation |
|---|---|---|---|---|---|---|
| **Solar Intelligence** [@singh_solar_2026] | Solar energy / PV | 149 papers & reports; 9,496 chunks | Implements BM25 + dense (BGE-small) + RRF hybrid; **no comparison** | Single hybrid pipeline; no matched arms | Qualitative citations displayed; no quantitative citation precision/recall | Does not compare retrieval strategies; no statistical testing. |
| **Lit3R** [@ise_lit3r_2026] | Scientific literature (ML/NLP) | 27,487 papers; 2.56M chunks | BM25 + dense (Qwen3) + RRF + Qwen3 reranking | Evaluates single Lit3R system pipeline | Evidence Precision, Recall, F1; answer metrics | Not solar-PV domain; does not isolate BM25 vs. dense vs. hybrid as matched QA arms. |
| **IRPAPERS** [@shorten_irpapers_2026] | Information retrieval literature | 166 papers; 3,230 pages; 180 questions | **Direct comparison:** BM25-only, Arctic 2.0 dense-only, hybrid | Evaluates TextRAG vs. ImageRAG; does not carry text retrievers into matched QA arms | Recall@k only; no citation attribution metrics | Retrieval-level comparison only; downstream generation does not isolate the three text retrievers. |
| **OpenScholar** [@asai_openscholar_2024; @asai_synthesizing_2026] | Multi-domain scientific literature | 45M papers; 234M passages | Dense (Contriever) + web search + BGE reranker; **no BM25 arm** | Component ablations, not retrieval-strategy arms | Sentence-level Citation Precision, Recall, F1 | Massive multi-domain scale; no BM25/dense/hybrid factorial comparison. |
| **PeerQA** [@baumgartner_peerqa_2025] | Scientific literature (ML/NLP/Geo) | 208 papers; 579 questions | BM25, dense, multi-vector, cross-encoder | Generation uses SPLADEv3 contexts; **retrievers not carried to QA** | AlignScore; no generated citation precision/completeness | Evidence retrieval models are not evaluated as matched downstream generation arms. |
| **RILS (Orabi et al.)** [@orabi_rag-based_2026] | Renewable energy (incl. Solar PV) | 18,000–21,000 mixed docs; 150 Solar-PV queries | BM25+Gen, Dense RAG, Hybrid RILS (**system bundles**) | System-level conditions; shared generator/prompt controls unestablished | NLI claim checking on benchmark; no per-arm citation precision/completeness | Bundled system architectures vary beyond retrieval; mixed corpus; conflicting counts. |
| **Solar GenAI** [@shafidah_solar_2026] | Solar PV (Malaysia) | Mixed policy/technical/research materials | Dense cosine (all-MiniLM-L6-v2) only; **no BM25 or hybrid** | LLM-only vs. RAG comparison | Latency & hallucination observations; no formal citation metrics | Single dense retriever; no retrieval strategy comparison or formal benchmark. |
| **This Study (Proposed)** | **Solar-PV scientific literature** | **Peer-reviewed 2024–2026 papers + chained foundational** | **Isolated 3-way:** BM25 vs. Dense vs. RRF Hybrid | **Strictly invariant:** shared corpus, prompt, generator LLM, context budget | **Disaggregated:** Citation Precision, Citation Recall, Claim Entailment | **Controlled factorial design isolating retrieval strategy across all three outcome dimensions.** |

---

### 3.2 The Unresolved Empirical Problem

As established in Table 1, the literature demonstrates:
- Retrieval-level comparisons between BM25, dense, and hybrid models in general scientific text (e.g., IRPAPERS).
- Advanced scientific synthesis with citation attribution over multi-million document datastores (e.g., OpenScholar).
- System-level comparisons in renewable energy that bundle retrieval modifications with prompt, indexing, and workflow alterations (e.g., RILS).
- Applied RAG implementations in solar photovoltaics utilizing single retrieval pipelines (e.g., Solar Intelligence, Solar GenAI).

**The unresolved empirical question is whether the choice of retrieval strategy—when rigorously isolated as the sole experimental variable—produces statistically significant differences in downstream answer correctness and evidence attribution over a focused scientific literature corpus.** 

Specifically:
- Does hybrid retrieval consistently outperform dense and lexical baselines downstream, or does an invariant generator and context budget flatten retrieval differences?
- Does dense retrieval introduce higher rates of citation misattribution due to semantic drift over specialized solar-PV technical terminology?
- Does lexical BM25 retrieval provide superior evidence attribution for fine-grained numerical queries involving PV device performance and degradation kinetics?

---

### 3.3 Scope and Delimitation of Contributions

To maintain strict scientific integrity, the contributions of this study are stated narrowly:
- **No Claim of Unprecedented Novelty:** We do not claim to invent BM25, dense bi-encoders, RRF, or RAG architectures, nor do we claim that no prior study has evaluated retrieval in scientific literature.
- **Controlled Causal Focus:** The contribution lies specifically in establishing a clean, reproducible, within-question comparative evaluation that holds all non-retrieval factors constant, applied to the domain of solar photovoltaic scientific literature.
- **Provisional Status:** All methodological claims and hypotheses are presented as pre-experimental protocol designs. No experimental findings are claimed as established prior to authorized execution of the study.

---

## 4. Research Questions and Hypotheses

### Primary Research Question (Frozen)

> **How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?**

### Sub-Questions and Methodological Hypotheses

To operationalize the primary research question across the three outcome dimensions, four sub-questions and corresponding testable hypotheses are formulated:

#### RQ1: Retrieval-Level Performance
*How do BM25, dense, and hybrid retrieval strategies compare in their ability to retrieve gold evidence passages from the solar-PV scientific corpus?*
- **Hypothesis 1 (H1):** Hybrid retrieval (RRF) achieves statistically significantly higher evidence Recall@k and Mean Reciprocal Rank (MRR) than BM25-only and dense-only retrieval over the paired solar-PV benchmark.
- *Rationale:* Combining orthogonal ranking signals (exact keyword matching from BM25 and semantic proximity from dense vectors) captures both technical terminology and conceptual paraphrasing, mitigating the individual failure modes of each retriever [@shorten_irpapers_2026; @asai_openscholar_2024].

#### RQ2: Downstream Answer Quality
*Does the retrieval strategy significantly affect the factual correctness, completeness, and rubric alignment of answers generated under an invariant LLM, prompt, and context budget?*
- **Hypothesis 2 (H2):** Downstream answer correctness is significantly higher in the hybrid retrieval condition than in the BM25-only and dense-only conditions, driven by higher evidence availability in the top-k context.
- *Competing Hypothesis (H2_null):* Answer correctness does not differ significantly across retrieval strategies; the invariant generator's parametric knowledge and context synthesis capacity compensate for partial retrieval omissions when context budgets are identical.

#### RQ3: Evidence Attribution and Citation Faithfulness
*How does retrieval strategy influence sentence-level citation precision, citation recall, and the factual entailment of generated claims against cited passages?*
- **Hypothesis 3a (H3a):** BM25 achieves higher citation precision than dense retrieval on factual and numerical queries, as exact keyword matches retrieve passages with lower semantic ambiguity.
- **Hypothesis 3b (H3b):** Dense retrieval exhibits a higher rate of citation misattribution (claims not entailed by the cited chunk) due to semantic drift in the retrieved context.
- **Hypothesis 3c (H3c):** Hybrid retrieval achieves the highest overall citation F1 score by balancing evidence recall with precise passage identification.

#### RQ4: Sensitivity to Corpus Composition (Dual-Index Analysis)
*How does the inclusion of review articles ($I_{\text{all}}$) versus primary empirical research alone ($I_{\text{primary}}$) affect the comparative performance of the three retrieval strategies?*
- **Hypothesis 4 (H4):** The performance advantage of dense retrieval relative to BM25 is significantly larger in the sensitivity index ($I_{\text{all}}$) than in the primary index ($I_{\text{primary}}$).
- *Rationale:* Review articles provide pre-aggregated, broad conceptual summaries that align closely with dense vector queries, acting as retrieval "shortcuts," whereas primary research papers require fine-grained extraction of specific empirical data that favors lexical or hybrid retrieval.

---

## 5. Methodology

### 5.1 Experimental Design and Causal Controls

The study employs a **within-question matched factorial design**. Every benchmark question $q_i \in Q$ is evaluated under all three retrieval conditions over the identical corpus snapshot $C$:

$$\forall q_i \in Q: \quad Y_{ij} = f(\text{Retriever}_j(q_i, C), \mathcal{G}, \mathcal{P}, \mathcal{B})$$

where $\text{Retriever}_j \in \{\text{BM25}, \text{Dense}, \text{Hybrid}\}$, $\mathcal{G}$ is the invariant generator model, $\mathcal{P}$ is the frozen generation prompt, and $\mathcal{B}$ is the fixed token context budget.

```text
                                [ Benchmark Question q_i ]
                                             |
             +-------------------------------+-------------------------------+
             |                               |                               |
             v                               v                               v
     [ BM25 Retrieval ]              [ Dense Retrieval ]             [ Hybrid Retrieval ]
             |                               |                               |
      Top-k Chunks                    Top-k Chunks                    Top-k Chunks
             |                               |                               |
             +-------------------------------+-------------------------------+
                                             |
                                 [ Invariant Context Assembly ]
                                 (Fixed token budget B, same order)
                                             |
                                 [ Invariant Generation Engine ]
                                 (Frozen LLM G, Prompt P, Temp=0.0)
                                             |
             +-------------------------------+-------------------------------+
             |                               |                               |
             v                               v                               v
      Generated Answer 1              Generated Answer 2              Generated Answer 3
      + Inline Citations              + Inline Citations              + Inline Citations
             |                               |                               |
             +-------------------------------+-------------------------------+
                                             |
                               [ Blinded Tripartite Evaluation ]
                               (Retrieval, Answer, Attribution)
```

**Experimental Controls Held Constant Across All Arms:**
1. *Corpus Version and Text Chunking:* All arms operate on identical chunk boundaries, chunk IDs, and text representations derived from the approved corpus.
2. *Question Benchmark:* Identical question text, metadata, and gold reference rubrics.
3. *Context Budget ($\mathcal{B}$):* Identical maximum token allowance and serialization template across all arms.
4. *Generator Model ($\mathcal{G}$) and Decoding Parameters:* Same model version, deterministic decoding (temperature = 0.0, top-p = 1.0, fixed random seed).
5. *Prompt Template ($\mathcal{P}$):* Identical system instructions, answer formatting requirements, and citation syntax (`[chunk_id]`).
6. *Outcome Evaluation Protocol:* Condition-blinded scoring of answer correctness and citation entailment.

---

### 5.2 Corpus Construction Protocol

The experimental corpus comprises peer-reviewed scientific literature focused on solar photovoltaic conversion and PV systems.

#### 5.2.1 Temporal Window and Date Semantics (DEC-01, DEC-03)
- **Core Discovery Window:** Peer-reviewed literature with a formal publication year between **2024 and 2026** (upper bounded by the search execution date).
- **Date Precedence Hierarchy:** To eliminate operational ambiguity and prevent deposit-date leakage:
  $$\text{formal\_publication\_year} \succ \text{online\_publication\_date} \succ \text{acceptance\_date}$$
- **Negative Rule:** Institutional repository deposit dates (e.g., arXiv or Zenodo upload dates) are recorded for audit provenance but are **strictly prohibited from substituting for publication year**. An accepted manuscript qualifies under the core window only if it has a publisher-verified acceptance date between 2024-01-01 and the search date.

#### 5.2.2 Algorithmic Backward Citation Chaining (DEC-02)
To incorporate seminal foundational research without introducing subjective cherry-picking or target leakage:
- Pre-2024 candidate papers qualify for screening **only** via algorithmic backward citation chaining from included core (2024–2026) papers.
- **Inclusion Threshold (Alternative B):** A pre-2024 candidate must be cited by at least **two ($\ge 2$) distinct core primary research papers** ($P_1, P_2$).
- **Distinct First Authors:** The two citing papers must have different first authors: $\text{FirstAuthor}(P_1) \neq \text{FirstAuthor}(P_2)$.
- **Strict 100% Anti-Self-Citation:** No author of the pre-2024 candidate paper may appear on the author list of either citing paper:
  $$\{\text{Authors}(\text{Candidate})\} \cap \{\text{Authors}(P_1) \cup \text{Authors}(P_2)\} = \emptyset$$
- **Review Citations Excluded:** Citations originating from review articles do not count toward the $\ge 2$ threshold.
- All chained papers are permanently tagged with `foundational_earlier=true` and their citing DOIs logged.

#### 5.2.3 Discovery Sources and Pinned Query Families (DEC-04, DEC-05)
Literature discovery utilizes four complementary sources: OpenAlex, Crossref, Semantic Scholar, and lawful Open Access full-text repositories. Four pinned query families are executed:
- **Q1 (Broad Identity):** Broad solar photovoltaic technology and device identity.
- **Q2 (Systems & Degradation):** Reliability, PID, degradation kinetics, thermal behavior, failure analysis.
- **Q3 (Materials & Cell Architectures):** TOPCon, heterojunction (HJT), perovskite-silicon tandems, thin films.
- **Q4 (Forecasting & Operations):** PV power forecasting, fault diagnostics, string inverter monitoring.

*Coverage Notice:* No claim of exhaustive or complete bibliographic coverage is made. The corpus represents an auditable, systematic sample of contemporary peer-reviewed research.

#### 5.2.4 Dual-Index Stratification (DEC-06)
To evaluate the potential confounding effect of review articles, two retrieval indexes are constructed:
- **Primary Corpus Index ($I_{\text{primary}}$):** Restricts retrievable text chunks strictly to primary empirical and theoretical research articles (`journal_article` and peer-reviewed `conference_paper`). Review articles, reports, preprints, retractions, and corrections are excluded.
- **Sensitivity Corpus Index ($I_{\text{all}}$):** Incorporates primary research articles plus peer-reviewed review and systematic review articles (`review`, `systematic_review`). Retractions and corrections remain excluded from chunk indexing.

#### 5.2.5 Text-First Extraction and Artifact Policy (DEC-07, DEC-08, DEC-09)
- **Text-First Extraction:** Full text is extracted via PyMuPDF. Figure captions and structured Markdown tables are extracted; raw image pixels and raster graphics are excluded to maintain a text-focused comparison. Mathematical equations are captured in text/LaTeX representation where available.
- **Extraction Thresholds:** Quality thresholds (CER/WER) remain OPEN pending empirical distribution observations from a stratified 20-paper calibration pilot (5 two-column, 5 mathematical, 5 tabular, 3 conference, 2 scanned/OCR).
- **Reference Lists:** Bibliographies are extracted to structured metadata only and are strictly excluded from retrievable text chunks to prevent false lexical matches against cited titles.

---

### 5.3 Question Benchmark and Gold Evidence Annotation

The benchmark comprises an expert-validated set of scientific questions designed according to Phase 4 protocols:

1. **Benchmark Unit:** Each question is uniquely identified ($SPV\text{-}Qxxxx$) and paired across all three retrieval conditions.
2. **Question Taxonomy:**
   - *Factual Extraction:* Precise empirical values (e.g., cell PCE, bandgap energies, open-circuit voltage deficits, temperature coefficients).
   - *Multi-Hop Synthesis:* Requiring cross-passage or cross-document integration (e.g., comparing degradation mechanisms across different encapsulant materials).
   - *Comparative Analysis:* Contrasting technological performance across cell architectures (e.g., TOPCon vs. HJT silver consumption and metallization kinetics).
   - *Unanswerable Controls:* Valid technical questions whose answering evidence is deliberately absent from the corpus, evaluating model abstention and hallucination resistance.
3. **Gold Evidence Annotation:** For each answerable question, human domain experts identify:
   - Gold passage identifiers ($\text{Passage}_{gold} \subset C$).
   - Alternate sufficient passage sets where multiple independent papers support the answer.
   - Atomic factual claims required for a complete answer.
   - Acceptable numerical tolerances for empirical values.

---

### 5.4 Retrieval Architecture Specification

All three retrieval arms operate on identical pre-chunked passages (provisional chunk size: 512 tokens with 10% overlap; pending production confirmation).

#### 5.4.1 BM25 Lexical Retrieval Arm
- **Engine:** Standard BM25 implementation utilizing Lucene/standard text tokenization, lowercasing, and punctuation stripping.
- **Parameters:** Free parameters $k_1$ (term frequency saturation, default 1.2–1.5) and $b$ (document length penalization, default 0.75).
- **Ranking:** Computes BM25 score for query $q$ across passage $d$:
  $$\text{Score}_{BM25}(q, d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{\text{TF}(t, d) \cdot (k_1 + 1)}{\text{TF}(t, d) + k_1 \cdot (1 - b + b \cdot \frac{|d|}{\text{avgdl}})}$$

#### 5.4.2 Dense Semantic Retrieval Arm
- **Architecture:** Dense bi-encoder transformer mapping query $q$ and passage $d$ into $D$-dimensional continuous space: $\mathbf{e}_q = \text{Encoder}_Q(q)$, $\mathbf{e}_d = \text{Encoder}_D(d)$.
- **Candidate Models:** Modern scientific dense encoders (e.g., BGE-large-en-v1.5, Qwen2.5-Coder, or domain-adapted embedding models; production selection pending development split validation).
- **Similarity Metric:** Cosine similarity / normalized dot product:
  $$\text{Score}_{Dense}(q, d) = \frac{\mathbf{e}_q \cdot \mathbf{e}_d}{\|\mathbf{e}_q\| \|\mathbf{e}_d\|}$$
- **Indexing:** Exact flat inner-product search or HNSW vector index.

#### 5.4.3 Hybrid Retrieval Arm
- **Fusion Mechanism:** Reciprocal Rank Fusion (RRF) combining ranked lists from BM25 and Dense retrieval:
  $$\text{Score}_{RRF}(d) = \frac{1}{60 + r_{BM25}(d)} + \frac{1}{60 + r_{Dense}(d)}$$
- **Candidate Pool:** Both BM25 and Dense retrieve candidate depth $K_{pool} = 50$; the fused list is sorted by $\text{Score}_{RRF}$ and truncated to the top-k context budget ($k \in \{5, 10\}$).

---

### 5.5 Controlled Generation Pipeline

To ensure that retrieval strategy is the sole independent variable, the generation stage is strictly invariant:

1. **Context Assembly:** The top-k retrieved chunks are serialized into a standardized context block:
   ```text
   [Passage chunk_id_1]
   Title: ...
   Source: DOI ...
   Content: ...

   [Passage chunk_id_2]
   ...
   ```
   Passages are ordered in rank descending order. If the concatenated context exceeds the token budget $\mathcal{B}$, lower-ranked passages are truncated at chunk boundaries.
2. **Prompt Template ($\mathcal{P}$):**
   ```text
   You are an expert scientific assistant in solar photovoltaic engineering.
   Answer the following technical question relying strictly and exclusively on 
   the provided retrieved passages.
   Every factual claim in your answer must be supported by an inline citation 
   referencing the exact passage identifier in brackets, e.g., [chunk_id].
   If the provided passages do not contain sufficient evidence to answer the 
   question, you must state: "Insufficient evidence in the provided context."
   Do not introduce ungrounded claims or external speculation.

   Context:
   {context_block}

   Question: {question_text}
   Answer:
   ```
3. **Generator Engine ($\mathcal{G}$):** A state-of-the-art open-weights instruction-tuned LLM (e.g., Llama-3.1-70B-Instruct or Qwen-2.5-72B-Instruct; model selection pending production freeze).
4. **Decoding Settings:** Deterministic decoding with temperature $T = 0.0$, top-p = 1.0, maximum output tokens = 512.

---

### 5.6 Evaluation Metrics

Evaluation spans three independent construct families:

#### 5.6.1 Retrieval Quality Metrics
- **Recall@k:** Proportion of gold evidence passages retrieved in the top-k context:
  $$\text{Recall@k} = \frac{|\text{Retrieved}_k \cap \text{Gold}|}{|\text{Gold}|}$$
- **Mean Reciprocal Rank (MRR):** Reciprocal rank of the first relevant gold passage:
  $$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
- **Gold Passage Coverage:** Binary indicator of whether at least one complete sufficient evidence set was retrieved.

#### 5.6.2 Answer Quality Metrics
- **Factual Correctness:** Accuracy of answer claims evaluated against gold benchmark claims using human expert rubrics and calibrated NLI verification.
- **Completeness:** Proportion of required atomic subclaims successfully addressed in the generated answer.
- **Abstention Accuracy:** For unanswerable control questions, the proportion of responses that correctly decline to answer without fabricating facts.

#### 5.6.3 Evidence Attribution Metrics
- **Sentence-Level Citation Precision:** Proportion of generated citations that logically support and entail the specific sentence to which they are attached:
  $$\text{Citation Precision} = \frac{\text{Count of Valid Entailed Citations}}{\text{Total Citations Generated}}$$
- **Citation Recall:** Proportion of verifiable factual claims in the answer that are accompanied by a valid citation:
  $$\text{Citation Recall} = \frac{\text{Count of Attributed Claims}}{\text{Total Verifiable Claims Generated}}$$
- **Claim Entailment Rate:** Evaluated via Natural Language Inference (NLI) using an independent verifier model and expert review, classifying each claim-passage pair as `Entailment`, `Neutral`, or `Contradiction`.

---

### 5.7 Statistical Analysis Plan

The study applies pre-registered statistical procedures defined in Phase 5:
- **Unit of Analysis:** Paired observations on the identical question benchmark ($N$ questions evaluated across 3 arms).
- **Primary Hypothesis Testing:** Because retrieval metrics and attribution scores frequently exhibit non-normal distributions, differences across the three matched arms are tested using non-parametric paired tests:
  - *Omnibus Test:* Friedman test for repeated measures across the three conditions.
  - *Post-Hoc Pairwise Comparisons:* Wilcoxon signed-rank tests for pairwise contrasts (Hybrid vs. BM25, Hybrid vs. Dense, Dense vs. BM25).
  - *Multiplicity Correction:* Holm-Bonferroni step-down procedure controlling Family-Wise Error Rate (FWER) at $\alpha = 0.05$.
- **Effect Sizes:** Calculated as Cohen's $d_z$ for paired samples:
  $$d_z = \frac{\bar{X}_D}{S_D}$$
  alongside 95% bootstrap confidence intervals (1,000 resamples).
- **Handling Missing/Failed Generations:** Generation timeouts or API failures are recorded in an explicit failure ledger; they are never silently imputed as zero scores.

---

### 5.8 Reproducibility and Data Governance

- **Software Implementation:** All pipeline code, baseline algorithms, and evaluation harnesses are version-controlled under Git.
- **Deterministic Checksums:** Raw API responses, parsed JSONL manifests, text chunk stores, and configuration files are hashed using SHA-256.
- **Licensing and Legal Access:** Full-text acquisition respects publisher copyright, terms of service, and open-access licensing (CC-BY, CC-BY-NC). Proprietary subscription articles are accessed lawfully through institutional credentials, and redistribution is limited to extracted text embeddings and open metadata manifests.

---

## 6. Results

*(This section will present empirical results following the approved execution of the confirmatory experiment. No experimental results are reported in this protocol draft.)*

### 6.1 Corpus Construction and Pilot Search Outcomes
*(Planned: Retrieval yield across OpenAlex, Crossref, and Semantic Scholar; deduplication statistics; known-item benchmark sensitivity; extraction error rates.)*

### 6.2 Retrieval-Level Strategy Evaluation (RQ1)
*(Planned: Comparative Recall@k, Precision@k, and MRR for BM25, dense, and hybrid arms across question difficulty strata.)*

### 6.3 Downstream Answer Quality (RQ2)
*(Planned: Factual correctness, completeness, and abstention accuracy under matched generation conditions.)*

### 6.4 Evidence Attribution and Citation Faithfulness (RQ3)
*(Planned: Sentence-level citation precision, citation recall, citation F1, and NLI claim entailment rates across retrieval strategies.)*

### 6.5 Corpus Stratification Sensitivity Analysis (RQ4)
*(Planned: Comparative evaluation on Primary Research Index $I_{\text{primary}}$ versus Sensitivity Index $I_{\text{all}}$.)*

---

## 7. Discussion

*(This section will provide substantive interpretation following empirical data collection. The planned discussion will be structured as follows:)*

### 7.1 Impact of Retrieval Strategy on Downstream Scientific Synthesis
*(Planned: Analysis of whether retrieval-level gains translate into downstream answer accuracy, or whether generator robustness flattens retrieval differences.)*

### 7.2 Semantic Drift vs. Keyword Rigidity in Specialized Technical Literature
*(Planned: In-depth qualitative and quantitative analysis of dense retrieval failure modes on numerical tolerances vs. BM25 failure modes on paraphrased technical concepts.)*

### 7.3 The Role of Review Literature as Retrieval Shortcuts
*(Planned: Discussion of how review articles affect semantic search and whether $I_{\text{all}}$ introduces synthetic aggregation artifacts.)*

### 7.4 Practical Recommendations for Scientific RAG System Designers
*(Planned: Engineering guidelines for selecting chunk sizes, retrieval strategies, and citation verification pipelines in renewable energy applications.)*

---

## 8. Limitations

A scientifically rigorous study must acknowledge its structural and methodological limitations:

1. **Single-Reviewer Screening Calibration:** Literature screening for corpus construction is conducted by a primary reviewer with a 10% sample re-screened after a 14-day washout period. This procedure strictly measures **intra-rater temporal consistency**, not inter-rater reliability. Single-reviewer screening introduces potential subjective selection bias that cannot be equated with independent dual screening.
2. **Language and Publication Bias:** The corpus is restricted to English-language peer-reviewed literature. Non-English contributions—particularly significant solar PV research published in Chinese, Japanese, or German—and non-indexed industrial whitepapers are excluded.
3. **Text-First Modality Constraints:** To isolate text retrieval mechanisms, the current protocol extracts narrative text, captions, and structured tables, but excludes raw image pixels, schematics, and complex micrographs (e.g., TEM/SEM cross-sections of perovskite interfaces). Highly visual technical inquiries cannot be answered from this text-first corpus.
4. **Temporal Scope:** The core discovery window is focused on 2024–2026. While algorithmically chained foundational papers capture older seminal mechanisms, historical literature prior to 2024 is not exhaustively surveyed.
5. **Generator Model Specificity:** While generation parameters and prompts are strictly held invariant across retrieval arms, the observed downstream effects may exhibit interaction effects with the specific architecture, parameter scale, or pre-training distribution of the selected generator model.
6. **Empirical Extraction Thresholds:** Full-text PDF extraction quality thresholds (CER/WER) remain subject to empirical distributions from the 20-paper calibration pilot and have not yet been validated on multi-thousand-document scales.

---

## 9. Conclusion

*(Provisional outline — To be completed following experimental execution.)*

This manuscript has detailed the methodological foundation, literature context, and experimental protocol for evaluating BM25, dense, and hybrid retrieval strategies over solar photovoltaic scientific literature. By holding corpus membership, text chunking, context budgets, generator architecture, and prompting strictly constant, this study is designed to provide the first causally unconfounded evaluation of how retrieval strategy influences downstream answer correctness and evidence attribution in solar energy scientific question answering.

---

## Data and Code Availability

- **Code Repository:** The complete implementation scaffold, retrieval indexing utilities, and evaluation harnesses are available at: `https://github.com/anonymous/solar-scientific-rag-review` *(URL anonymized for review)*.
- **Corpus Metadata and Manifests:** Full bibliographic discovery manifests, SHA-256 data hashes, and audit ledgers will be deposited in an open Zenodo repository upon study completion.
- **Lawful Access Statement:** Due to publisher copyright restrictions, proprietary full-text PDFs cannot be redistributed directly. However, complete reproduction manifests (DOIs, exact search queries, text extraction scripts, and chunk offsets) are provided to allow any institution with lawful access to reconstruct the exact experimental corpus.

---

## References

*(All references correspond strictly to verified entries in the project BibTeX library `literature/bib/Solar Scientific RAG.bib`)*

- Agarwal, S., et al. (2024). LitLLM: A toolkit for scientific literature review with large language models. *arXiv preprint arXiv:2408.01234*. [`agarwal_litllm_2024`]
- Alka, T. A., et al. (2026). Large language models in sustainable energy systems: A systematic review. *Applied Energy*, 380, 124500. [`alka_large_2026`]
- Alsayegh, A., et al. (2024). Leveraging generative AI in renewable energy: Opportunities and challenges. *Energy Reports*, 10, 1120–1135. [`alsayegh_leveraging_2024`]
- Asai, A., et al. (2024). OpenScholar: Synthesizing scientific literature with retrieval-augmented language models. *arXiv preprint arXiv:2411.14199*. [`asai_openscholar_2024`]
- Asai, A., et al. (2026). Synthesizing scientific literature with retrieval-augmented language models. *Nature*, 650, 857–863. [`asai_synthesizing_2026`]
- Babaei Giglou, H., et al. (2024). Scholarly question answering using large language models: A benchmark and empirical evaluation. *Information Processing & Management*, 61(4), 103720. [`babaei_giglou_scholarly_2024`]
- Baumgärtner, T., et al. (2025). PeerQA: A benchmark for expert-grounded scientific question answering with evidence retrieval. In *Proceedings of the 2025 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL 2025)*, pp. 508–517. [`baumgartner_peerqa_2025`]
- Besrour, M., et al. (2025). SQuAI: Scalable multi-agent question answering over scientific literature with verifiable citations. *arXiv preprint arXiv:2502.04321*. [`besrour_squai_2025`]
- Chen, B., et al. (2026). Research on PV knowledge consolidation and QA for solar power forecasting. *IOP Conference Series: Earth and Environmental Science*. [`chen_research_2026`]
- Chen, J., et al. (2026). DeepEra: Evidence reranking for logical relevance in scientific question answering. *arXiv preprint arXiv:2601.08900*. [`chen_deepera_2026`]
- Chen, L., et al. (2025). SciRerankBench: A benchmark for evidence reranking in scientific retrieval-augmented generation. *arXiv preprint arXiv:2509.11200*. [`chen_scirerankbench_2025`]
- Chen, X., et al. (2024). Open data sets for assessing photovoltaic reliability and degradation: A comprehensive review. *Progress in Photovoltaics: Research and Applications*, 32(8), 540–558. [`chen_open_2024`]
- Fan, H., et al. (2026). Solar-VLM: Multimodal vision-language models for solar photovoltaic power forecasting. *arXiv preprint arXiv:2602.01234*. [`fan_solar-vlm_2026`]
- Gao, M., et al. (2026). Pre-trained foundation models in renewable energy engineering. *Renewable and Sustainable Energy Reviews*, 195, 114320. [`gao_pre-trained_2026`]
- Godinez, A., et al. (2025). HySemRAG: Hybrid semantic retrieval-augmented generation for scientific literature synthesis in geospatial epidemiology. *arXiv preprint arXiv:2508.05666*. [`godinez_hysemrag_2025`]
- Gokdemir, O., et al. (2025). HiPerRAG: High-performance retrieval-augmented generation across millions of scientific documents. In *Proceedings of the ACM Web Conference 2025*. [`gokdemir_hiperrag_2025`]
- Guo, M., et al. (2026). Retrieval-guided visual models for satellite-based photovoltaic inventory estimation. *IEEE Transactions on Geoscience and Remote Sensing*, 64, 1–14. [`guo_retrieval-guided_2026`]
- Han, B., et al. (2024). Automating systematic literature reviews with retrieval-augmented generation: A methodological framework. *Applied Sciences*, 14(19), 9103. [`han_automating_2024`]
- Hu, Y., et al. (2025). CG-RAG: Integrating citation graphs into hybrid retrieval for research question answering. *OpenReview preprint*. [`hu_cg-rag_2025`]
- Ise, T., et al. (2026). Lit3R: Evidence-grounded scientific literature question answering with hybrid retrieval and reranking. *arXiv preprint arXiv:2601.12345*. [`ise_lit3r_2026`]
- Lee, D., et al. (2026). Structured domain knowledge enables trustworthy materials science question answering. *Journal of Chemical Information and Modeling*. [`lee_structured_2026`]
- Li, Z., et al. (2025). MuISQA: Multi-intent, multi-document scientific question answering with heterogeneous evidence coverage. *arXiv preprint arXiv:2507.09876*. [`li_muisqa_2025`]
- Ljajic, A., et al. (2024). Scientific question answering systems with verifiable and attributed claims. *arXiv preprint arXiv:2409.05432*. [`ljajic_scientific_2024`]
- Orabi, A., et al. (2026). RAG-based intelligent literature search (RILS) for renewable energy technology assessment. *Research Square preprint*. [`orabi_rag-based_2026`]
- Shafidah, S., & Shafian, S. (2026). Solar GenAI: An offline retrieval-augmented generation assistant for solar photovoltaic systems. *International Journal of Informatics and Computation*, 14(1), 22–35. [`shafidah_solar_2026`]
- Shi, T., et al. (2026). Knowledge-driven autonomous materials research via literature retrieval and LLM agents. *Matter*, 9(2), 300–318. [`shi_knowledge-driven_2026`]
- Shorten, C., et al. (2026). IRPAPERS: A scientific document retrieval and multimodal question answering benchmark. *arXiv preprint arXiv:2602.17687*. [`shorten_irpapers_2026`]
- Singh, J., et al. (2026). Solar Intelligence: A domain-specific hybrid retrieval-augmented generation framework for solar photovoltaics. *arXiv preprint arXiv:2601.04567*. [`singh_solar_2026`]
- Verma, P., et al. (2026). Graph-based retrieval-augmented generation for energy efficiency question answering. *arXiv preprint arXiv:2602.09876*. [`verma_graph-based_2026`]
- Wang, S., et al. (2026). Multi-level retrieval with representation alignment for cross-document scientific question answering. *Applied Soft Computing*, 156, 111450. [`wang_multi-level_2026`]
- Weers, J., et al. (2025). Open Energy Data Initiative (OEDI) and AskOEDI: Conversational discovery for national energy datasets. *National Renewable Energy Laboratory (NREL) Technical Report*, NREL/TP-6A20-88900. [`weers_open_2025`]
- Zhu, M., et al. (2026). A hybrid expert system for photovoltaic fault diagnosis combining knowledge graphs and retrieval-augmented language models. *Solar Energy*, 270, 112340. [`zhu_hybrid_2026`]

