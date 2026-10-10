from __future__ import annotations

import unittest

from solar_rag.corpus import (
    CorpusValidationError,
    normalize_doi,
    normalize_title,
    stable_document_id,
)
from solar_rag.corpus_workflow import (
    CorpusCandidate,
    build_corpus_manifest,
    document_record_id,
    duplicate_candidate_records,
    extraction_status_is_valid,
    license_status_is_valid,
    peer_review_status_is_valid,
    retraction_flags,
    screening_status_is_valid,
    summarize_corpus,
    validate_candidate_metadata,
)


class CorpusWorkflowValidationTests(unittest.TestCase):
    def test_candidate_validation_requires_metadata(self) -> None:
        with self.assertRaises(ValueError):
            validate_candidate_metadata({})

    def test_candidate_validation_requires_non_empty_strings(self) -> None:
        valid = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for field in ("record_id", "title", "source_name", "search_query", "search_date"):
            data = dict(valid)
            data[field] = "   "
            with self.assertRaises(ValueError):
                validate_candidate_metadata(data)

    def test_source_url_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        # Valid URLs
        for url in ("https://doi.org/10.1000/1", "http://example.com/paper"):
            candidate = validate_candidate_metadata({**base, "source_url": url})
            self.assertEqual(candidate.source_url, url)

        # Invalid URLs
        for url in ("ftp://example.com", "example.com/paper", "relative/path"):
            with self.assertRaises(ValueError):
                validate_candidate_metadata({**base, "source_url": url})

    def test_screening_status_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for status in ("not_assessed", "include_core", "include_context", "potentially_relevant", "exclude"):
            cand = validate_candidate_metadata({**base, "screening_status": status})
            self.assertEqual(cand.screening_status, status)
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "screening_status": "invalid_status"})

    def test_overlap_level_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for level in ("none", "low", "moderate", "high", "critical"):
            cand = validate_candidate_metadata({**base, "overlap_level": level})
            self.assertEqual(cand.overlap_level, level)
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "overlap_level": "extreme"})

    def test_confidence_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for conf in ("low", "medium", "high"):
            cand = validate_candidate_metadata({**base, "confidence": conf})
            self.assertEqual(cand.confidence, conf)
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "confidence": "uncertain"})

    def test_peer_review_status_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for prs in ("not_checked", "peer_reviewed", "not_peer_reviewed", "unclear"):
            cand = validate_candidate_metadata({**base, "peer_review_status": prs})
            self.assertEqual(cand.peer_review_status, prs)
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "peer_review_status": "bogus_peer_review"})

    def test_license_status_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for lic in ("not_recorded", "cc_by", "cc_by_sa", "other", "rights_unclear", "no_license_info"):
            cand = validate_candidate_metadata({**base, "license_status": lic})
            self.assertEqual(cand.license_status, lic)
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "license_status": "unrestricted"})

    def test_full_text_status_validation(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        for fts in ("not_checked", "not_found", "open_access", "subscriber_only", "partial_text", "extracted", "not_applicable"):
            cand = validate_candidate_metadata({**base, "full_text_status": fts})
            self.assertEqual(cand.full_text_status, fts)
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "full_text_status": "illegal_pirate"})

    def test_failed_and_partial_extraction_require_outcome_note(self) -> None:
        for extraction_status in ("failed", "partial"):
            candidate = CorpusCandidate(
                record_id="r1",
                title="Study title",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                extraction_status=extraction_status,
                extraction_note=None,
            )
            with self.assertRaises(ValueError):
                validate_candidate_metadata(candidate)

            candidate_with_note = CorpusCandidate(
                record_id="r1",
                title="Study title",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                extraction_status=extraction_status,
                extraction_note="Figures excluded due to OCR limit",
            )
            self.assertIsNotNone(validate_candidate_metadata(candidate_with_note))

    def test_status_helper_functions(self) -> None:
        self.assertTrue(screening_status_is_valid("include_core"))
        self.assertFalse(screening_status_is_valid("random"))
        self.assertTrue(extraction_status_is_valid("successful"))
        self.assertFalse(extraction_status_is_valid("random"))
        self.assertTrue(peer_review_status_is_valid("peer_reviewed"))
        self.assertFalse(peer_review_status_is_valid("random"))
        self.assertTrue(license_status_is_valid("cc_by"))
        self.assertFalse(license_status_is_valid("random"))


class DoiAndTitleNormalizationTests(unittest.TestCase):
    def test_doi_normalization_variants(self) -> None:
        expected = "10.1016/j.solmat.2023.112345"
        variants = [
            "10.1016/j.solmat.2023.112345",
            "10.1016/J.SOLMAT.2023.112345",
            "  10.1016/j.solmat.2023.112345  ",
            "https://doi.org/10.1016/j.solmat.2023.112345",
            "http://dx.doi.org/10.1016/j.solmat.2023.112345",
            "HTTPS://DOI.ORG/10.1016/J.SOLMAT.2023.112345",
            "doi:10.1016/j.solmat.2023.112345",
            "DOI: 10.1016/j.solmat.2023.112345 ",
            "https://doi.org/10.1016/j.solmat.2023.112345?utm_source=crossref",
            "https://doi.org/10.1016/j.solmat.2023.112345#page=1",
            "https://dx.doi.org/10.1016/j.solmat.2023.112345/",
        ]
        for variant in variants:
            self.assertEqual(normalize_doi(variant), expected, f"Failed for variant: {variant}")

    def test_doi_normalization_rejects_malformed(self) -> None:
        malformed = [
            "not_a_doi",
            "https://doi.org/",
            "doi:",
            "  ",
            "",
            "100.1000/invalid",
        ]
        for val in malformed:
            self.assertEqual(normalize_doi(val), "", f"Expected empty for: {val}")

    def test_candidate_doi_validation_rejects_malformed_doi(self) -> None:
        candidate = CorpusCandidate(
            record_id="r1",
            title="Study title",
            source_name="Crossref",
            search_query="solar pv",
            search_date="2026-10-01",
            doi="malformed-doi-value",
        )
        with self.assertRaises(ValueError):
            validate_candidate_metadata(candidate)

    def test_title_normalization_unicode_and_whitespace(self) -> None:
        self.assertEqual(
            normalize_title("  Perovskite \n\t Solar   Cell: Efficiency  "),
            "perovskite solar cell: efficiency",
        )
        # Unicode NFKC ligature and full-width decomposition
        self.assertEqual(
            normalize_title("ﬁlms ａｎｄ ＰＶ"),
            "films and pv",
        )
        # German sharp S
        self.assertEqual(
            normalize_title("Großflächige Module"),
            "grossflächige module",
        )


class PublicationYearCoercionTests(unittest.TestCase):
    def test_publication_year_coercion_valid(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        self.assertEqual(validate_candidate_metadata({**base, "publication_year": 2024}).publication_year, 2024)
        self.assertEqual(validate_candidate_metadata({**base, "publication_year": "2024"}).publication_year, 2024)
        self.assertEqual(validate_candidate_metadata({**base, "publication_year": " 2024 "}).publication_year, 2024)
        self.assertIsNone(validate_candidate_metadata({**base, "publication_year": None}).publication_year)
        self.assertIsNone(validate_candidate_metadata({**base, "publication_year": ""}).publication_year)

    def test_publication_year_coercion_invalid(self) -> None:
        base = {
            "record_id": "r1",
            "title": "Study Title",
            "source_name": "Crossref",
            "search_query": "solar pv",
            "search_date": "2026-10-01",
        }
        # Booleans must be rejected
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "publication_year": True})
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "publication_year": False})

        # Out-of-range years
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "publication_year": 999})
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "publication_year": 2201})

        # Non-numeric strings
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "publication_year": "invalid_year"})
        with self.assertRaises(ValueError):
            validate_candidate_metadata({**base, "publication_year": "2024-05-01"})


class StableDocumentIdTests(unittest.TestCase):
    def test_stable_document_id_deterministic(self) -> None:
        first = document_record_id(
            CorpusCandidate(
                record_id="r1",
                title="Perovskite tandem solar cell performance",
                source_name="Crossref",
                search_query="perovskite tandem",
                search_date="2026-10-01",
                doi="10.1000/example2",
                publication_year=2023,
            )
        )
        second = document_record_id(
            CorpusCandidate(
                record_id="r2",
                title="Perovskite tandem solar cell performance",
                source_name="OpenAlex",
                search_query="perovskite tandem",
                search_date="2026-10-01",
                doi="https://doi.org/10.1000/example2",
                publication_year=2025,
            )
        )
        self.assertEqual(first, second)

    def test_stable_document_id_without_doi_distinguishes_years(self) -> None:
        doc_2024 = stable_document_id(doi=None, title="Solar PV degradation", year=2024)
        doc_2025 = stable_document_id(doi=None, title="Solar PV degradation", year=2025)
        doc_none = stable_document_id(doi=None, title="Solar PV degradation", year=None)
        self.assertNotEqual(doc_2024, doc_2025)
        self.assertNotEqual(doc_2024, doc_none)
        self.assertNotEqual(doc_2025, doc_none)

    def test_stable_document_id_empty_raises(self) -> None:
        with self.assertRaises(CorpusValidationError):
            stable_document_id(doi=None, title="   ", year=None)


class DuplicateDetectionAndScreeningTests(unittest.TestCase):
    def test_duplicate_detection_flags_shared_doi_and_title(self) -> None:
        candidates = [
            CorpusCandidate(
                record_id="r1",
                title="A solar PV efficiency study",
                source_name="Crossref",
                search_query="solar pv efficiency",
                search_date="2026-10-01",
                doi="10.1000/example1",
                publication_year=2024,
            ),
            CorpusCandidate(
                record_id="r2",
                title="A solar PV efficiency study",
                source_name="Semantic Scholar",
                search_query="solar pv efficiency",
                search_date="2026-10-01",
                doi="10.1000/example1",
                publication_year=2024,
            ),
        ]
        duplicates = duplicate_candidate_records(candidates)
        self.assertEqual(duplicates[0]["kind"], "doi")
        self.assertIn("r1", duplicates[0]["record_ids"])
        self.assertIn("r2", duplicates[0]["record_ids"])

    def test_false_positive_title_collision_requires_review(self) -> None:
        candidates = [
            CorpusCandidate(
                record_id="r1",
                title="A solar pv reliability study",
                source_name="Crossref",
                search_query="solar pv reliability",
                search_date="2026-10-01",
            ),
            CorpusCandidate(
                record_id="r2",
                title="A solar pv reliability study",
                source_name="Google Scholar",
                search_query="solar pv reliability",
                search_date="2026-10-01",
                publication_year=2022,
            ),
        ]
        duplicates = duplicate_candidate_records(candidates)
        title_dupes = [item for item in duplicates if item["kind"] == "title"]
        self.assertTrue(len(title_dupes) > 0)
        self.assertEqual(title_dupes[0]["status"], "review_required")

    def test_same_doi_with_conflicting_metadata_flagged_as_duplicate(self) -> None:
        candidates = [
            CorpusCandidate(
                record_id="r1",
                title="Original Published Title",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                doi="10.1016/j.solmat.2023.100",
                publication_year=2023,
            ),
            CorpusCandidate(
                record_id="r2",
                title="Slightly Altered Publisher Title",
                source_name="OpenAlex",
                search_query="solar pv",
                search_date="2026-10-01",
                doi="https://doi.org/10.1016/j.solmat.2023.100",
                publication_year=2024,
            ),
        ]
        duplicates = duplicate_candidate_records(candidates)
        doi_dupes = [d for d in duplicates if d["kind"] == "doi"]
        self.assertEqual(len(doi_dupes), 1)
        self.assertEqual(doi_dupes[0]["status"], "duplicate")
        self.assertEqual(set(doi_dupes[0]["record_ids"]), {"r1", "r2"})

    def test_unique_records_produce_no_duplicate_flags(self) -> None:
        candidates = [
            CorpusCandidate(
                record_id="r1",
                title="Paper A",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                doi="10.1000/1",
            ),
            CorpusCandidate(
                record_id="r2",
                title="Paper B",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                doi="10.1000/2",
            ),
        ]
        duplicates = duplicate_candidate_records(candidates)
        self.assertEqual(len(duplicates), 0)


class RetractionAndCorrectionTests(unittest.TestCase):
    def test_retracted_and_corrected_documents_are_flagged(self) -> None:
        # All suspicious/actionable statuses must trigger review_required="yes"
        for status in ("retracted", "correction_pending", "corrected", "review_required"):
            cand1 = CorpusCandidate(
                record_id="r1",
                title="Title",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                retraction_status=status,
            )
            self.assertEqual(retraction_flags(cand1)["review_required"], "yes")

            cand2 = CorpusCandidate(
                record_id="r2",
                title="Title",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                correction_status=status,
            )
            self.assertEqual(retraction_flags(cand2)["review_required"], "yes")

    def test_unproblematic_status_does_not_trigger_review(self) -> None:
        cand = CorpusCandidate(
            record_id="r1",
            title="Title",
            source_name="Crossref",
            search_query="solar pv",
            search_date="2026-10-01",
            retraction_status="not_retracted",
            correction_status="not_checked",
        )
        self.assertEqual(retraction_flags(cand)["review_required"], "no")


class ManifestAndProvenanceIntegrityTests(unittest.TestCase):
    def test_manifest_reconciles_all_counts(self) -> None:
        candidates = [
            CorpusCandidate(
                record_id="r1",
                title="Alpha",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                screening_status="include_core",
                extraction_status="successful",
                full_text_status="open_access",
            ),
            CorpusCandidate(
                record_id="r2",
                title="Beta",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                screening_status="potentially_relevant",
                extraction_status="partial",
                extraction_note="OCR only; figures omitted",
                full_text_status="partial_text",
            ),
            CorpusCandidate(
                record_id="r3",
                title="Gamma",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                screening_status="include_context",
                extraction_status="not_started",
            ),
            CorpusCandidate(
                record_id="r4",
                title="Delta",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                screening_status="exclude",
                extraction_status="failed",
                extraction_note="Corrupt PDF payload",
            ),
        ]
        manifest = build_corpus_manifest(
            candidates,
            corpus_name="test_corpus",
            search_query="solar pv",
            search_date="2026-10-01",
            version="v0.1.0-test",
        )
        self.assertEqual(manifest["record_count"], 4)
        self.assertEqual(manifest["inclusion_count"], 2)  # include_core + include_context
        self.assertEqual(manifest["open_or_unassessed"], 1)  # potentially_relevant
        self.assertEqual(manifest["screening_status_counts"]["exclude"], 1)

        # Reconciliation check
        total_screening = sum(manifest["screening_status_counts"].values())
        self.assertEqual(total_screening, manifest["record_count"])

        total_extraction = sum(manifest["extraction_status_counts"].values())
        self.assertEqual(total_extraction, manifest["record_count"])

        reconciled_sum = (
            manifest["inclusion_count"]
            + manifest["open_or_unassessed"]
            + manifest["screening_status_counts"]["exclude"]
        )
        self.assertEqual(reconciled_sum, manifest["record_count"])

        summary = summarize_corpus(
            candidates,
            corpus_name="test_corpus",
            search_query="solar pv",
            search_date="2026-10-01",
            version="v0.1.0-test",
        )
        self.assertEqual(summary["record_count"], 4)
        self.assertEqual(summary["inclusion_count"], 2)
        self.assertEqual(summary["open_or_unassessed"], 1)
        self.assertEqual(summary["sha256"], manifest["sha256"])

    def test_manifest_deterministic_hash(self) -> None:
        candidates = [
            CorpusCandidate(
                record_id="r1",
                title="Alpha",
                source_name="Crossref",
                search_query="solar pv",
                search_date="2026-10-01",
                screening_status="include_core",
                extraction_status="successful",
            ),
        ]
        m1 = build_corpus_manifest(
            candidates,
            corpus_name="test",
            search_query="query",
            search_date="2026-10-01",
            version="v1",
        )
        m2 = build_corpus_manifest(
            candidates,
            corpus_name="test",
            search_query="query",
            search_date="2026-10-01",
            version="v1",
        )
        self.assertEqual(m1["sha256"], m2["sha256"])
        self.assertEqual(len(m1["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
