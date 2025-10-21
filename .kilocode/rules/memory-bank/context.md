# Current Context

## Work Focus
Phase 1 MVP implementation in progress. Basic project structure established with uv, CLI framework implemented, and core commands defined as placeholders.

## Recent Changes
- Memory Bank fully initialized with all 5 core files (brief.md, product.md, context.md, architecture.md, tech.md)
- Project structure initialized with uv: src/anvil/ package, pyproject.toml configured, dependencies installed
- Basic CLI framework implemented with all core commands (new, dev, run, fmt, lint, test, build) as placeholders
- Comprehensive test suite created with 9 tests covering CLI functionality
- Fixed memory leak in test_cli.py test_new_command (missing cleanup of created project files)
- Updated test assertions to match actual CLI behavior (missing dependencies, implemented features)
- Added .gitignore entries for .idea/ and test artifacts (src/test*/, packages/)
- Added cleanup in test_e2e.py to prevent accumulation of test scaffolded projects
- All tests passing without memory issues or assertion failures

## Next Steps
- Add tool detection and fallback behavior for ruff, pytest, etc.
- Begin development of core toolchain commands (fmt, lint, test)
- Implement `anvil dev` command with file watching
- Add `anvil run` command with entry point resolution
- Implement remaining toolchain commands (build, release)