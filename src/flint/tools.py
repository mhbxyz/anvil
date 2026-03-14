from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
from typing import TextIO

from flint.config import ProjectSettings
from flint.errors import tooling_error


@dataclass(slots=True)
class ToolResult:
    name: str
    returncode: int


def build_run_command(settings: ProjectSettings, reload_enabled: bool) -> list[str]:
    command = ["uv", "run", "uvicorn", settings.app_module]
    if reload_enabled:
        command.append("--reload")
    return command


def run_foreground(command: list[str], cwd: Path) -> int:
    try:
        completed = subprocess.run(command, cwd=cwd)
    except FileNotFoundError as exc:
        raise tooling_error(
            f"Could not execute `{command[0]}`.",
            "Install the required tooling and ensure it is available in PATH.",
        ) from exc
    return 0 if completed.returncode == 0 else 1


def spawn_background(command: list[str], cwd: Path) -> subprocess.Popen[str]:
    try:
        return subprocess.Popen(command, cwd=cwd)
    except FileNotFoundError as exc:
        raise tooling_error(
            f"Could not execute `{command[0]}`.",
            "Install the required tooling and ensure it is available in PATH.",
        ) from exc


def run_check_pipeline(settings: ProjectSettings, stdout: TextIO | None = None) -> int:
    stream = stdout or sys.stdout
    commands: list[tuple[str, list[str]]] = [
        ("lint", ["uv", "run", "ruff", "check", "."]),
        ("test", ["uv", "run", "pytest"]),
    ]
    if settings.typecheck:
        commands.append(("typecheck", ["uv", "run", "pyright"]))

    for step_name, command in commands:
        print(f"==> {step_name}", file=stream)
        returncode = run_step(command, settings.root)
        if returncode != 0:
            print(f"FAILED {step_name}", file=stream)
            return 1
        print(f"OK {step_name}", file=stream)
    return 0


def run_step(command: list[str], cwd: Path) -> int:
    try:
        completed = subprocess.run(command, cwd=cwd)
    except FileNotFoundError as exc:
        raise tooling_error(
            f"Could not execute `{command[0]}`.",
            "Install the required tooling and ensure it is available in PATH.",
        ) from exc
    return completed.returncode
