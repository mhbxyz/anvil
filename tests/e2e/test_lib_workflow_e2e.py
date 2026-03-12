from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import time

from tests.e2e.helpers import env_with_repo_src, run_flint


def test_e2e_lib_workflow_new_install_test_check(tmp_path: Path) -> None:
    create = run_flint(["new", "mylib", "--profile", "lib"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr

    project_dir = tmp_path / "mylib"

    install = subprocess.run(
        ["uv", "sync", "--extra", "dev"],
        cwd=project_dir,
        env=env_with_repo_src(),
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )
    assert install.returncode == 0, install.stdout + install.stderr

    test_result = run_flint(["test"], cwd=project_dir)
    assert test_result.returncode == 0, test_result.stdout + test_result.stderr

    check_result = run_flint(["check"], cwd=project_dir)
    assert check_result.returncode == 0, check_result.stdout + check_result.stderr


def test_e2e_lib_run_is_rejected_with_usage_error(tmp_path: Path) -> None:
    create = run_flint(["new", "mylib", "--profile", "lib"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr
    project_dir = tmp_path / "mylib"

    result = run_flint(["run"], cwd=project_dir)

    assert result.returncode == 2
    assert "ERROR [usage]" in result.stderr
    assert "`flint run` is not supported for profile `lib`." in result.stderr


def test_e2e_lib_dev_runs_in_checks_only_mode(tmp_path: Path) -> None:
    create = run_flint(["new", "mylib", "--profile", "lib"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr
    project_dir = tmp_path / "mylib"

    install = subprocess.run(
        ["uv", "sync", "--extra", "dev"],
        cwd=project_dir,
        env=env_with_repo_src(),
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )
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
