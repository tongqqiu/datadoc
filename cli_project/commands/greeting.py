"""Greeting commands for the CLI application."""

from rich.console import Console
from rich.panel import Panel

console = Console()


def hello(name: str) -> None:
    """Greet someone by name.

    Args:
        name: The name of the person to greet.
    """
    console.print(
        Panel(
            f"[green]Hello, {name}![/green]",
            title="Greeting",
            border_style="green",
        )
    )
    return None


def greet(count: int, name: str) -> None:
    """Greet someone multiple times.

    Args:
        count: Number of times to repeat the greeting.
        name: The name of the person to greet.
    """
    for i in range(count):
        console.print(
            Panel(
                f"[green]Hello, {name}![/green]",
                title=f"Greeting {i + 1}/{count}",
                border_style="green",
            )
        )
    return None
