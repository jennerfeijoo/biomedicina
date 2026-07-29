#!/usr/bin/env python3
"""Calculate two-rater agreement for Bioinstrumentation unit 1 rubrics."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = (
    ROOT
    / "data"
    / "review_protocols"
    / "bioinstrumentacion-unit-01-human-review.json"
)


class AgreementError(ValueError):
    """Raised when a ratings payload or protocol is invalid."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AgreementError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AgreementError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AgreementError(f"{path} must contain an object")
    return payload


def load_thresholds(protocol_path: Path) -> dict[str, float | int]:
    protocol = load_json(protocol_path)
    review = protocol.get("inter_rater_review")
    if not isinstance(review, dict):
        raise AgreementError("protocol lacks inter_rater_review")
    thresholds = review.get("pilot_thresholds")
    if not isinstance(thresholds, dict):
        raise AgreementError("protocol lacks pilot thresholds")
    required = {
        "minimum_ordinal_exact_agreement",
        "maximum_ordinal_mean_absolute_difference",
        "minimum_ordinal_linear_weighted_kappa",
        "minimum_critical_flag_exact_agreement",
        "maximum_unresolved_critical_disagreements",
    }
    if set(thresholds) != required:
        raise AgreementError("pilot threshold fields changed unexpectedly")
    return thresholds


def _validate_payload(
    payload: dict[str, Any],
) -> tuple[list[int], list[int], list[bool], list[bool], list[int], list[dict[str, Any]]]:
    scale = payload.get("scale")
    ratings = payload.get("ratings")
    if not isinstance(scale, list) or len(scale) < 2:
        raise AgreementError("scale must contain at least two ordered categories")
    if any(not isinstance(value, int) for value in scale):
        raise AgreementError("scale categories must be integers")
    if scale != sorted(set(scale)):
        raise AgreementError("scale must be sorted and unique")
    if not isinstance(ratings, list) or not ratings:
        raise AgreementError("ratings must be a non-empty list")

    allowed = set(scale)
    seen: set[tuple[str, str]] = set()
    scores_a: list[int] = []
    scores_b: list[int] = []
    critical_a: list[bool] = []
    critical_b: list[bool] = []
    normalized: list[dict[str, Any]] = []

    for index, row in enumerate(ratings):
        if not isinstance(row, dict):
            raise AgreementError(f"rating {index} must be an object")
        artifact_id = row.get("artifact_id")
        criterion_id = row.get("criterion_id")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            raise AgreementError(f"rating {index} lacks artifact_id")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise AgreementError(f"rating {index} lacks criterion_id")
        key = (artifact_id, criterion_id)
        if key in seen:
            raise AgreementError(f"duplicated rating key: {artifact_id}/{criterion_id}")
        seen.add(key)

        score_a = row.get("rater_a")
        score_b = row.get("rater_b")
        flag_a = row.get("critical_a")
        flag_b = row.get("critical_b")
        if score_a not in allowed or score_b not in allowed:
            raise AgreementError(f"rating {artifact_id}/{criterion_id} uses an invalid score")
        if not isinstance(flag_a, bool) or not isinstance(flag_b, bool):
            raise AgreementError(
                f"rating {artifact_id}/{criterion_id} requires boolean critical flags"
            )
        scores_a.append(score_a)
        scores_b.append(score_b)
        critical_a.append(flag_a)
        critical_b.append(flag_b)
        normalized.append(
            {
                "artifact_id": artifact_id,
                "criterion_id": criterion_id,
                "rater_a": score_a,
                "rater_b": score_b,
                "critical_a": flag_a,
                "critical_b": flag_b,
            }
        )
    return scores_a, scores_b, critical_a, critical_b, scale, normalized


def _nominal_kappa(values_a: list[Any], values_b: list[Any]) -> float | None:
    if len(values_a) != len(values_b) or not values_a:
        raise AgreementError("nominal kappa requires paired non-empty ratings")
    n = len(values_a)
    observed = sum(a == b for a, b in zip(values_a, values_b, strict=True)) / n
    categories = set(values_a) | set(values_b)
    marginal_a = Counter(values_a)
    marginal_b = Counter(values_b)
    expected = sum(
        (marginal_a[category] / n) * (marginal_b[category] / n)
        for category in categories
    )
    denominator = 1.0 - expected
    if abs(denominator) < 1e-12:
        return None
    return (observed - expected) / denominator


def _linear_weighted_kappa(
    scores_a: list[int], scores_b: list[int], scale: list[int]
) -> float | None:
    if len(scores_a) != len(scores_b) or not scores_a:
        raise AgreementError("weighted kappa requires paired non-empty ratings")
    positions = {value: index for index, value in enumerate(scale)}
    maximum_distance = len(scale) - 1
    n = len(scores_a)

    def weight(left: int, right: int) -> float:
        return 1.0 - abs(positions[left] - positions[right]) / maximum_distance

    observed = sum(
        weight(left, right)
        for left, right in zip(scores_a, scores_b, strict=True)
    ) / n
    marginal_a = Counter(scores_a)
    marginal_b = Counter(scores_b)
    expected = sum(
        weight(left, right)
        * (marginal_a[left] / n)
        * (marginal_b[right] / n)
        for left in scale
        for right in scale
    )
    denominator = 1.0 - expected
    if abs(denominator) < 1e-12:
        return None
    return (observed - expected) / denominator


def _confusion_matrix(
    scores_a: list[int], scores_b: list[int], scale: list[int]
) -> list[list[int]]:
    positions = {value: index for index, value in enumerate(scale)}
    matrix = [[0 for _ in scale] for _ in scale]
    for left, right in zip(scores_a, scores_b, strict=True):
        matrix[positions[left]][positions[right]] += 1
    return matrix


def analyze_agreement(
    payload: dict[str, Any], thresholds: dict[str, float | int]
) -> dict[str, Any]:
    scores_a, scores_b, critical_a, critical_b, scale, ratings = _validate_payload(
        payload
    )
    count = len(scores_a)
    exact = sum(a == b for a, b in zip(scores_a, scores_b, strict=True)) / count
    mean_absolute_difference = sum(
        abs(a - b) for a, b in zip(scores_a, scores_b, strict=True)
    ) / count
    weighted_kappa = _linear_weighted_kappa(scores_a, scores_b, scale)
    critical_exact = sum(
        a == b for a, b in zip(critical_a, critical_b, strict=True)
    ) / count
    critical_kappa = _nominal_kappa(critical_a, critical_b)
    critical_disagreements = [
        {
            "artifact_id": row["artifact_id"],
            "criterion_id": row["criterion_id"],
            "critical_a": row["critical_a"],
            "critical_b": row["critical_b"],
        }
        for row in ratings
        if row["critical_a"] != row["critical_b"]
    ]

    checks = {
        "ordinal_exact_agreement": exact
        >= float(thresholds["minimum_ordinal_exact_agreement"]),
        "ordinal_mean_absolute_difference": mean_absolute_difference
        <= float(thresholds["maximum_ordinal_mean_absolute_difference"]),
        "ordinal_linear_weighted_kappa": weighted_kappa is not None
        and weighted_kappa
        >= float(thresholds["minimum_ordinal_linear_weighted_kappa"]),
        "critical_flag_exact_agreement": critical_exact
        >= float(thresholds["minimum_critical_flag_exact_agreement"]),
        "unresolved_critical_disagreements": len(critical_disagreements)
        <= int(thresholds["maximum_unresolved_critical_disagreements"]),
    }

    def rounded(value: float | None) -> float | None:
        return None if value is None else round(value, 6)

    return {
        "fixture_id": payload.get("fixture_id"),
        "synthetic": payload.get("synthetic") is True,
        "rating_count": count,
        "scale": scale,
        "ordinal_confusion_matrix": {
            "rows_rater_a": scale,
            "columns_rater_b": scale,
            "counts": _confusion_matrix(scores_a, scores_b, scale),
        },
        "ordinal_exact_agreement": rounded(exact),
        "ordinal_mean_absolute_difference": rounded(mean_absolute_difference),
        "ordinal_linear_weighted_kappa": rounded(weighted_kappa),
        "critical_flag_exact_agreement": rounded(critical_exact),
        "critical_flag_unweighted_kappa": rounded(critical_kappa),
        "unresolved_critical_disagreements": critical_disagreements,
        "gate_checks": checks,
        "gate_passed": all(checks.values()),
        "interpretation": (
            "Internal pilot gate only; inspect the confusion matrix and disagreements. "
            "Metrics do not establish content validity or reviewer competence."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON ratings payload")
    parser.add_argument(
        "--protocol", type=Path, default=DEFAULT_PROTOCOL, help="review protocol JSON"
    )
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    parser.add_argument(
        "--enforce", action="store_true", help="exit with status 1 when the gate fails"
    )
    args = parser.parse_args()

    try:
        report = analyze_agreement(load_json(args.input), load_thresholds(args.protocol))
    except AgreementError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.enforce and not report["gate_passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
