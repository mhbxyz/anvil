from pathlib import Path
from unittest.mock import patch

from flint.config import ProjectSettings
from flint.tools import build_run_command, run_check_pipeline


def make_settings(tmp_path: Path, typecheck: bool = False) -> ProjectSettings:
    return ProjectSettings(
        root=tmp_path,
        app_module="demo.main:app",
        watch_paths=[tmp_path / "src"],
        typecheck=typecheck,
    )


def test_build_run_command_uses_uvicorn_reload(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)

    assert build_run_command(settings, reload_enabled=True) == [
        "uv",
        "run",
        "uvicorn",
        "demo.main:app",
        "--reload",
    ]


def test_run_check_pipeline_runs_in_fixed_order(tmp_path: Path) -> None:
    settings = make_settings(tmp_path, typecheck=True)
    calls: list[list[str]] = []

    def fake_run(command: list[str], cwd: Path) -> int:
        calls.append(command)
        return 0

    with patch("flint.tools.run_step", side_effect=fake_run):
        exit_code = run_check_pipeline(settings)

    assert exit_code == 0
    assert calls == [
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "pytest"],
        ["uv", "run", "pyright"],
    ]


def test_run_check_pipeline_stops_on_failure(tmp_path: Path) -> None:
    settings = make_settings(tmp_path, typecheck=True)
    calls: list[list[str]] = []

    def fake_run(command: list[str], cwd: Path) -> int:
        calls.append(command)
        return 1 if command[2] == "pytest" else 0

    with patch("flint.tools.run_step", side_effect=fake_run):
        exit_code = run_check_pipeline(settings)

    assert exit_code == 1
    assert calls == [
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "pytest"],
    ]
