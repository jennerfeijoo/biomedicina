from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/course_redevelopment/biomecanica-medios-continuos/units/unit-06.json"
MIRROR = ROOT / "data/generated_units/biomecanica-medios-continuos/unit-06.json"


def update(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in data["sources"]}

    # V&V 10 and VVUQ 10.2 are distinct standards. The portfolio auditor
    # correctly treats equal fallback URLs as duplicate bibliographic identities,
    # so give V&V 10 its verified ISBN and VVUQ 10.2 its product-specific ASME URL.
    by_id["asme-vv10"]["isbn"] = "9780791873168"
    by_id["asme-vvuq10-2"]["url"] = (
        "https://www.asme.org/codes-standards/find-codes-standards/"
        "the-role-of-uncertainty-quantification-in-verification-and-validation-"
        "of-computational-solid-mechanics-models"
    )

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


update(SOURCE)
update(MIRROR)
assert SOURCE.read_bytes() == MIRROR.read_bytes(), "source and generated mirror diverged"

unit = json.loads(SOURCE.read_text(encoding="utf-8"))
sources = {item["id"]: item for item in unit["sources"]}
assert sources["asme-vv10"]["isbn"] == "9780791873168"
assert "the-role-of-uncertainty-quantification" in sources["asme-vvuq10-2"]["url"]
