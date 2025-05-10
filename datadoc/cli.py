"""Main CLI entry point."""

from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .models.odcs import OpenDataContractStandardODCS

app = typer.Typer(
    name="datadoc",
    help="A modern command-line interface example",
    add_completion=False,
)
console = Console()


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


@app.command()
def generate_models(
    schema_file: Path = typer.Argument(
        ...,
        help="Path to the JSON schema file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_file: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to the output Python file (default: models/odcs.py)",
        file_okay=True,
        dir_okay=False,
        writable=True,
    ),
    python_version: str = typer.Option(
        "3.11",
        "--python-version",
        "-p",
        help="Target Python version for generated code",
    ),
) -> None:
    """
    Generate Pydantic models from a JSON schema file.

    This command uses datamodel-codegen to generate Python Pydantic models
    from a JSON schema file. The generated models can be used for validation
    and type checking.
    """
    import subprocess

    if output_file is None:
        output_file = Path("models") / "odcs.py"

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate models using datamodel-codegen
    cmd = [
        "datamodel-codegen",
        "--input",
        str(schema_file),
        "--input-file-type",
        "json",
        "--output",
        str(output_file),
        "--target-python-version",
        python_version,
        "--use-collections",
        "--use-schema-description",
        "--use-field-description",
        "--use-typed-dict",
    ]

    try:
        subprocess.run(cmd, check=True)
        console.print(
            Panel(
                f"[green]✓[/green] Successfully generated models at {output_file}",
                title="Model Generation Successful",
                border_style="green",
            )
        )
    except subprocess.CalledProcessError as e:
        console.print(
            Panel(
                f"[red]✗[/red] Error generating models:\n{str(e)}",
                title="Model Generation Failed",
                border_style="red",
            )
        )
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
