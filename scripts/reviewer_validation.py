from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


SOURCE_ACCESS_RANK = {
    "metadata_or_abstract": 0,
    "localized_excerpt": 1,
    "localized_full_text": 2,
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_COMPARISONS = {"ai_human", "human_human", "ai_ai"}


def _active(payload: dict[str, Any], today: date) -> bool:
    if payload.get("status") != "validated_for_scope":
        return False
    reviewer = payload.get("reviewer") or {}
    evidence = payload.get("evidence") or {}
    if not SHA256_RE.fullmatch(str(reviewer.get("configuration_sha256") or "")):
        return False
    if evidence.get("study_status") != "completed":
        return False
    if not str(evidence.get("preregistration") or "").strip():
        return False
    if not isinstance(evidence.get("sample_size"), int) or evidence.get("sample_size", 0) <= 0:
        return False
    if (
        not isinstance(evidence.get("human_reference_reviewers"), int)
        or evidence.get("human_reference_reviewers", 0) < 2
    ):
        return False
    if not REQUIRED_COMPARISONS.issubset(set(evidence.get("comparisons") or [])):
        return False
    if evidence.get("noninferiority_passed") is not True:
        return False
    margin = evidence.get("noninferiority_margin_critical_error_sensitivity")
    if (
        not isinstance(margin, (int, float))
        or isinstance(margin, bool)
        or not 0 < margin < 1
    ):
        return False
    sensitivity = evidence.get("critical_error_sensitivity") or {}
    if any(
        not isinstance(sensitivity.get(field), (int, float))
        or isinstance(sensitivity.get(field), bool)
        or not 0 <= sensitivity[field] <= 1
        for field in ("estimate", "ci_low", "ci_high")
    ):
        return False
    validity = payload.get("validity") or {}
    if not str(validity.get("content_commit") or "").strip():
        return False
    try:
        valid_from = date.fromisoformat(str(validity["valid_from"]))
        valid_until = date.fromisoformat(str(validity["valid_until"]))
    except (KeyError, TypeError, ValueError):
        return False
    return valid_from <= today <= valid_until


def find_applicable_validation(
    directory: Path,
    *,
    provider: str,
    model: str,
    model_version: str,
    prompt_id: str,
    rubric_version: str,
    domain: str,
    risk_level: str,
    claim_types: list[str],
    language: str,
    source_access: str,
    author_context_isolated: bool,
    blind_to_author_rationale: bool,
    today: date | None = None,
) -> dict[str, Any] | None:
    """Return an exact, active validation record or require provisional review."""
    current_date = today or date.today()
    observed_access = SOURCE_ACCESS_RANK.get(source_access, -1)
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict) or not _active(payload, current_date):
            continue

        reviewer = payload.get("reviewer") or {}
        if any(
            reviewer.get(key) != value
            for key, value in {
                "provider": provider,
                "model": model,
                "model_version": model_version,
                "prompt_id": prompt_id,
                "rubric_version": rubric_version,
            }.items()
        ):
            continue

        scope = payload.get("scope") or {}
        if domain not in set(scope.get("domains") or []):
            continue
        if risk_level not in set(scope.get("claim_risk_levels") or []):
            continue
        if not set(claim_types).issubset(set(scope.get("claim_types") or [])):
            continue
        if language not in set(scope.get("languages") or []):
            continue
        required_access = SOURCE_ACCESS_RANK.get(scope.get("source_access_required"), 99)
        if observed_access < required_access:
            continue

        independence = payload.get("independence") or {}
        if author_context_isolated and independence.get("author_context_isolated") is not True:
            continue
        if blind_to_author_rationale and independence.get("blind_to_author_rationale") is not True:
            continue

        authorization = payload.get("authorization") or {}
        if authorization.get("can_authorize_publication") is not True:
            continue
        if authorization.get("requires_zero_critical_findings") is not True:
            continue
        if authorization.get("abstain_out_of_scope") is not True:
            continue
        return payload
    return None
