#!/usr/bin/env python3
"""Build a deterministic manifest for the Bioinstrumentation U1 review packet."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HANDOFF = ROOT / "data" / "review_handoffs" / "bioinstrumentacion-unit-01.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


class PacketError(ValueError):
    """Raised when the review packet contract is invalid."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PacketError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PacketError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PacketError(f"{path} must contain an object")
    return payload


def build_manifest(handoff_path: Path, reviewed_commit: str) -> dict[str, Any]:
    if not HEX40.fullmatch(reviewed_commit):
        raise PacketError("reviewed_commit must be a lowercase 40-character SHA")
    handoff = load_json(handoff_path)
    artifacts = handoff.get("required_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise PacketError("handoff required_artifacts must be a non-empty list")
    if len(set(artifacts)) != len(artifacts):
        raise PacketError("handoff required_artifacts contains duplicates")

    entries: list[dict[str, Any]] = []
    for relative in artifacts:
        if not isinstance(relative, str) or not relative.strip():
            raise PacketError("artifact paths must be non-empty strings")
        path = ROOT / relative
        try:
            data = path.read_bytes()
        except FileNotFoundError as exc:
            raise PacketError(f"required artifact is missing: {relative}") from exc
        entries.append(
            {
                "path": relative,
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    canonical = json.dumps(entries, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    packet_digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {
        "schema_version": "1.0",
        "manifest_type": "disciplinary_review_packet",
        "handoff_id": handoff.get("handoff_id"),
        "reviewed_commit": reviewed_commit,
        "artifact_count": len(entries),
        "artifacts": entries,
        "packet_digest_sha256": packet_digest,
        "deterministic": True,
        "contains_human_evidence": False,
        "interpretation": "This manifest freezes packet content for review; it is not a review decision.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, default=DEFAULT_HANDOFF)
    parser.add_argument("--reviewed-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        manifest = build_manifest(args.handoff, args.reviewed_commit)
    except PacketError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    rendered = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
