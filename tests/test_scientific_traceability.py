from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_scientific_traceability.py"
SPEC = importlib.util.spec_from_file_location("validate_scientific_traceability", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def registry() -> dict:
    return {
        "schema_version": "1.0",
        "subject_id": "bioestadistica",
        "content_version": "1.0.0",
        "content_commit": "abc123",
        "claims": [
            {
                "claim_id": "BIO-U01-C001",
                "unit": 1,
                "text": "La afirmación sometida a trazabilidad.",
                "claim_type": "method",
                "risk": "high",
                "source_id": "SRC-001",
                "locator": {"page": 12, "section": "2.1"},
                "support": "direct",
                "source_verification_status": "verified_directly",
                "review_state": "ai_review_provisional",
                "reviewer_validation_id": None,
            }
        ],
    }


class ScientificTraceabilityTests(unittest.TestCase):
    def test_high_risk_claim_with_direct_locator_is_valid(self) -> None:
        self.assertEqual(MODULE.validate_registry(registry()), [])

    def test_high_risk_claim_without_locator_is_rejected(self) -> None:
        payload = registry()
        payload["claims"][0]["locator"] = {}
        errors = MODULE.validate_registry(payload)
        self.assertTrue(any("localizador exacto" in error for error in errors))

    def test_claim_without_positive_unit_is_rejected(self) -> None:
        payload = registry()
        payload["claims"][0].pop("unit")
        errors = MODULE.validate_registry(payload)
        self.assertTrue(any("unit debe ser un entero positivo" in error for error in errors))

    def test_validated_claim_requires_validation_record(self) -> None:
        payload = registry()
        payload["claims"][0]["review_state"] = "ai_review_validated"
        errors = MODULE.validate_registry(payload)
        self.assertTrue(any("reviewer_validation_id" in error for error in errors))

    def test_unknown_canonical_source_is_rejected(self) -> None:
        errors = MODULE.validate_registry(
            registry(),
            source_records={"OTHER": {"verification_status": "verified_directly"}},
        )
        self.assertTrue(any("no existe en el registro canónico" in error for error in errors))

    def test_claim_must_exist_in_declared_unit(self) -> None:
        errors = MODULE.validate_registry(
            registry(),
            content_strings={1: ["Otro contenido"]},
        )
        self.assertTrue(any("no aparece en la unidad canónica" in error for error in errors))

    def test_claim_matching_canonical_source_and_content_is_valid(self) -> None:
        errors = MODULE.validate_registry(
            registry(),
            source_records={"SRC-001": {"verification_status": "verified_directly"}},
            content_strings={1: ["La afirmación sometida a trazabilidad."]},
        )
        self.assertEqual(errors, [])

    def test_direct_claim_cannot_use_metadata_only_source(self) -> None:
        errors = MODULE.validate_registry(
            registry(),
            source_records={"SRC-001": {"verification_status": "verified_metadata"}},
        )
        self.assertTrue(any("no está verificada directamente" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
