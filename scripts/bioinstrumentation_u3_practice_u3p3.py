#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def diagnose(features: dict[str, float]) -> dict[str, object]:
    candidates: list[dict[str, object]] = []
    if features.get("line_ratio", 0.0) >= 0.35:
        candidates.append({"label": "power_line_interference", "mechanism": "coupling_common_mode_with_conversion", "test": "compare_50_60_hz_peak_and_impedance_balance"})
    if features.get("baseline_step", 0.0) >= 0.5:
        candidates.append({"label": "motion_or_contact_artifact", "mechanism": "interface_potential_or_impedance_change", "test": "inspect_contact_event_and_low_frequency_transient"})
    if features.get("clipped_fraction", 0.0) >= 0.02:
        candidates.append({"label": "saturation_or_clipping", "mechanism": "front_end_range_exceeded", "test": "compare_raw_range_and_gain_budget"})
    if features.get("high_frequency_burst", 0.0) >= 0.4:
        candidates.append({"label": "cable_or_non_target_biological_activity", "mechanism": "triboelectric_cable_motion_or_muscle_activity", "test": "repeat_with_cable_fixed_and_context_annotation"})
    return {
        "dominant": candidates[0]["label"] if candidates else "undetermined",
        "candidates": candidates,
        "requires_discriminating_test": True,
        "diagnostic_claim_is_not_clinical": True,
    }


def fixtures() -> dict[str, dict[str, float]]:
    return {
        "line_interference": {"line_ratio": 0.55, "baseline_step": 0.05, "clipped_fraction": 0.0, "high_frequency_burst": 0.1},
        "contact_motion": {"line_ratio": 0.08, "baseline_step": 0.85, "clipped_fraction": 0.0, "high_frequency_burst": 0.15},
        "clipping": {"line_ratio": 0.1, "baseline_step": 0.2, "clipped_fraction": 0.08, "high_frequency_burst": 0.1},
        "ambiguous_burst": {"line_ratio": 0.05, "baseline_step": 0.1, "clipped_fraction": 0.0, "high_frequency_burst": 0.7},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = {name: {"features": values, "diagnosis": diagnose(values)} for name, values in fixtures().items()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(payload)} diagnostic fixtures to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
