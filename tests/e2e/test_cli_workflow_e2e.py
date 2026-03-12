from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import time

from tests.e2e.helpers import env_with_repo_src, run_flint


def test_e2e_cli_workflow_new_install_test_check(tmp_path: Path) -> None:
    create = run_flint(["new", "mycli", "--profile", "cli"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr

    project_dir = tmp_path / "mycli"

    install = run_flint(["install"], cwd=project_dir, timeout=240)
    assert install.returncode == 0, install.stdout + install.stderr

    test_result = run_flint(["test"], cwd=project_dir)
    assert test_result.returncode == 0, test_result.stdout + test_result.stderr

    check_result = run_flint(["check"], cwd=project_dir)
    assert check_result.returncode == 0, check_result.stdout + check_result.stderr


def test_e2e_cli_run_executes_entrypoint(tmp_path: Path) -> None:
    create = run_flint(["new", "mycli", "--profile", "cli"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr
    project_dir = tmp_path / "mycli"

    install = run_flint(["install"], cwd=project_dir, timeout=240)
    assert install.returncode == 0, install.stdout + install.stderr

    result = run_flint(["run"], cwd=project_dir)

    assert result.returncode == 0
    assert "hello from flint cli profile" in result.stdout


def test_e2e_cli_dev_runs_in_checks_only_mode(tmp_path: Path) -> None:
    create = run_flint(["new", "mycli", "--profile", "cli"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr
    project_dir = tmp_path / "mycli"

    install = run_flint(["install"], cwd=project_dir, timeout=240)
    assert install.returncode == 0, install.stdout + install.stderr

    process = subprocess.Popen(
        [sys.executable, "-m", "flint", "dev"],
        cwd=project_dir,
        env=env_with_repo_src(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(1.0)

    assert process.poll() is None

    process.terminate()
    process.wait(timeout=5)
