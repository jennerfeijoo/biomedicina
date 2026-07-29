#!/usr/bin/env python3
"""Deterministic assessment routing for Bioinstrumentation unit 1."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPLEMENTATION = ROOT / "data" / "assessment_implementations" / "bioinstrumentacion-unit-01.json"


class AssessmentError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssessmentError(f"{path} must contain an object")
    return data
