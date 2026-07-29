#!/usr/bin/env python3
"""Validate the executable practice infrastructure for Bioinstrumentation U1."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "generate_bioinstrumentation_thermal_dataset.py"
HEADER_AUDITOR_PATH = ROOT / "scripts" / "audit_wfdb_header.py"
FIXTURE_PATH = (
    ROOT
    / "data"
    / "practice_fixtures"
    / "bioinstrumentacion"
    / "mitdb-100"
    / "100.hea"
)
ATTRIBUTION_PATH = FIXTURE_PATH.parent / "ATTRIBUTION.md"
CONTRACT_PATH = (
    ROOT
    / "data"
    / "practice_implementations"
    / "bioinstrumentacion-unit-01.json"
)
PACKAGE_PATH = (
    ROOT
    / "data"
    / "course_plan_packages"
    / "package-04-bioinstrumentation-excellence-pilot.json"
)
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
AUTHORAL_UNIT_PATH = (
    ROOT
    / "data"
    / "course_redevelopment"
    / "bioinstrumentacion"
    / "units"
    / "unit-01.json"
)
DOC_PATH = (
    ROOT
    / "docs"
    / "pilots"
    / "bioinstrumentacion"
    / "unit-01"
    / "PRACTICE_IMPLEMENTATION.md"
)


def load_module(path: Path, name: str) -> ModuleType:
    if not path.exists():
        raise ValueError(f"missing {path.relative_to(ROOT)}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise ValueError(f"missing {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def validate_thermal(generator: ModuleType) -> str:
    params = generator.ThermalParameters(noise_std_c=0.0)
    rows = generator.simulate(params)
    expected_count = int(round(params.duration_s / params.dt_s)) + 1
    if len(rows) != expected_count:
        raise ValueError(
            f"thermal row count expected {expected_count}, got {len(rows)}"
        )
    if list(rows[0]) != list(generator.FIELDNAMES):
        raise ValueError("thermal columns do not match the declared field order")

    step_index = int(round(params.step_time_s / params.dt_s))
    tau_index = int(round((params.step_time_s + params.tau_s) / params.dt_s))
    five_tau_index = int(
        round((params.step_time_s + 5 * params.tau_s) / params.dt_s)
    )
    baseline = rows[step_index]["T_s_C"]
    target = rows[step_index]["T_d_C"]
    total_change = target - baseline
    if total_change == 0:
        raise ValueError("thermal step must produce a non-zero change")
    fraction_tau = (rows[tau_index]["T_s_C"] - baseline) / total_change
    if not math.isclose(
        fraction_tau, 1 - math.exp(-1), rel_tol=0, abs_tol=1e-9
    ):
        raise ValueError(f"one-tau fraction invalid: {fraction_tau}")
    fraction_five_tau = (
        rows[five_tau_index]["T_s_C"] - baseline
    ) / total_change
    if fraction_five_tau <= 0.99:
        raise ValueError(
            f"five-tau fraction must exceed 0.99, got {fraction_five_tau}"
        )

    post_step = [row["T_s_C"] for row in rows[step_index:]]
    if any(b < a for a, b in zip(post_step, post_step[1:])):
        raise ValueError("ideal first-order response must be monotonic")
    if max(post_step) > target + 1e-12:
        raise ValueError("ideal first-order response must not overshoot")
    if any(
        row["T_d_C"] != row["T_u_C"] + params.contact_bias_c
        for row in rows
    ):
        raise ValueError(
            "T_d must remain distinct from T_u through the declared contact bias"
        )

    noisy = generator.ThermalParameters()
    same_a = generator.csv_bytes(generator.simulate(noisy))
    same_b = generator.csv_bytes(generator.simulate(noisy))
    different = generator.csv_bytes(
        generator.simulate(generator.ThermalParameters(seed=noisy.seed + 1))
    )
    if same_a != same_b:
        raise ValueError("thermal generation is not deterministic for the same seed")
    if same_a == different:
        raise ValueError("changing the seed must change the noisy indication")

    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path, manifest_path = generator.write_outputs(Path(temp_dir), noisy)
        payload = csv_path.read_bytes()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(payload).hexdigest()
        if manifest["outputs"]["sha256"] != digest:
            raise ValueError("thermal manifest hash does not match CSV bytes")
        if manifest["outputs"]["row_count"] != expected_count:
            raise ValueError("thermal manifest row count is incorrect")
        limitations = " ".join(manifest["limitations"]).lower()
        for marker in ("not validated", "diagnosis", "device validation"):
            if marker not in limitations:
                raise ValueError(
                    f"thermal manifest lacks limitation marker: {marker}"
                )
    return hashlib.sha256(same_a).hexdigest()


def validate_header(auditor: ModuleType) -> None:
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    metadata = auditor.parse_wfdb_header(text)
    errors = auditor.audit_record_100(metadata)
    if errors:
        raise ValueError("record 100 fixture failed audit: " + "; ".join(errors))
    if len(metadata.comments) != 2:
        raise ValueError("record 100 fixture must preserve two comment lines")
    malformed = text.replace("100 2 360 650000", "100 3 360 650000", 1)
    try:
        auditor.parse_wfdb_header(malformed)
    except ValueError:
        pass
    else:
        raise ValueError("malformed signal count must be rejected")


def validate_contract(thermal_hash: str) -> None:
    contract = load_json(CONTRACT_PATH)
    if contract.get("status") != "implemented_internal_review":
        raise ValueError("practice implementation status is incorrect")
    if contract.get("course_editorial_state") != "pending":
        raise ValueError("practice implementation must keep course pending")
    if contract.get("full_theory_drafting_authorized") is not False:
        raise ValueError(
            "practice implementation must not authorize full theory drafting"
        )
    practices = contract.get("practices")
    if not isinstance(practices, list) or len(practices) != 2:
        raise ValueError("contract must contain exactly two executable practices")
    ids = {item.get("id") for item in practices if isinstance(item, dict)}
    if ids != {"thermal-synthetic", "physionet-header-audit"}:
        raise ValueError(f"unexpected practice ids: {ids}")
    if contract.get("expected_default_thermal_sha256") != thermal_hash:
        raise ValueError("contract thermal golden hash is stale")
    validation = contract.get("validation")
    if not isinstance(validation, dict) or validation.get("runs_offline") is not True:
        raise ValueError("practice validation must be explicitly offline")
    review_state = contract.get("review_state")
    if not isinstance(review_state, dict):
        raise ValueError("practice implementation lacks review_state")
    if review_state.get("disciplinary_review") != "pending_human_review":
        raise ValueError("disciplinary review must remain pending")
    if review_state.get("unit_developed") is not False:
        raise ValueError("unit must remain undeveloped")

    package = load_json(PACKAGE_PATH)
    if package.get("current_phase") != "unit_01_practice_implementation_review":
        raise ValueError("pilot package phase is not synchronized")
    unit_preparation = package.get("unit_preparation")
    if not isinstance(unit_preparation, dict):
        raise ValueError("pilot package lacks unit_preparation")
    if unit_preparation.get("practice_implementation") != str(
        CONTRACT_PATH.relative_to(ROOT)
    ):
        raise ValueError(
            "pilot package does not reference the practice implementation"
        )

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("authoral unit must not exist during practice implementation")

    doc_text = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "Implementación reproducible",
        "Sin descarga en CI",
        "No es un modelo fisiológico validado",
        "Revisión disciplinar",
    ):
        if marker not in doc_text:
            raise ValueError(
                f"practice implementation document lacks marker: {marker}"
            )
    attribution = ATTRIBUTION_PATH.read_text(encoding="utf-8")
    for marker in (
        "MIT-BIH Arrhythmia Database",
        "10.13026/C2F305",
        "Open Data Commons Attribution License v1.0",
    ):
        if marker not in attribution:
            raise ValueError(f"fixture attribution lacks marker: {marker}")


def main() -> int:
    try:
        generator = load_module(
            GENERATOR_PATH, "bioinstrumentation_thermal_generator"
        )
        auditor = load_module(HEADER_AUDITOR_PATH, "wfdb_header_auditor")
        thermal_hash = validate_thermal(generator)
        validate_header(auditor)
        validate_contract(thermal_hash)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U1 practices")
    print(f"thermal golden sha256: {thermal_hash}")
    print("2 executable practices · offline CI · course remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
