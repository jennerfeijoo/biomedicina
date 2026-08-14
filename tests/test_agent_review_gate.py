from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from citonauta_agent.reviewer_validation import find_applicable_validation


def validated_manifest() -> dict:
    return {
        "validation_id": "VALID-001",
        "status": "validated_for_scope",
        "reviewer": {
            "provider": "ollama",
            "model": "review-model:1",
            "model_version": "sha256:model",
            "prompt_id": "prompt-v1",
            "rubric_version": "rubric-v1",
            "configuration_sha256": "a" * 64,
        },
        "scope": {
            "domains": ["bioestadistica"],
            "claim_risk_levels": ["medium"],
            "claim_types": ["definition", "method"],
            "languages": ["es"],
            "source_access_required": "localized_full_text",
        },
        "independence": {
            "author_context_isolated": True,
            "blind_to_author_rationale": True,
        },
        "validity": {
            "valid_from": "2026-01-01",
            "valid_until": "2026-12-31",
            "content_commit": "abc123",
        },
        "evidence": {
            "study_status": "completed",
            "preregistration": "https://example.org/protocol",
            "sample_size": 120,
            "human_reference_reviewers": 3,
            "comparisons": ["ai_human", "human_human", "ai_ai"],
            "noninferiority_margin_critical_error_sensitivity": 0.05,
            "noninferiority_passed": True,
            "critical_error_sensitivity": {
                "estimate": 0.96,
                "ci_low": 0.91,
                "ci_high": 0.99,
            },
        },
        "authorization": {
            "can_authorize_publication": True,
            "requires_zero_critical_findings": True,
            "abstain_out_of_scope": True,
        },
    }


class AgentReviewGateTests(unittest.TestCase):
    def find(self, payload: dict, **overrides):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "record.json").write_text(json.dumps(payload), encoding="utf-8")
            arguments = {
                "provider": "ollama",
                "model": "review-model:1",
                "model_version": "sha256:model",
                "prompt_id": "prompt-v1",
                "rubric_version": "rubric-v1",
                "domain": "bioestadistica",
                "risk_level": "medium",
                "claim_types": ["definition", "method"],
                "language": "es",
                "source_access": "localized_full_text",
                "author_context_isolated": True,
                "blind_to_author_rationale": True,
                "today": date(2026, 8, 14),
            }
            arguments.update(overrides)
            return find_applicable_validation(directory, **arguments)

    def test_exact_active_record_allows_validated_review(self) -> None:
        result = self.find(validated_manifest())
        self.assertIsNotNone(result)
        self.assertEqual(result["validation_id"], "VALID-001")

    def test_metadata_only_sources_cannot_use_full_text_validation(self) -> None:
        self.assertIsNone(
            self.find(validated_manifest(), source_access="metadata_or_abstract")
        )

    def test_model_change_invalidates_scope_match(self) -> None:
        self.assertIsNone(self.find(validated_manifest(), model="review-model:2"))

    def test_unvalidated_claim_type_invalidates_scope_match(self) -> None:
        self.assertIsNone(
            self.find(validated_manifest(), claim_types=["definition", "clinical"])
        )

    def test_unvalidated_record_cannot_authorize(self) -> None:
        payload = validated_manifest()
        payload["status"] = "unvalidated"
        self.assertIsNone(self.find(payload))


if __name__ == "__main__":
    unittest.main()
