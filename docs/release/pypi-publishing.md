# PyPI Publishing

[Project README](../../README.md) · [Docs Index](../README.md) · [Publishing](README.md)

This guide documents the only supported publishing flow for `flint-dev`: GitHub OIDC trusted publishing to TestPyPI and PyPI via [publish.yml](../../.github/workflows/publish.yml).

## Workflows

- Build validation: `.github/workflows/ci.yml`
  - runs on PR and `main`
  - builds wheel/sdist via `uv build`
  - smoke-installs built wheel and runs `flint --help`
- Publish pipeline: `.github/workflows/publish.yml`
  - runs on version tags (`v*`)
  - publishes to TestPyPI
  - verifies install from TestPyPI via `pip`
  - verifies install from TestPyPI via `pipx`
  - runs smoke flow: `flint --help`, `flint new ...`, `uv sync --extra dev`, `flint test`
  - publishes to PyPI

## One-time setup on TestPyPI and PyPI

Configure **Trusted Publisher** on both indexes with:

- Owner: `mhbxyz`
- Repository: `Flint`
- Workflow: `publish.yml`
- Environment: `testpypi` (for TestPyPI) and `pypi` (for PyPI)

No API token is required once trusted publishing is configured.

## Direct tag trigger (fallback)

Publish can also be triggered directly by pushing a release tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Expected sequence:

1. build artifacts
2. publish TestPyPI
3. install smoke from TestPyPI
4. publish PyPI

## Troubleshooting

- If TestPyPI install verification fails intermittently, rerun once after index propagation.
- If publish fails with OIDC/trust errors, confirm trusted publisher binding exactly matches owner/repo/workflow.
- If version already exists, bump version and create a new tag.

## See Also

- [Publishing index](README.md)
