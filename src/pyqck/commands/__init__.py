import typer

from pyqck.commands import check, dev, fmt, install, lint, new, run, test


def register_commands(app: typer.Typer) -> None:
    """Register all command groups on the root app."""

    passthrough_context = {
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }

    app.command(name="new")(new.new_command)
    app.command(name="install", context_settings=passthrough_context)(install.install_command)
    app.command(name="sync", context_settings=passthrough_context)(install.install_command)
    app.command(name="dev")(dev.dev_command)
    app.command(name="run", context_settings=passthrough_context)(run.run_command)
    app.command(name="test", context_settings=passthrough_context)(test.test_command)
    app.command(name="lint", context_settings=passthrough_context)(lint.lint_command)
    app.command(name="fmt", context_settings=passthrough_context)(fmt.fmt_command)
    app.command(name="check")(check.check_command)
