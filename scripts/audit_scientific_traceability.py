#!/usr/bin/env python3
"""Expose canonical claim gaps without confusing provisional publication with approval.

Use --strict for scientific completion. Technical CI records the same findings;
its success never authorizes a course to become complete.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from validate_scientific_traceability import (
    ROOT, DEFAULT_DIRECTORY, CANONICAL_COURSE_DIRECTORY,
    validate_repository_registry,
)

def registry_paths(directory: Path) -> list[Path]:
    paths = {p.stem: p for p in directory.glob("*.json") if not p.name.startswith("_")}
    if directory.resolve() == DEFAULT_DIRECTORY.resolve():
        paths.update({p.parent.name: p for p in CANONICAL_COURSE_DIRECTORY.glob("*/claims.json")})
    return [paths[key] for key in sorted(paths)]


def load_registry(path: Path) -> Any:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if path.name == "claims.json" and isinstance(payload, dict):
        payload = dict(payload)
        payload["subject_id"] = payload.get("course_id")
        # The corpus fingerprint identifies the files actually checked, without
        # inventing a historical commit or overwriting the author's review record.
        digest = hashlib.sha256()
        for source in sorted(path.parent.rglob("*.json")):
            digest.update(source.relative_to(path.parent).as_posix().encode())
            digest.update(source.read_bytes())
        payload["content_commit"] = payload.get("content_commit") or "sha256:" + digest.hexdigest()
    return payload


def audit() -> dict:
    rows = []
    for path in registry_paths(DEFAULT_DIRECTORY):
        payload = load_registry(path)
        errors = validate_repository_registry(payload, str(path.relative_to(ROOT)))
        rows.append({"course_id": payload.get("subject_id"),
                     "claims": len(payload.get("claims", [])), "errors": errors})
    return {"registries": len(rows), "claims": sum(r["claims"] for r in rows),
            "errors": sum(len(r["errors"]) for r in rows), "courses": rows,
            "scope": "Registered claims only; passing does not establish full corpus coverage or scientific correctness."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(args.strict and result["errors"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
