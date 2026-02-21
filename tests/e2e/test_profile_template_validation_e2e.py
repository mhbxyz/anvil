from __future__ import annotations

from pathlib import Path

from tests.e2e.helpers import run_pyqck


def test_new_rejects_unknown_profile(tmp_path: Path) -> None:
    result = run_pyqck(["new", "bad", "--profile", "worker"], cwd=tmp_path)

    assert result.returncode == 2
    assert "ERROR [usage] Unsupported profile `worker`." in result.stderr
    assert "Hint:" in result.stderr


def test_new_rejects_reserved_profile(tmp_path: Path) -> None:
    result = run_pyqck(["new", "bad", "--profile", "web"], cwd=tmp_path)

    assert result.returncode == 2
    assert "ERROR [usage] Profile `web` is reserved and not scaffoldable yet." in result.stderr
    assert "Hint:" in result.stderr


def test_new_rejects_unknown_template(tmp_path: Path) -> None:
    result = run_pyqck(
        ["new", "bad", "--profile", "api", "--template", "flask"],
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert "ERROR [usage] Unsupported template `flask` for profile `api`." in result.stderr
    assert "Hint:" in result.stderr


def test_new_rejects_incompatible_profile_template_pair(tmp_path: Path) -> None:
    result = run_pyqck(
        ["new", "bad", "--profile", "api", "--template", "baseline-cli"],
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert (
        "ERROR [usage] Template `baseline-cli` is not compatible with profile `api`."
        in result.stderr
    )
    assert "Hint:" in result.stderr
