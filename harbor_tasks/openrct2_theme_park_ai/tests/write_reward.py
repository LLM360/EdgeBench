#!/usr/bin/env python3
"""Write an EdgeBench TOTAL_SCORE directly as a Harbor reward."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


TOTAL_SCORE_RE = re.compile(
    r"^TOTAL_SCORE\s+([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)\s*$",
    re.MULTILINE,
)


def extract_total_score(output: str) -> float | None:
    matches = TOTAL_SCORE_RE.findall(output)
    if not matches:
        return None
    try:
        score = float(matches[-1])
    except ValueError:
        return None
    return score if math.isfinite(score) else None


def reward_from_result(eval_status: int, raw_score: float | None) -> float:
    if eval_status != 0 or raw_score is None:
        return 0.0
    return raw_score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_path", type=Path)
    parser.add_argument("--eval-status", type=int, required=True)
    args = parser.parse_args()

    output = args.log_path.read_text(errors="replace") if args.log_path.exists() else ""
    raw_score = extract_total_score(output)
    reward = reward_from_result(args.eval_status, raw_score)

    Path("/logs/verifier/reward.json").write_text(
        json.dumps({"reward": reward}) + "\n"
    )
    print(f"EDGE_BENCH_RAW_SCORE={raw_score!r}")
    print(f"HARBOR_REWARD={reward:.12g}")


if __name__ == "__main__":
    main()
