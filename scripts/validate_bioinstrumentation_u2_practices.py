#!/usr/bin/env python3
"""Validate executable practice infrastructure for Bioinstrumentation U2."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATIC_PATH = ROOT / "scripts" / "generate_bioinstrumentation_u2_static_dataset.py"
DYNAMIC_PATH = ROOT / "scripts" / "generate_bioinstrumentation_u2_dynamic_dataset.py"
AUDITOR_PATH = ROOT / "scripts" / "audit_bioinstrumentation_u2_datasheets.py"
FIXTURE_PATH = (
    ROOT
    / "data"
    / "practice_fixtures"
    / "bioinstrumentacion"
    / "unit-02"
    / "component-datasheet-records.json"
)
CONTRACT_PATH = (
    ROOT
    / "data"
    / "practice_implementations"
    / "bioinstrumentacion-unit-02.json"
)
AUTH_PATH = (
    ROOT
    / "data"
    / "authoring_authorizations"
    / "bioinstrumentacion-unit-02-practices-provisional.json"
)
HANDOFF_PATH = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-02.json"
PACKAGE_PATH = (
    ROOT
    / "data"
    / "course_plan_packages"
    / "package-04-bioinstrumentation-excellence-pilot.json"
)
STATUS_PATH = ROOT / "data" / "catalog_statuses.json"
DOC_PATH = (
    ROOT
    / "docs"
    / "pilots"
    / "bioinstrumentacion"
    / "unit-02"
    / "PRACTICE_IMPLEMENTATION.md"
)
READINESS_PATH = DOC_PATH.parent / "AUTHORING_READINESS.md"
AUTHORAL_UNIT_PATH = (
    ROOT
    / "data"
    / "course_redevelopment"
    / "bioinstrumentacion"
    / "units"
    / "unit-02.json"
)
DECISION_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-disciplinary-review.json"
MANIFEST_PATH = ROOT / "data" / "review_evidence" / "bioinstrumentacion-unit-02-review-packet.json"


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


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return payload


def relative_error(observed: float, expected: float) -> float:
    if expected == 0:
        return abs(observed - expected)
    return abs(observed - expected) / abs(expected)


def validate_static(generator: ModuleType) -> str:
    noiseless = generator.StaticParameters(noise_sd=0.0)
    rows = generator.simulate(noiseless)
    models = {row["model"] for row in rows}
    if models != {"linear-local", "saturation", "dead-zone", "hysteresis"}:
        raise ValueError(f"unexpected static models: {models}")

    linear = [row for row in rows if row["model"] == "linear-local"]
    slope, intercept = generator.fit_line(linear)
    if relative_error(slope, noiseless.sensitivity_k) > 0.01:
        raise ValueError("noiseless linear slope exceeds 1 percent error")
    if relative_error(intercept, noiseless.offset_b) > 0.01:
        raise ValueError("noiseless linear offset exceeds 1 percent error")

    noisy_parameters = generator.StaticParameters()
    noisy_rows = generator.simulate(noisy_parameters)
    noisy_linear = [row for row in noisy_rows if row["model"] == "linear-local"]
    noisy_slope, noisy_intercept = generator.fit_line(noisy_linear)
    if relative_error(noisy_slope, noisy_parameters.sensitivity_k) > 0.03:
        raise ValueError("noisy linear slope exceeds 3 percent error")
    if relative_error(noisy_intercept, noisy_parameters.offset_b) > 0.03:
        raise ValueError("noisy linear offset exceeds 3 percent error")

    saturation = {
        round(float(row["x_input_unit"]), 10): float(row["y_ideal_output_unit"])
        for row in rows
        if row["model"] == "saturation"
    }

    def local_slope(center: float) -> float:
        step = noiseless.grid_step
        return (
            saturation[round(center + step, 10)]
            - saturation[round(center - step, 10)]
        ) / (2.0 * step)

    central = abs(local_slope(0.0))
    extreme = abs(local_slope(noiseless.x_max - noiseless.grid_step))
    if central == 0 or extreme / central >= 0.20:
        raise ValueError("saturation extreme sensitivity is not below 20 percent of central sensitivity")

    dead_zone = [
        float(row["y_ideal_output_unit"])
        for row in rows
        if row["model"] == "dead-zone"
        and abs(float(row["x_input_unit"])) <= noiseless.dead_zone_d + 1e-12
    ]
    expected_linear_change = 2.0 * noiseless.dead_zone_d * noiseless.sensitivity_k
    if max(dead_zone) - min(dead_zone) >= 0.10 * expected_linear_change:
        raise ValueError("dead-zone output varies too much inside the declared region")

    hysteresis = [row for row in rows if row["model"] == "hysteresis"]
    by_x: dict[float, dict[str, float]] = {}
    for row in hysteresis:
        x = round(float(row["x_input_unit"]), 10)
        by_x.setdefault(x, {})[str(row["branch"])] = float(row["y_output_unit"])
    differences = [
        values["ascending"] - values["descending"]
        for values in by_x.values()
        if set(values) == {"ascending", "descending"}
    ]
    branch_difference = sum(differences) / len(differences)
    if relative_error(branch_difference, 2.0 * noiseless.hysteresis_h) > 0.05:
        raise ValueError("hysteresis branch difference does not recover 2*h")
    residuals = generator.branch_residual_means(hysteresis)
    if residuals["ascending"] <= 0 or residuals["descending"] >= 0:
        raise ValueError("grouped line fit did not preserve opposite branch residuals")
    if abs(residuals["ascending"] - residuals["descending"]) < 1.5 * noiseless.hysteresis_h:
        raise ValueError("grouped line fit hides the hysteresis branch pattern")

    same_a = generator.csv_bytes(generator.simulate(noisy_parameters))
    same_b = generator.csv_bytes(generator.simulate(noisy_parameters))
    changed = generator.csv_bytes(
        generator.simulate(
            generator.StaticParameters(seed=noisy_parameters.seed + 1)
        )
    )
    if same_a != same_b:
        raise ValueError("static generator is not deterministic for the same seed")
    if same_a == changed:
        raise ValueError("changing the static seed must change the noisy output")

    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path, manifest_path = generator.write_outputs(Path(temp_dir), noisy_parameters)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        if manifest.get("outputs", {}).get("sha256") != digest:
            raise ValueError("static manifest hash does not match CSV bytes")
        if manifest.get("outputs", {}).get("row_count") != len(noisy_rows):
            raise ValueError("static manifest row count is incorrect")
        limitations = " ".join(manifest.get("limitations", [])).lower()
        for marker in ("people", "unique physical mechanism", "clinical", "device-performance"):
            if marker not in limitations:
                raise ValueError(f"static manifest lacks limitation marker: {marker}")
    return hashlib.sha256(same_a).hexdigest()


def validate_dynamic(generator: ModuleType) -> tuple[str, str]:
    noiseless = generator.DynamicParameters(noise_sd=0.0)
    rows = generator.simulate_first_order(noiseless)
    expected_count = int(round(noiseless.duration_s / noiseless.dt_s)) + 1
    if len(rows) != expected_count:
        raise ValueError("dynamic row count is incorrect")

    tau_estimate = generator.estimate_tau_seconds(
        rows, noiseless.step_time_s, "y_output_unit"
    )
    if relative_error(tau_estimate, noiseless.tau_s) > 0.01:
        raise ValueError("noiseless tau estimate exceeds 1 percent error")

    noisy = generator.DynamicParameters()
    noisy_rows = generator.simulate_first_order(noisy)
    noisy_tau = generator.estimate_tau_seconds(
        noisy_rows, noisy.step_time_s, "y_output_unit"
    )
    if relative_error(noisy_tau, noisy.tau_s) > 0.05:
        raise ValueError("noisy tau estimate exceeds 5 percent error")

    post = [
        float(row["y_ideal_output_unit"])
        for row in rows
        if float(row["time_s"]) >= noiseless.step_time_s
    ]
    if any(current < previous - 1e-12 for previous, current in zip(post, post[1:])):
        raise ValueError("positive first-order response is not monotonic")
    target = noiseless.offset_b + noiseless.gain_k * noiseless.step_amplitude
    if max(post) > target + 1e-12:
        raise ValueError("positive first-order response overshoots")

    fc = 1.0 / (2.0 * math.pi * noiseless.tau_s)
    magnitude = generator.normalized_magnitude(fc, noiseless.tau_s)
    if not math.isclose(magnitude, 1.0 / math.sqrt(2.0), rel_tol=0.01):
        raise ValueError("normalized magnitude at corner frequency is incorrect")

    negative_rows = generator.simulate_negative_controls(noiseless)
    pure_reasons = generator.reject_simple_first_order(
        negative_rows, noiseless.step_time_s, noiseless.dt_s, "pure-delay"
    )
    if not any("pure delay" in reason for reason in pure_reasons):
        raise ValueError("pure-delay negative control was not rejected")
    second_reasons = generator.reject_simple_first_order(
        negative_rows,
        noiseless.step_time_s,
        noiseless.dt_s,
        "underdamped-second-order",
    )
    if not any("overshoot" in reason for reason in second_reasons):
        raise ValueError("underdamped second-order control was not rejected")
    try:
        generator.require_time_axis(generator.static_only_curve(noiseless))
    except ValueError as exc:
        if "time axis" not in str(exc):
            raise
    else:
        raise ValueError("static-only control permitted tau estimation")

    first_a = generator.first_order_csv_bytes(generator.simulate_first_order(noisy))
    first_b = generator.first_order_csv_bytes(generator.simulate_first_order(noisy))
    first_changed = generator.first_order_csv_bytes(
        generator.simulate_first_order(
            generator.DynamicParameters(seed=noisy.seed + 1)
        )
    )
    if first_a != first_b:
        raise ValueError("dynamic generator is not deterministic for the same seed")
    if first_a == first_changed:
        raise ValueError("changing the dynamic seed must change the noisy output")
    negative_payload = generator.negative_csv_bytes(
        generator.simulate_negative_controls(noisy)
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        first_path, negative_path, manifest_path = generator.write_outputs(
            Path(temp_dir), noisy
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        outputs = manifest.get("outputs", {})
        if outputs.get("first_order_sha256") != hashlib.sha256(first_path.read_bytes()).hexdigest():
            raise ValueError("dynamic first-order manifest hash is incorrect")
        if outputs.get("negative_controls_sha256") != hashlib.sha256(negative_path.read_bytes()).hexdigest():
            raise ValueError("dynamic negative-control manifest hash is incorrect")
        limitations = " ".join(manifest.get("limitations", [])).lower()
        for marker in ("-3 db", "not universally equal", "synthetic", "clinical"):
            if marker not in limitations:
                raise ValueError(f"dynamic manifest lacks limitation marker: {marker}")
    return hashlib.sha256(first_a).hexdigest(), hashlib.sha256(negative_payload).hexdigest()


def validate_datasheet_audit(auditor: ModuleType) -> str:
    fixture = load_json(FIXTURE_PATH)
    report = auditor.audit_fixture(fixture)
    if report.get("status") != "pass" or report.get("errors") != []:
        raise ValueError("documentary fixture failed the baseline audit")
    if report.get("models") != {
        "thermistor": "NTCLG100E2103JB",
        "strain-gage": "CEA-06-125UNA-350",
        "photodiode": "S5821-03",
    }:
        raise ValueError("datasheet audit models are incorrect")
    counts = report.get("category_counts", {})
    if counts.get("typical") != 3 or counts.get("maximum") != 1:
        raise ValueError("typical and maximum categories were not preserved")
    if report.get("intentionally_unresolved_field_count") != 1:
        raise ValueError("lot-specific gauge factor is not the single unresolved field")

    missing_condition = copy.deepcopy(fixture)
    for component in missing_condition["components"]:
        if component["component_id"] == "photodiode":
            for field in component["fields"]:
                if field["name"] == "cutoff_frequency":
                    field["conditions"] = ""
    errors = auditor.audit_fixture(missing_condition).get("errors", [])
    if not any("cutoff_frequency lacks measurement conditions" in error for error in errors):
        raise ValueError("missing photodiode cutoff condition was not rejected")

    typical_as_guarantee = copy.deepcopy(fixture)
    for component in typical_as_guarantee["components"]:
        if component["component_id"] == "photodiode":
            for field in component["fields"]:
                if field["name"] == "photosensitivity":
                    field["guaranteed"] = True
    errors = auditor.audit_fixture(typical_as_guarantee).get("errors", [])
    if not any("converts a typical value into a guarantee" in error for error in errors):
        raise ValueError("typical-as-guarantee mutation was not rejected")

    payload_report = copy.deepcopy(report)
    payload_report["fixture"] = {
        "fixture_id": fixture.get("fixture_id"),
        "sha256": hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest(),
    }
    payload = auditor.report_bytes(payload_report)
    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "datasheet-audit.json"
        written = auditor.write_report(FIXTURE_PATH, output)
        if written.get("status") != "pass":
            raise ValueError("written datasheet audit does not pass")
        if output.read_bytes() != payload:
            raise ValueError("datasheet audit output is not deterministic")
    return hashlib.sha256(payload).hexdigest()


def validate_contract(static_hash: str, dynamic_hash: str, negative_hash: str, audit_hash: str) -> None:
    contract = load_json(CONTRACT_PATH)
    expected_identity = {
        "implementation_id": "bioinstrumentacion-unit-02-practices",
        "subject_id": "bioinstrumentacion",
        "unit_number": 2,
        "status": "implemented_internal_review",
        "course_editorial_state": "pending",
        "external_professional_review_status": "pending_human_review",
        "full_theory_drafting_authorized": False,
        "authoral_unit_present": False,
        "public_release_authorized": False,
    }
    for key, wanted in expected_identity.items():
        if contract.get(key) != wanted:
            raise ValueError(f"practice contract {key} is incorrect")
    if contract.get("provisional_internal_authorization") != str(AUTH_PATH.relative_to(ROOT)):
        raise ValueError("practice contract does not reference the provisional authorization")

    practices = contract.get("practices")
    if not isinstance(practices, list) or len(practices) != 3:
        raise ValueError("practice contract must contain exactly three practices")
    if {item.get("id") for item in practices if isinstance(item, dict)} != {"U2-P1", "U2-P2", "U2-P3"}:
        raise ValueError("practice ids are incorrect")
    for practice in practices:
        if not isinstance(practice, dict):
            raise ValueError("practice entries must be objects")
        if practice.get("network_required") is not False:
            raise ValueError(f"{practice.get('id')} requires network access")
        if not isinstance(practice.get("acceptance_tests"), list) or len(practice["acceptance_tests"]) < 7:
            raise ValueError(f"{practice.get('id')} lacks acceptance tests")
        limitations = " ".join(practice.get("limitations", [])).lower()
        if "clinical" not in limitations:
            raise ValueError(f"{practice.get('id')} lacks a clinical-scope limitation")

    hashes = contract.get("golden_hashes", {})
    expected_hashes = {
        "static_characteristics_csv_sha256": static_hash,
        "first_order_response_csv_sha256": dynamic_hash,
        "dynamic_negative_controls_csv_sha256": negative_hash,
        "datasheet_audit_report_sha256": audit_hash,
    }
    if hashes != expected_hashes:
        raise ValueError(f"practice golden hashes are stale: {hashes!r}")
    validation = contract.get("validation", {})
    if validation.get("runs_offline") is not True:
        raise ValueError("practice validation must run offline")
    if validation.get("uses_temporary_directories") is not True:
        raise ValueError("practice validation must use temporary directories")
    if validation.get("generated_outputs_tracked") is not False:
        raise ValueError("generated practice outputs must remain untracked")
    if validation.get("negative_controls_required") is not True:
        raise ValueError("negative controls must remain required")


def validate_repository_state() -> None:
    authorization = load_json(AUTH_PATH)
    if authorization.get("status") != "authorized_for_controlled_practice_implementation_provisionally":
        raise ValueError("provisional practice authorization is missing")
    if authorization.get("review_characterization", {}).get("human_disciplinary_review_completed") is not False:
        raise ValueError("provisional authorization fabricates human review")

    handoff = load_json(HANDOFF_PATH)
    if handoff.get("status") != "ready_pending_external_review":
        raise ValueError("external handoff no longer remains pending")
    if handoff.get("practice_implementation_authorized") is not False:
        raise ValueError("external handoff fabricates professional practice authorization")
    if handoff.get("full_theory_drafting_authorized") is not False:
        raise ValueError("external handoff authorizes full theory")

    package = load_json(PACKAGE_PATH)
    if package.get("schema_version") != "2.0":
        raise ValueError("central package schema is not synchronized")
    if package.get("unit_02_practice_implementation_workstream") != "unit_02_practices_implemented_internal_review":
        raise ValueError("Unit 2 practice implementation workstream is not synchronized")
    preparation = package.get("unit_02_preparation", {})
    if preparation.get("practice_implementation_present") is not True:
        raise ValueError("central package does not record the practice implementation")
    if preparation.get("authoral_unit_present") is not False:
        raise ValueError("central package claims an authoral Unit 2 file")
    section = package.get("unit_02_practice_implementation")
    if not isinstance(section, dict):
        raise ValueError("central package lacks Unit 2 practice implementation")
    expected_section = {
        "status": "implemented_internal_review",
        "contract": str(CONTRACT_PATH.relative_to(ROOT)),
        "document": str(DOC_PATH.relative_to(ROOT)),
        "validation": "scripts/validate_bioinstrumentation_u2_practices.py",
        "practice_ids": ["U2-P1", "U2-P2", "U2-P3"],
        "network_required_in_ci": False,
        "generated_outputs_tracked": False,
        "data_scope": "synthetic_or_compact_documentary_metadata_only",
        "external_professional_review_status": "pending_human_review",
        "professional_endorsement_present": False,
        "full_theory_drafting_authorized": False,
        "authoral_unit_present": False,
        "public_release_authorized": False,
        "unit_developed": False,
        "course_state": "pending",
        "editorial_effect": "internal_practice_implementation_only",
    }
    if section != expected_section:
        raise ValueError("central package Unit 2 practice section is incorrect")

    statuses = load_json(STATUS_PATH)
    if "bioinstrumentacion" not in set(statuses.get("pending", [])):
        raise ValueError("Bioinstrumentation must remain pending")
    if "bioinstrumentacion" in set(statuses.get("developed", [])):
        raise ValueError("Bioinstrumentation was promoted prematurely")
    if AUTHORAL_UNIT_PATH.exists():
        raise ValueError("Unit 2 authoral file exists before theory authorization")
    if DECISION_PATH.exists() or MANIFEST_PATH.exists():
        raise ValueError("practice implementation fabricated external review evidence")

    fixture = load_json(FIXTURE_PATH)
    if fixture.get("human_data") is not False or fixture.get("clinical_device_data") is not False:
        raise ValueError("documentary fixture exceeds the authorized data scope")

    document = DOC_PATH.read_text(encoding="utf-8")
    for marker in (
        "Implementación reproducible",
        "U2-P1",
        "U2-P2",
        "U2-P3",
        "pure-delay",
        "static-only",
        "No reproduce hojas de datos completas",
        "issue `#161`",
    ):
        if marker not in document:
            raise ValueError(f"practice implementation document lacks marker: {marker}")
    readiness = READINESS_PATH.read_text(encoding="utf-8")
    for marker in (
        "u2_practices_implemented: true",
        "practice_implementation_status: implemented_internal_review",
        "external_professional_practice_authorization: false",
        "full_theory_drafting_authorized: false",
    ):
        if marker not in readiness:
            raise ValueError(f"AUTHORING_READINESS lacks marker: {marker}")


def main() -> int:
    try:
        static_generator = load_module(STATIC_PATH, "bioinstrumentation_u2_static_generator")
        dynamic_generator = load_module(DYNAMIC_PATH, "bioinstrumentation_u2_dynamic_generator")
        datasheet_auditor = load_module(AUDITOR_PATH, "bioinstrumentation_u2_datasheet_auditor")
        static_hash = validate_static(static_generator)
        dynamic_hash, negative_hash = validate_dynamic(dynamic_generator)
        audit_hash = validate_datasheet_audit(datasheet_auditor)
        validate_contract(static_hash, dynamic_hash, negative_hash, audit_hash)
        validate_repository_state()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    print("OK Bioinstrumentation U2 practices")
    print(f"static golden sha256: {static_hash}")
    print(f"dynamic golden sha256: {dynamic_hash}")
    print(f"negative-control sha256: {negative_hash}")
    print(f"datasheet-audit sha256: {audit_hash}")
    print("3 executable practices · offline CI · external review pending · theory blocked · course pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
