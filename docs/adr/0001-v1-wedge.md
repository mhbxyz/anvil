# ADR 0001: Flint v1 Wedge

- Status: Accepted
- Date: 2026-03-14

## Decision

Flint v1 is an opinionated dev-loop CLI for existing Python ASGI projects.

The first shipped value is:

- `flint run` for convention-based app startup
- `flint dev` for server plus watch-driven checks
- `flint check` for deterministic local validation

## Non-Goals

- `flint new` or any project scaffolding
- plugin APIs
- framework parity beyond ASGI conventions
- environment management beyond delegating to `uv`
- large config schemas

## Rationale

The previous project attempted to solve scaffolding, workflows, and framework abstraction at the same time. This reset narrows Flint to one measurable promise: a coherent local loop for existing ASGI repos.
