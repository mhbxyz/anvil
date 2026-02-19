import subprocess
import sys


def test_cli_help_exit_code_zero() -> None:
    process = subprocess.run(
        [sys.executable, "-m", "pyignite", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0
    assert "PyIgnite CLI" in process.stdout
