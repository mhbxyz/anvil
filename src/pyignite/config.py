from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProjectConfig:
    """Minimal project configuration placeholder."""

    root_dir: Path
