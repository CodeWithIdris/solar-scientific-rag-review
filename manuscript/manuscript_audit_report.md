# Scientific Manuscript Integrity Audit Report — Version 0.2

**Project:** Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature  
**Date:** 2026-10-21  
**Audit Target:** `manuscript/manuscript_v0_1.md` $\rightarrow$ `manuscript/manuscript_v0_2.md`  
**Status:** AUDIT COMPLETE — MANUSCRIPT HARDENED — RESEARCHER APPROVAL PENDING ON OPEN DECISIONS  

---

## 1. Executive Summary

This audit critically evaluated `manuscript_v0_1.md` against project evidence notes, the master bibliography (`Solar Scientific RAG.bib`), and the consolidated protocol registers. The primary objectives were:
1. Eliminating premature certainty, ungrounded novelty assertions, and directional bias in hypotheses.
2. Aligning every literature claim with verified evidence locations and documenting discrepancies transparently.
3. Establishing strict demarcation between frozen design principles, proposed implementation choices, pilot-dependent parameters, and unperformed experimental work.

The manuscript has been upgraded to **Version 0.2** (`manuscript/manuscript_v0_2.md`), with all 50 substantive claims audited in [`manuscript/evidence_and_claim_register.csv`](./evidence_and_claim_register.csv).

---

## 2. Critical and Major Scientific Problems Found in Version 0.1

### Problem 1: Unqualified Novelty and Universal Absence Claims (Critical)
- **Finding:** In Section 3.1 and the claim register, statements asserted that *"No prior study isolates BM25, dense, and hybrid retrieval as the sole experimental variable over a shared solar-PV literature corpus."*
- **Critique:** Universal negative assertions ("no prior work exists") cannot be scientifically substantiated merely because our focused screening pass did not locate one. Furthermore, paywalled or recently published literature (e.g., Wang et al., ScienceDirect 2026) remains partially uninspected.
- **Remediation in v0.2:** Re-framed as an explicitly bounded observation: *"Within our screened literature base (synthesized in Table 1), prior studies have not isolated BM25, dense, and hybrid retrieval as the sole independent variable across matched downstream generation and citation-attribution arms in a solar-PV scientific literature corpus. Pending completion of systematic screening and full-text verification across pending records (notably Wang et al.), this study proposes a controlled comparison under shared downstream conditions..."*

### Problem 2: Directional Bias and Competing Hypotheses in RQ2 & RQ3 (Major)
- **Finding:** Hypothesis 2 (H2) asserted as a matter of anticipated fact that downstream answer correctness *would* be significantly higher in hybrid retrieval than in BM25 or dense retrieval. Hypothesis 3 asserted that BM25 *would* achieve higher citation precision and that dense retrieval *would* exhibit higher semantic drift.
- **Critique:**
  1. *Downstream Generator Compensation:* In an invariant generation pipeline with a matched context budget, an instruction-tuned LLM can compensate for partial retrieval omissions via parametric knowledge or summarization capacity, potentially flattening downstream answer correctness differences.
  2. *Lexical Misattribution:* BM25 can retrieve passages mentioning keywords out of context (e.g., in background literature reviews or negative results), which can cause citation misattribution just as dense semantic drift does.
- **Remediation in v0.2:**
  - Formulated H2 alongside an explicit competing null hypothesis ($H2_{null}$) testing whether the invariant generator compensates for retrieval differences.
  - Narrowed H3a strictly to fine-grained numerical queries, and framed H3b (general citation precision across complex queries) non-directionally.
  - Re-framed H4 (review literature impact in $I_{\text{all}}$) as an exploratory non-directional sensitivity question.

### Problem 3: Concealment of Paywalled Literature Limitations (Major)
- **Finding:** In v0.1, Wang et al. (`wang_multi-level_2026`) was cited in Section 2.2 without prominent disclosure that its publisher full text remains inaccessible behind ScienceDirect paywalls.
- **Critique:** Citing a paper's abstract while discussing its detailed retrieval and benchmarking controls risks misleading peer reviewers regarding the extent of verified evidence.
- **Remediation in v0.2:** Added an explicit caveat in Section 2.2, Table 1, and the claim register (`CLM-017`) stating that full text was unavailable after multiple targeted attempts, and that its detailed retrieval arms and controls are unestablished.

### Problem 4: Premature Certainty on Pilot-Dependent Thresholds and Power (Major)
- **Finding:** Certain technical parameters (e.g., CER/WER extraction cutoffs, benchmark sample size guaranteeing statistical power, server-side API sorting) were phrased as if fixed or assured.
- **Critique:**
  1. Setting arbitrary numeric extraction cutoffs prior to observation risks mass rejection of valid mathematical papers.
  2. Power ($1-\beta \ge 0.80$) cannot be guaranteed by merely declaring a target sample size ($N=100\text{--}200$); it depends on observed variance across arms.
  3. Server-side API sorting syntax on public endpoints requires live empirical verification.
- **Remediation in v0.2:** Explicitly labeled all implementation choices as provisional, designated CER/WER thresholds as **OPEN** pending the 20-paper pilot, and replaced claims of guaranteed statistical power with a pre-registered plan to calculate Minimum Detectable Effect Sizes (MDES) and 95% bootstrap confidence intervals.

---

## 3. Comprehensive Summary of Changes Made in Version 0.2

1. **Research Gap and Novelty Claims (Section 1, Section 3):**
   - Replaced all absolute novelty assertions with scoped claims bounded by the screened evidence base.
   - Updated Table 1 with explicit footnotes identifying paywalled full-text limitations (`wang_multi-level_2026`).
2. **Background and Related Work (Section 2):**
   - Section 2.2: Preserved documented count discrepancies in OpenScholar (237M embeddings in abstract vs. 234M passages in methods; 2,967 questions vs. 2.2k teaser vs. 208 long-form expert answers).
   - Section 2.3: Preserved documented corpus count discrepancies in RILS (18,000 docs/28,800 passages in Table 1 vs. 21,000 docs/32,800 passages in §6.2) and date discrepancies in Solar Intelligence (1994–2026 in text vs. 1994–2006 in Table 1).
   - Explicitly clarified that RILS bundles system components beyond retrieval and does not isolate retrieval strategy.
3. **Hypotheses Formulation (Section 4):**
   - H1: Retained as directional strictly for retrieval-level evidence recall.
   - H2: Paired directional H2 with competing null $H2_{null}$.
   - H3: Narrowed H3a strictly to fine-grained numerical queries; framed H3b non-directionally.
   - H4: Converted into an exploratory, non-directional sensitivity hypothesis.
   - Explicitly noted that hypotheses are protocol proposals awaiting researcher sign-off, not preregistered facts.
4. **Methodological Precision (Section 5):**
   - Clearly categorized components into (A) Frozen study design, (B) Proposed implementation choices, (C) Pilot-dependent decisions, and (D) Unperformed work.
   - Clarified that `repository_deposit_date` is strictly prohibited from substituting for qualifying publication year.
   - Marked candidate dense embedding models, chunk size/overlap, generator LLM, prompt template, and RRF parameters as provisional.
   - Replaced claims of guaranteed statistical power with MDES and bootstrap interval procedures.
5. **Traceability Register Expansion:**
   - Expanded [`manuscript/evidence_and_claim_register.csv`](./evidence_and_claim_register.csv) from 7 to 10 columns, adding `evidence_location`, `support_level`, `discrepancies`, and `action_required`.
   - Audited all 50 claims; confirmed 100% RFC-4180 CSV compliance.

---

## 4. Claims Requiring Full Text or External Verification

| Claim ID | Citation Key | Paper Title / Venue | Verified Source Content | Missing / Unverified Details | Required Action |
|---|---|---|---|---|---|
| **CLM-017** | `wang_multi-level_2026` | Multi-level retrieval with representation alignment... (*Applied Soft Computing* 2026) | ScienceDirect PII `S1568494626000979` highlights and abstract snippets. | Full text is paywalled/inaccessible. Stated task is cross-document scientific QA over SciLitQA (>50k pairs), but exact retrieval arms, baselines, generator controls, and attribution metrics are unestablished. | Disclose abstract-only status in manuscript; do not infer missing methodology. Attempt full-text acquisition if institutional access expands. |
| **CLM-026** | `chen_research_2026` | Research on PV knowledge consolidation and QA for solar power forecasting (*IOP Conf. Ser.* 2026) | Conference abstract only; publisher full text unavailable. | Stated task is specialized PV-QA for forecasting; scientific-paper corpus composition and retrieval arms are unestablished. | Disclose abstract-only status; retain as background application context only. |

---

## 5. Hypotheses Recommended for Formal Researcher Decision

The four hypotheses in Section 4 are submitted for formal researcher review and sign-off:

1. **RQ1 / Hypothesis 1 (Retrieval Quality):**
   - *Recommendation:* **RETAIN AS DIRECTIONAL.** Prior benchmarks (IRPAPERS, Lit3R) strongly support that RRF hybrid retrieval achieves higher evidence Recall@k than individual lexical or dense retrievers.
2. **RQ2 / Hypothesis 2 (Downstream Answer Quality):**
   - *Recommendation:* **RETAIN WITH COMPETING RIVAL NULL ($H2$ vs. $H2_{null}$).** Evaluating whether retrieval differences survive the generation bottleneck is a core empirical contribution of this study; assuming downstream superiority a priori is methodologically unjustified.
3. **RQ3 / Hypothesis 3 (Evidence Attribution & Faithfulness):**
   - *Recommendation:* **NARROW TO NUMERICAL QUERIES (H3a) AND MAKE GENERAL ATTRIBUTION NON-DIRECTIONAL (H3b).** BM25's advantage is defensible for exact numbers/formulas, but lexical keyword matching in complex narrative text does not guarantee higher attribution precision.
4. **RQ4 / Hypothesis 4 (Corpus Stratification Sensitivity):**
   - *Recommendation:* **RETAIN AS EXPLORATORY / NON-DIRECTIONAL.** Investigating whether review articles introduce semantic aggregation shortcuts should be evaluated as an open empirical question.

---

## 6. Remaining Blockers to Pilot Execution

Before Phase 9 (Pilot Execution) can begin, the following **two critical blockers** must be resolved:

1. **CRITICAL BLOCKER 1: Nomination of 10 Known-Item DOIs (DEC-05):**
   - Table 2.2.3 in [`phase8_2_signoff_checklist.md`](../notes/methodology/phase8_2_signoff_checklist.md) requires 10 verified peer-reviewed 2024 solar-PV paper Titles and DOIs across the 5 technical subdomains. Without these DOIs, query sensitivity cannot be measured during the 300-slot pilot search.
2. **CRITICAL BLOCKER 2: Formal Approval of Citation Chaining Alternative B (DEC-02):**
   - Formal sign-off on Alternative B (Distinct First Authors + 100% Candidate Anti-Self-Citation) to replace the unexecutable "corresponding author" API assumption.

---

## 7. Exact Next Action Needed from the Researcher

To unlock Phase 9 (Pilot Execution) and authorize discovery search:
1. Review the revised manuscript ([`manuscript/manuscript_v0_2.md`](./manuscript_v0_2.md)) and audit report.
2. Confirm the recommended hypothesis formulations in Section 5.
3. Approve Alternative B for citation chaining in [`protocol_closure_register.md`](../notes/methodology/protocol_closure_register.md) (DEC-02).
4. Supply the 10 paper Titles and DOIs for Table 2.2.3 (DEC-05).

**Real-paper discovery, paper scraping, benchmark construction, and confirmatory experiment execution remain strictly BLOCKED until these actions are completed.**

