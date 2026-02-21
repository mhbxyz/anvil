import typer

from pyqck.commands._common import build_adapters_or_exit
from pyqck.tooling import ToolError, ToolKey


def install_command(ctx: typer.Context) -> None:
    """Sync project dependencies via configured packaging backend."""

    adapters = build_adapters_or_exit()
    args = tuple(ctx.args) if ctx.args else ("sync", "--extra", "dev")

    try:
        result = adapters.run(ToolKey.PACKAGING, args=args)
    except ToolError as exc:
        typer.secho(f"ERROR [tooling] {exc.message}", fg=typer.colors.RED, err=True)
        typer.secho(f"Hint: {exc.hint}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=1) from exc

    if result.stdout:
        typer.echo(result.stdout, nl=False)
    if result.stderr:
        typer.echo(result.stderr, err=True, nl=False)

    if result.exit_code == 0:
        typer.secho("OK [install]", fg=typer.colors.GREEN)
        return

    typer.secho(
        f"ERROR [tooling] Dependency sync failed via `{result.command[0]}`.",
        fg=typer.colors.RED,
        err=True,
    )
    typer.secho(
        "Hint: Resolve backend errors above, then retry `pyqck install`.",
        fg=typer.colors.YELLOW,
        err=True,
    )
    raise typer.Exit(code=result.exit_code)
