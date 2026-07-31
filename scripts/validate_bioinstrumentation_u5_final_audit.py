from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/final_authoral_audits/bioinstrumentacion-unit-05.json"
UNIT = ROOT / "data/course_redevelopment/bioinstrumentacion/units/unit-05.json"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    unit = json.loads(UNIT.read_text(encoding="utf-8"))

    assert audit["subject_id"] == "bioinstrumentacion"
    assert audit["unit"] == 5
    assert audit["status"] == "final_authoral_audit_passed_internal"
    assert audit["course_editorial_state"] == "pending"
    assert unit["status"] == "authoral_draft_internal_review"

    dimensions = audit["dimensions"]
    assert len(dimensions) == 8
    assert all(item["decision"] == "pass_internal" for item in dimensions)

    findings = audit["binding_findings"]
    assert findings == {
        "U5-F01": "resolved_in_authoral_draft",
        "U5-F02": "resolved_in_authoral_draft",
    }

    assert unit["audit_findings_resolved"]["U5-F01"].startswith("resolved_")
    assert unit["audit_findings_resolved"]["U5-F02"].startswith("resolved_")

    u5a5 = audit["review_packages"]["U5-A5"]
    assert u5a5["type"] == "real_human_review"
    assert u5a5["status"] == "prepared_not_executed"
    assert u5a5["automatic_approval_allowed"] is False

    disciplinary = audit["review_packages"]["disciplinary_review"]
    assert disciplinary["status"] == "prepared_not_executed"
    assert disciplinary["approval_claimed"] is False

    release = audit["release_decision"]
    assert release["internal_authoral_audit_passed"] is True
    for key in (
        "human_review_executed",
        "professional_review_executed",
        "professional_approval_claimed",
        "public_release_authorized",
        "course_completion_authorized",
    ):
        assert release[key] is False, key

    print("Bioinstrumentation Unit 5 final authoral audit validated.")


if __name__ == "__main__":
    main()
