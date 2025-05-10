"""Main CLI entry point."""

from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from cli_project.commands import greeting

from .models.odcs import OpenDataContractStandardODCS

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


@app.command()
def validate(
    file: Path = typer.Argument(
        ...,
        help="Path to the YAML file to validate",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed validation errors",
    ),
) -> None:
    """
    Validate a YAML file against the Open Data Contract Standard (ODCS) schema.

    The command will check if the YAML file contains a valid data contract
    according to the ODCS specification.
    """
    try:
        # Read and parse YAML file
        with open(file) as f:
            yaml_content = yaml.safe_load(f)

        # Validate against Pydantic model
        contract = OpenDataContractStandardODCS.model_validate(yaml_content)

        # If we get here, validation passed
        console.print(
            Panel(
                "[green]✓[/green] YAML file is a valid ODCS data contract",
                title="Validation Successful",
                border_style="green",
            )
        )

        if verbose:
            # Show the validated contract details
            console.print("\n[bold]Contract Details:[/bold]")
            console.print(f"Version: {contract.version}")
            console.print(f"ID: {contract.id}")
            console.print(f"Name: {contract.name}")
            console.print(f"Status: {contract.status}")
            if contract.description:
                console.print(f"Description: {contract.description}")

    except yaml.YAMLError as e:
        console.print(
            Panel(
                f"[red]✗[/red] Invalid YAML format:\n{str(e)}",
                title="Validation Failed",
                border_style="red",
            )
        )
        raise typer.Exit(1)
    except Exception as e:
        console.print(
            Panel(
                f"[red]✗[/red] Invalid data contract:\n{str(e)}",
                title="Validation Failed",
                border_style="red",
            )
        )
        if verbose:
            console.print("\n[bold]Detailed Error:[/bold]")
            console.print(Syntax(str(e), "python", theme="monokai"))
        raise typer.Exit(1)


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
