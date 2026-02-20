#!/usr/bin/env bash
set -euo pipefail

BASELINE_PATH="benchmarks/baseline.alpha.json"
if [ "${GITHUB_ACTIONS:-}" = "true" ] && [ -f "benchmarks/baseline.github-hosted.alpha.json" ]; then
  BASELINE_PATH="benchmarks/baseline.github-hosted.alpha.json"
fi

FAIL_THRESHOLD="${PYQCK_BENCH_FAIL_THRESHOLD:-30}"

uv run python scripts/benchmark_runtime.py --output benchmarks/current.alpha.json
uv run python scripts/benchmark_compare.py "${BASELINE_PATH}" benchmarks/current.alpha.json "${FAIL_THRESHOLD}"
