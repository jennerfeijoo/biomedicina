from __future__ import annotations

import base64
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / ".tmp" / "imagenes_avanzadas_i_u5_payload.b64"
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-05.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-05.json"
TEST = ROOT / "tests" / "test_imagenes_biomedicas_avanzadas_i_unit_05_curated.py"
WORKFLOW = ROOT / ".github" / "workflows" / "materialize-imagenes-avanzadas-i-u5.yml"
SELF = Path(__file__)
EXPECTED_SHA256 = "315493c322b6562b85be91f479f10259d5c94b4b91bd50ae0ac200d2177bcdad"

encoded = "".join(PAYLOAD.read_text(encoding="utf-8").split())
raw = zlib.decompress(base64.b64decode(encoded))
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"payload sha256 mismatch: {actual}")

obj = json.loads(raw.decode("utf-8"))
unit = obj["unit"]
test_content = obj["test"]

assert unit["subject_id"] == "imagenes-biomedicas-avanzadas-i"
assert unit["unit"] == 5
assert unit["slug"] == "registro-y-fusion"
assert len(unit["theory_sections"]) == 5
assert len(unit["glossary"]) >= 55
assert len(unit["guided_activities"][0]["problems"]) >= 20
assert len(unit["sources"]) >= 18
assert all(x["verification_status"] == "verified_directly" for x in unit["sources"])

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
TEST.write_text(test_content, encoding="utf-8")

json.loads(SOURCE.read_text(encoding="utf-8"))
assert SOURCE.read_bytes() == MIRROR.read_bytes()
assert "concepto de la unidad que debe definirse mediante entidades observables" not in text.casefold()
assert "cnr=" not in text.casefold()

for path in (PAYLOAD, SELF, WORKFLOW):
    if path.exists():
        path.unlink()

print("U5 materializada y validada; artefactos temporales retirados.")
