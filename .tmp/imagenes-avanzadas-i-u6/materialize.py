from __future__ import annotations

import base64
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / ".tmp" / "imagenes-avanzadas-i-u6"
PARTS = sorted(TMP.glob("part*.b64"))
SOURCE = ROOT / "data" / "course_redevelopment" / "imagenes-biomedicas-avanzadas-i" / "units" / "unit-06.json"
MIRROR = ROOT / "data" / "generated_units" / "imagenes-biomedicas-avanzadas-i" / "unit-06.json"
TEST = ROOT / "tests" / "test_imagenes_biomedicas_avanzadas_i_unit_06_curated.py"
WORKFLOW = ROOT / ".github" / "workflows" / "materialize-imagenes-avanzadas-i-u6.yml"
SELF = Path(__file__)

if len(PARTS) != 5:
    raise SystemExit(f"expected 5 payload parts, found {len(PARTS)}")
encoded = "".join("".join(p.read_text(encoding="utf-8").split()) for p in PARTS)
raw = gzip.decompress(base64.b64decode(encoded))
obj = json.loads(raw.decode("utf-8"))

if isinstance(obj, dict) and "unit" in obj:
    unit = obj["unit"]
    test_content = obj.get("test") or obj.get("test_content")
elif isinstance(obj, dict) and obj.get("subject_id") == "imagenes-biomedicas-avanzadas-i":
    unit = obj
    test_content = None
else:
    raise SystemExit(f"unexpected payload structure: {type(obj).__name__}, keys={list(obj)[:12] if isinstance(obj, dict) else 'n/a'}")

assert unit["subject_id"] == "imagenes-biomedicas-avanzadas-i"
assert unit["unit"] == 6
assert unit["slug"] == "control-de-calidad-cuantitativo"
assert len(unit.get("theory_sections", [])) >= 5
assert len(unit.get("glossary", [])) >= 55
assert len(unit.get("guided_activities", [])) >= 1
assert len(unit["guided_activities"][0].get("problems", [])) >= 20
assert len(unit.get("self_assessment", [])) >= 12
assert len(unit.get("biomedical_connections", [])) >= 6
assert len(unit.get("sources", [])) >= 18
assert all(s.get("verification_status") == "verified_directly" for s in unit["sources"])

text = json.dumps(unit, ensure_ascii=False, indent=2) + "\n"
low = text.casefold()
assert "concepto de la unidad que debe definirse mediante entidades observables" not in low
assert "cnr=" not in low
SOURCE.write_text(text, encoding="utf-8")
MIRROR.write_text(text, encoding="utf-8")
assert SOURCE.read_bytes() == MIRROR.read_bytes()

if test_content:
    TEST.write_text(test_content, encoding="utf-8")
elif not TEST.exists():
    raise SystemExit("payload has no regression test and no test file exists")

# Remove all temporary transfer infrastructure before committing.
for p in PARTS:
    p.unlink(missing_ok=True)
SELF.unlink(missing_ok=True)
WORKFLOW.unlink(missing_ok=True)
try:
    TMP.rmdir()
except OSError:
    pass
print("Imágenes Biomédicas Avanzadas I U6 materializada y validada.")
