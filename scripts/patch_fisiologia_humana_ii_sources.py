#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_unique(items: list[dict], additions: list[dict]) -> None:
    urls = {str(item.get("url", "")) for item in items}
    for item in additions:
        if item["url"] not in urls:
            items.append(item)
            urls.add(item["url"])


def main() -> int:
    course_path = ROOT / "data" / "generated_courses" / "fisiologia-humana-ii.json"
    course = load(course_path)
    append_unique(course["core_resources"], [
        {
            "title": "Physical activity",
            "organization": "World Health Organization",
            "url": "https://www.who.int/news-room/fact-sheets/detail/physical-activity",
            "type": "recurso oficial"
        }
    ])
    save(course_path, course)

    unit4_path = ROOT / "data" / "generated_units" / "fisiologia-humana-ii" / "unit-04.json"
    unit4 = load(unit4_path)
    append_unique(unit4["sources"], [
        {
            "title": "Endocrine Library",
            "organization": "Endocrine Society",
            "url": "https://www.endocrine.org/patient-engagement/endocrine-library",
            "type": "recurso profesional"
        },
        {
            "title": "The Endocrine System",
            "organization": "OpenStax",
            "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/17-introduction",
            "type": "recurso abierto"
        }
    ])
    save(unit4_path, unit4)

    unit5_path = ROOT / "data" / "generated_units" / "fisiologia-humana-ii" / "unit-05.json"
    unit5 = load(unit5_path)
    append_unique(unit5["sources"], [
        {
            "title": "Maternal health",
            "organization": "World Health Organization",
            "url": "https://www.who.int/health-topics/maternal-health",
            "type": "recurso oficial"
        },
        {
            "title": "Pregnancy",
            "organization": "NICHD",
            "url": "https://www.nichd.nih.gov/health/topics/pregnancy",
            "type": "recurso oficial"
        }
    ])
    save(unit5_path, unit5)

    print("Bibliografía de Fisiología Humana II diversificada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
