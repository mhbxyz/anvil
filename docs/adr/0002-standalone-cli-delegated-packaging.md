# ADR 0002: Standalone CLI, Delegated Tool Runner

[Project README](../../README.md) · [Docs Index](../README.md) · [ADR Index](README.md)

- Status: Accepted
- Date: 2026-02-20
- Owners: Flint maintainers
- Related: [Alpha quickstart](../getting-started/quickstart-alpha.md), milestone M5 planning

## Context

Flint is a workflow CLI, not an environment/package manager. Project setup and in-environment tool execution rely on `uv`, which already owns dependency resolution, virtual environment management, and command execution.

## Decision

1. Flint remains a standalone orchestration CLI at product/UX level.
2. Flint does not become a package manager.
3. Environment and tool execution are delegated to a tool runner, with `uv` as the only official runner during alpha.
4. Flint does not add wrapper commands for dependency sync/install.

## Responsibility Boundary

- `flint` owns:
  - command workflows (`new`, `dev`, `run`, `test`, `lint`, `fmt`, `check`)
  - project conventions and defaults
  - diagnostics and actionable errors
- tool runner (`uv` in alpha) owns:
  - dependency resolution and lock/install behavior
  - virtual environment management
  - command execution inside project environment

## Consequences

- Positive:
  - clear product boundary and maintainable architecture
  - keeps Flint focused on developer experience and orchestration
- Tradeoff:
  - alpha docs must explicitly explain the split between `uv sync --extra dev` and `flint ...`

## Implementation Notes

- Alpha (now): keep `uv` as required runner and document execution model clearly.
- Flint commands assume the project environment has already been prepared with `uv sync --extra dev`.
- Internal command execution continues to use `uv run <tool>` for deterministic project-local tooling.

## See Also

- [ADR index](README.md)
- [Release checklist](../release/release-alpha-checklist.md)
