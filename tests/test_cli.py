from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from flint.cli import app

runner = CliRunner()


def test_check_command_exits_zero_on_success(tmp_path: Path) -> None:
    (tmp_path / "src" / "demo").mkdir(parents=True)
    (tmp_path / "src" / "demo" / "main.py").write_text("app = object()\n")

    with patch("flint.cli.run_check_pipeline", return_value=0):
        result = runner.invoke(app, ["check", "--cwd", str(tmp_path)])

    assert result.exit_code == 0


def test_run_command_renders_actionable_config_error(tmp_path: Path) -> None:
    result = runner.invoke(app, ["run", "--cwd", str(tmp_path)])

    assert result.exit_code == 2
    assert "ERROR [config] Could not resolve an ASGI app target." in result.stderr
    assert "Hint:" in result.stderr
