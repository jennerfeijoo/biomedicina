#!/usr/bin/env python3
"""Parse and audit a local WFDB header without downloading signal data."""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SignalSpecification:
    file_name: str
    format_token: str
    gain_token: str
    adc_resolution_bits: int
    adc_zero: int
    initial_value: int
    checksum: int
    block_size: int
    description: str


@dataclass(frozen=True)
class HeaderMetadata:
    record_name: str
    signal_count: int
    sampling_frequency_hz: float
    sample_count: int
    signals: tuple[SignalSpecification, ...]
    comments: tuple[str, ...]


def _parse_int(token: str, label: str) -> int:
    try:
        return int(token)
    except ValueError as exc:
        raise ValueError(f"{label} must be an integer, got {token!r}") from exc


def _parse_float(token: str, label: str) -> float:
    normalized = token.split("/", 1)[0]
    try:
        value = float(normalized)
    except ValueError as exc:
        raise ValueError(f"{label} must be numeric, got {token!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"{label} must be finite")
    return value


def parse_wfdb_header(text: str) -> HeaderMetadata:
    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]
    comments = tuple(line[1:].strip() for line in raw_lines if line.startswith("#"))
    data_lines = [line for line in raw_lines if not line.startswith("#")]
    if not data_lines:
        raise ValueError("header contains no record line")

    record_tokens = data_lines[0].split()
    if len(record_tokens) < 4:
        raise ValueError(
            "record line requires record, signal count, sampling frequency, and sample count"
        )
    record_name = record_tokens[0]
    signal_count = _parse_int(record_tokens[1], "signal_count")
    sampling_frequency_hz = _parse_float(record_tokens[2], "sampling_frequency_hz")
    sample_count = _parse_int(record_tokens[3], "sample_count")
    if signal_count <= 0:
        raise ValueError("signal_count must be > 0")
    if sampling_frequency_hz <= 0:
        raise ValueError("sampling_frequency_hz must be > 0")
    if sample_count <= 0:
        raise ValueError("sample_count must be > 0")
    if len(data_lines) != signal_count + 1:
        raise ValueError(
            f"expected {signal_count} signal lines, found {len(data_lines) - 1}"
        )

    signals: list[SignalSpecification] = []
    for index, line in enumerate(data_lines[1:], start=1):
        tokens = line.split()
        if len(tokens) < 9:
            raise ValueError(f"signal line {index} requires at least 9 fields")
        signals.append(
            SignalSpecification(
                file_name=tokens[0],
                format_token=tokens[1],
                gain_token=tokens[2],
                adc_resolution_bits=_parse_int(
                    tokens[3], f"signal {index} adc_resolution_bits"
                ),
                adc_zero=_parse_int(tokens[4], f"signal {index} adc_zero"),
                initial_value=_parse_int(tokens[5], f"signal {index} initial_value"),
                checksum=_parse_int(tokens[6], f"signal {index} checksum"),
                block_size=_parse_int(tokens[7], f"signal {index} block_size"),
                description=" ".join(tokens[8:]),
            )
        )

    return HeaderMetadata(
        record_name=record_name,
        signal_count=signal_count,
        sampling_frequency_hz=sampling_frequency_hz,
        sample_count=sample_count,
        signals=tuple(signals),
        comments=comments,
    )


def audit_record_100(metadata: HeaderMetadata) -> list[str]:
    errors: list[str] = []
    if metadata.record_name != "100":
        errors.append(f"record_name expected '100', got {metadata.record_name!r}")
    if metadata.signal_count != 2:
        errors.append(f"signal_count expected 2, got {metadata.signal_count}")
    if metadata.sampling_frequency_hz != 360:
        errors.append(
            "sampling_frequency_hz expected 360, "
            f"got {metadata.sampling_frequency_hz}"
        )
    if metadata.sample_count != 650000:
        errors.append(f"sample_count expected 650000, got {metadata.sample_count}")
    labels = [signal.description for signal in metadata.signals]
    if labels != ["MLII", "V5"]:
        errors.append(f"channel labels expected ['MLII', 'V5'], got {labels!r}")
    formats = [signal.format_token for signal in metadata.signals]
    if formats != ["212", "212"]:
        errors.append(f"format tokens expected ['212', '212'], got {formats!r}")
    files = [signal.file_name for signal in metadata.signals]
    if files != ["100.dat", "100.dat"]:
        errors.append(f"signal files expected ['100.dat', '100.dat'], got {files!r}")
    return errors


def metadata_to_dict(metadata: HeaderMetadata) -> dict[str, object]:
    return {
        "record_name": metadata.record_name,
        "signal_count": metadata.signal_count,
        "sampling_frequency_hz": metadata.sampling_frequency_hz,
        "sample_count": metadata.sample_count,
        "signals": [asdict(signal) for signal in metadata.signals],
        "comments": list(metadata.comments),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("header", type=Path)
    parser.add_argument("--expect-record-100", action="store_true")
    parser.add_argument("--json-output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        metadata = parse_wfdb_header(args.header.read_text(encoding="utf-8"))
        errors = audit_record_100(metadata) if args.expect_record_100 else []
        if errors:
            raise ValueError("; ".join(errors))
        payload = json.dumps(metadata_to_dict(metadata), indent=2, sort_keys=True) + "\n"
        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            args.json_output.write_text(payload, encoding="utf-8")
        print(payload, end="")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
