#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/review_packets/bioinstrumentacion-unit-02-human-execution.json"


def main() -> int:
    payload = json.loads(PACKET.read_text(encoding="utf-8"))
    assert payload["packet_id"] == "bioinstrumentacion-unit-02-human-execution-2026-07-30"
    assert payload["status"] == "frozen_pending_human_execution"
    assert payload["frozen_commit"] == "c628862637d0144fc5a8e52fadf98131ae161195"
    assert payload["coordination_issue"] == 171
    assert payload["professional_review_issue"] == 161
    roles = {item["role"] for item in payload["artifacts"]}
    assert roles == {
        "authoral_unit",
        "human_review_protocol",
        "internal_audit",
        "empty_cognitive_template",
        "empty_inter_rater_template",
    }
    for item in payload["artifacts"]:
        assert (ROOT / item["path"]).is_file(), item["path"]
    blocks = payload["required_human_blocks"]
    assert blocks["cognitive_sessions"]["minimum_completed"] == 3
    assert blocks["feedback_usability_reviews"]["minimum_reviewers"] == 2
    assert blocks["inter_rater_round"]["reviewer_count"] == 2
    assert blocks["professional_disciplinary_review"]["status"] == "pending_human_review"
    governance = payload["repository_governance"]
    assert governance["real_participant_data_committed"] is False
    assert governance["direct_identifiers_prohibited"] is True
    assert governance["clinical_or_sensitive_data_prohibited"] is True
    assert governance["ci_evidence_is_synthetic_only"] is True
    editorial = payload["editorial_state"]
    assert editorial == {
        "course": "pending",
        "unit_developed": False,
        "public_release_authorized": False,
        "human_evidence_present": False,
    }
    print("OK Bioinstrumentation U2 frozen human execution packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
