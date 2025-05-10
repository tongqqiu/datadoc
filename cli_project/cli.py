"""Main CLI entry point."""

import typer
from rich.console import Console
from rich.panel import Panel

from cli_project.commands import greeting

app = typer.Typer(
    name="cli-project",
    help="A modern command-line interface example",
    add_completion=False,
)
console = Console()


@app.command()
def hello(
    name: str = typer.Option(
        "World",
        "--name",
        "-n",
        help="Name to greet",
    ),
) -> None:
    """Greet someone by name."""
    greeting.hello(name)


@app.command()
def greet(
    count: int = typer.Option(
        1,
        "--count",
        "-c",
        help="Number of greetings",
        min=1,
    ),
    name: str = typer.Option(
        "World",
        "--name",
        "-n",
        help="Name to greet",
    ),
) -> None:
    """Greet someone multiple times."""
    greeting.greet(count, name)


def main() -> None:
    """Main entry point for the CLI."""
    try:
        app()
    except Exception as e:
        console.print(
            Panel(
                f"[red]Error:[/red] {str(e)}",
                title="Error",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    main()
