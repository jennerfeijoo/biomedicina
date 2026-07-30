#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    v_min, v_max, bits = -1.0, 1.0, 10
    levels = 2**bits
    lsb = (v_max - v_min) / levels
    inputs = [-1.25, -1.0, -0.503, -0.001, 0.0, 0.317, 0.999, 1.0, 1.23]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["input_v", "clipped_v", "code", "reconstructed_v", "quantization_error_v", "saturated", "lsb_v"])
        for value in inputs:
            clipped = min(max(value, v_min), v_max)
            saturated = value < v_min or value > v_max
            code = min(levels - 1, max(0, int((clipped - v_min) / lsb)))
            reconstructed = v_min + (code + 0.5) * lsb
            writer.writerow([
                f"{value:.6f}",
                f"{clipped:.6f}",
                code,
                f"{reconstructed:.9f}",
                f"{reconstructed - clipped:.9f}",
                str(saturated).lower(),
                f"{lsb:.9f}",
            ])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
