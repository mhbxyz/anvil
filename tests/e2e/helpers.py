from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def repo_src() -> Path:
    return repo_root() / "src"


def env_with_repo_src() -> dict[str, str]:
    env = dict(os.environ)
    previous = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{repo_src()}:{previous}" if previous else str(repo_src())
    return env


def run_pyqck(args: list[str], cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pyqck", *args],
        cwd=cwd,
        env=env_with_repo_src(),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
