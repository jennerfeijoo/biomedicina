#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def classify(records: list[tuple[int, float, str]]) -> list[tuple[int, float, str, str]]:
    seen: set[tuple[int, str]] = set()
    last_sequence: dict[str, int] = {}
    output: list[tuple[int, float, str, str]] = []
    for sequence, timestamp, channel in records:
        key = (sequence, channel)
        status = "ok"
        if key in seen:
            status = "duplicate"
        elif channel in last_sequence and sequence < last_sequence[channel]:
            status = "reordered"
        elif channel in last_sequence and sequence > last_sequence[channel] + 1:
            status = f"gap:{sequence - last_sequence[channel] - 1}"
        seen.add(key)
        last_sequence[channel] = max(sequence, last_sequence.get(channel, sequence))
        output.append((sequence, timestamp, channel, status))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records = [
        (0, 0.000, "A"), (0, 0.000, "B"),
        (1, 0.010, "A"), (1, 0.010, "B"),
        (3, 0.030, "A"), (2, 0.020, "B"),
        (3, 0.030, "A"), (4, 0.040, "A"),
        (4, 0.040, "B"), (3, 0.030, "B"),
    ]
    classified = classify(records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sequence", "timestamp_s", "channel", "status"])
        for sequence, timestamp, channel, status in classified:
            writer.writerow([sequence, f"{timestamp:.6f}", channel, status])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
