import typer

from pyignite.commands import check, dev, fmt, lint, run, test


def register_commands(app: typer.Typer) -> None:
    """Register all command groups on the root app."""

    app.command()(dev.dev_command)
    app.command()(run.run_command)
    app.command()(test.test_command)
    app.command()(lint.lint_command)
    app.command()(fmt.fmt_command)
    app.command()(check.check_command)
