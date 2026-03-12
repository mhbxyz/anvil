import typer

from flint.commands._common import (
    build_adapters_or_exit,
    ensure_tool_available_or_exit,
    resolve_profile_capabilities_or_exit,
    usage_error,
)
from flint.devloop import run_dev_loop
from flint.scaffold import DevMode
from flint.tooling import ToolKey


def dev_command() -> None:
    """Run the local development loop."""

    adapters = build_adapters_or_exit()
    capabilities = resolve_profile_capabilities_or_exit(adapters.config)
    if capabilities.dev_mode == DevMode.UNSUPPORTED:
        usage_error(
            f"`flint dev` is not supported for profile `{adapters.config.project.profile}`.",
            "Use `flint test` and `flint check` directly for this profile.",
        )

    if capabilities.dev_mode == DevMode.SERVER_WITH_CHECKS:
        ensure_tool_available_or_exit(adapters, ToolKey.RUNNING)
    ensure_tool_available_or_exit(adapters, ToolKey.LINTING)
    ensure_tool_available_or_exit(adapters, ToolKey.TYPING)
    ensure_tool_available_or_exit(adapters, ToolKey.TESTING)
    run_dev_loop(adapters, mode=capabilities.dev_mode)
