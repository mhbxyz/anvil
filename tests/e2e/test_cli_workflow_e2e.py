from __future__ import annotations

from pathlib import Path

from tests.e2e.helpers import run_pyqck


def test_e2e_cli_workflow_new_install_test_check(tmp_path: Path) -> None:
    create = run_pyqck(["new", "mycli", "--profile", "cli"], cwd=tmp_path)
    assert create.returncode == 0, create.stdout + create.stderr

    project_dir = tmp_path / "mycli"

    install = run_pyqck(["install"], cwd=project_dir, timeout=240)
    assert install.returncode == 0, install.stdout + install.stderr

    test_result = run_pyqck(["test"], cwd=project_dir)
    assert test_result.returncode == 0, test_result.stdout + test_result.stderr

    check_result = run_pyqck(["check"], cwd=project_dir)
    assert check_result.returncode == 0, check_result.stdout + check_result.stderr
