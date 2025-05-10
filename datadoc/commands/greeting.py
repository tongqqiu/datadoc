"""Greeting commands for the CLI application."""

from rich.console import Console

console = Console()


def hello(name: str) -> None:
    """Print a greeting message."""
    print(f"Hello, {name}!")


def greet(count: int, name: str) -> None:
    """Print a greeting message multiple times."""
    for _ in range(count):
        print(f"Hello, {name}!")
