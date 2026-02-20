#!/usr/bin/env bash
set -euo pipefail

uv run pytest tests/e2e
