from __future__ import annotations

from pathlib import Path

from flint.scaffold.cli_template import CLITemplateContext, build_cli_template
from flint.scaffold.fastapi import FastAPITemplateContext, build_fastapi_template
from flint.scaffold.lib_template import LibTemplateContext, build_lib_template
from flint.scaffold.registry import DevMode, ProfileCapabilities, RunMode, ScaffoldRegistry


def build_default_scaffold_registry() -> ScaffoldRegistry:
    registry = ScaffoldRegistry()
    registry.register(
        profile="api",
        template="fastapi",
        generator=_build_api_fastapi,
        capabilities=ProfileCapabilities(
            run_mode=RunMode.SERVER,
            dev_mode=DevMode.SERVER_WITH_CHECKS,
        ),
        default=True,
    )
    registry.register(
        profile="lib",
        template="baseline-lib",
        generator=_build_lib_baseline,
        capabilities=ProfileCapabilities(
            run_mode=RunMode.UNSUPPORTED,
            dev_mode=DevMode.CHECKS_ONLY,
        ),
        default=True,
    )
    registry.register(
        profile="cli",
        template="baseline-cli",
        generator=_build_cli_baseline,
        capabilities=ProfileCapabilities(
            run_mode=RunMode.CLI,
            dev_mode=DevMode.CHECKS_ONLY,
        ),
        default=True,
    )

    registry.reserve_profile("web")
    registry.reserve_profile("game")
    return registry


def _build_api_fastapi(project_name: str) -> dict[Path, str]:
    context = FastAPITemplateContext.from_project_name(project_name)
    return build_fastapi_template(context)


def _build_lib_baseline(project_name: str) -> dict[Path, str]:
    context = LibTemplateContext.from_project_name(project_name)
    return build_lib_template(context)


def _build_cli_baseline(project_name: str) -> dict[Path, str]:
    context = CLITemplateContext.from_project_name(project_name)
    return build_cli_template(context)
