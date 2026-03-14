from __future__ import annotations

from pathlib import Path

import typer

from flint.config import load_project_settings
from flint.devloop import run_dev_loop
from flint.errors import FlintError
from flint.tools import build_run_command, run_check_pipeline, run_foreground

app = typer.Typer(
    name="flint",
    no_args_is_help=True,
    help="Opinionated dev loop CLI for existing Python ASGI projects.",
)


def _handle_error(exc: FlintError) -> None:
    first, second = exc.render()
    typer.secho(first, err=True, fg=typer.colors.RED)
    typer.echo(second, err=True)
    raise typer.Exit(exc.exit_code)


@app.command()
def run(cwd: Path = typer.Option(Path.cwd(), "--cwd", help="Project root to operate on.")) -> None:
    """Start the project's ASGI app."""
    try:
        settings = load_project_settings(cwd)
        exit_code = run_foreground(build_run_command(settings, reload_enabled=True), settings.root)
    except FlintError as exc:
        _handle_error(exc)
    raise typer.Exit(exit_code)


@app.command()
def dev(cwd: Path = typer.Option(Path.cwd(), "--cwd", help="Project root to operate on.")) -> None:
    """Start the app and watch-driven checks."""
    try:
        settings = load_project_settings(cwd)
        exit_code = run_dev_loop(settings)
    except FlintError as exc:
        _handle_error(exc)
    raise typer.Exit(exit_code)


@app.command()
def check(cwd: Path = typer.Option(Path.cwd(), "--cwd", help="Project root to operate on.")) -> None:
    """Run deterministic local checks."""
    try:
        settings = load_project_settings(cwd)
        exit_code = run_check_pipeline(settings)
    except FlintError as exc:
        _handle_error(exc)
    raise typer.Exit(exit_code)


def main() -> None:
    app()
