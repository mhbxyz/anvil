import typer
from rich.console import Console

from pyignite.commands import register_commands

app = typer.Typer(
    name="pyignite",
    no_args_is_help=True,
    help="PyIgnite CLI - developer toolchain for Python APIs.",
)
console = Console()


@app.callback()
def callback() -> None:
    """Main entrypoint for the CLI."""


register_commands(app)


def main() -> None:
    app()
