import subprocess
import sys


def test_cli_help_exit_code_zero() -> None:
    process = subprocess.run(
        [sys.executable, "-m", "flint", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0
    assert "Flint CLI" in process.stdout
    assert "│ install" not in process.stdout
    assert "│ sync" not in process.stdout
