# Binary Distribution Strategy (Issue #23)

[Project README](../../README.md) · [Docs Index](../README.md) · [Release and Feedback](README.md)

This document captures the option tradeoffs, prototype result, and rollout recommendation for standalone binary distribution.

## Evaluation Summary

| Option | Standalone without Python on target | Cross-platform practicality (alpha) | CI complexity | Notes |
| --- | --- | --- | --- | --- |
| PyInstaller | yes | high (Linux/macOS feasible now) | medium | Best balance for alpha; larger artifacts |
| Nuitka | yes | medium | high | Heavier toolchain and longer builds |
| PEX | no | high | low-medium | Great packaging, but requires Python runtime |
| shiv | no | high | low-medium | Similar to PEX; zipapp model |

## Prototype (Linux)

Prototype path: **PyInstaller one-file binary**.

Build command used:

```bash
uv run --with pyinstaller pyinstaller --onefile --name flint-linux --specpath /tmp src/flint/__main__.py --paths src
```

Measured on local Linux environment:

- Build time (clean): about `11.44s`
- Artifact: `dist/flint-linux`
- Artifact size: about `16M`
- Startup (`--help`) average across 5 runs: about `225ms`

Smoke flow executed successfully:

```bash
FLINT_BIN="$PWD/dist/flint-linux"

"$FLINT_BIN" --help
"$FLINT_BIN" new smoke-api --profile api --template fastapi
cd smoke-api
uv sync --extra dev
"$FLINT_BIN" test
```

Observed outcome:

- `new` created scaffold successfully.
- `uv sync --extra dev` prepared the project environment successfully.
- `test` completed with `OK [test]`.

## Recommendation

- **Go**: publish Linux binary artifacts as experimental GitHub Release assets.
- **Conditional go**: add macOS binary once smoke checks are green in CI.
- **No-go (for alpha)**: replacing PyPI distribution; keep `pip`/`pipx` as primary path.

## Rollout Proposal

1. Add and maintain dedicated workflow `.github/workflows/binary-experimental.yml` (separate from PyPI publish) to build Linux binary assets.
2. Upload binary artifacts to GitHub Releases with `experimental` label.
3. Keep existing TestPyPI/PyPI verification workflow as release gate of record.
4. Re-evaluate Windows support after one milestone of Linux/macOS signal.

## Risks and Mitigations

- Platform-specific breakage risk -> enforce per-platform smoke checks (`--help`, `new`, `uv sync --extra dev`, `test`).
- Artifact size increase -> publish binaries as optional assets, not default install path.
- Support burden increase -> document alpha support scope clearly in install docs.

## See Also

- [ADR 0003](../adr/0003-binary-distribution-strategy.md)
- [Releasing Flint](releasing.md)
- [PyPI trusted publishing](pypi-publishing.md)
