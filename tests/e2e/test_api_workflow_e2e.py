from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

from tests.e2e.helpers import env_with_repo_src, run_pyqck


def _create_project(tmp_path: Path, name: str = "myapi") -> Path:
    create = run_pyqck(["new", name, "--profile", "api", "--template", "fastapi"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr
    return tmp_path / name


def _set_run_port(project_dir: Path, port: int) -> None:
    config_path = project_dir / "pyquick.toml"
    content = config_path.read_text(encoding="utf-8")
    config_path.write_text(content.replace("port = 8000", f"port = {port}"), encoding="utf-8")


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def test_e2e_api_workflow_new_run_test_check(tmp_path: Path) -> None:
    project_dir = _create_project(tmp_path, "myapi")
    sync = run_pyqck(["install"], cwd=project_dir, timeout=240)
    assert sync.returncode == 0, sync.stdout + sync.stderr

    test_result = run_pyqck(["test"], cwd=project_dir)
    assert test_result.returncode == 0, test_result.stdout + test_result.stderr

    check_result = run_pyqck(["check"], cwd=project_dir)
    assert check_result.returncode == 0, check_result.stdout + check_result.stderr

    _set_run_port(project_dir, _free_port())
    run_process = subprocess.Popen(
        [sys.executable, "-m", "pyqck", "run"],
        cwd=project_dir,
        env=env_with_repo_src(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(1.5)

    assert run_process.poll() is None

    run_process.terminate()
    run_process.wait(timeout=5)


def test_e2e_failure_missing_tool_shows_actionable_hint(tmp_path: Path) -> None:
    project_dir = _create_project(tmp_path, "broken-tool")

    config_path = project_dir / "pyquick.toml"
    content = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        content.replace('packaging = "uv"', 'packaging = "missing-tool"'), encoding="utf-8"
    )

    result = run_pyqck(["test"], cwd=project_dir)
    assert result.returncode == 1
    assert "ERROR [tooling]" in result.stderr
    assert "Hint:" in result.stderr


def test_e2e_failure_invalid_config_shows_diagnostics(tmp_path: Path) -> None:
    project_dir = _create_project(tmp_path, "broken-config")

    config_path = project_dir / "pyquick.toml"
    config_path.write_text("[run]\nport = 'bad'\n", encoding="utf-8")

    result = run_pyqck(["run"], cwd=project_dir)
    assert result.returncode == 2
    assert "ERROR [config]" in result.stderr
    assert "Hint:" in result.stderr
