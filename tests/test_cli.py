"""Tests for CLI commands."""

from typer.testing import CliRunner

from cli_project.cli import app


def test_hello_default() -> None:
    """Test hello command with default name."""
    runner = CliRunner()
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_hello_custom_name() -> None:
    """Test hello command with custom name."""
    runner = CliRunner()
    result = runner.invoke(app, ["hello", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.stdout


def test_greet_default() -> None:
    """Test greet command with default values."""
    runner = CliRunner()
    result = runner.invoke(app, ["greet"])
    assert result.exit_code == 0
    assert result.stdout.count("Hello, World!") == 1


def test_greet_multiple_times() -> None:
    """Test greet command with multiple greetings."""
    runner = CliRunner()
    result = runner.invoke(app, ["greet", "--count", "3", "--name", "Bob"])
    assert result.exit_code == 0
    assert result.stdout.count("Hello, Bob!") == 3


def test_greet_short_options() -> None:
    """Test greet command with short options."""
    runner = CliRunner()
    result = runner.invoke(app, ["greet", "-c", "2", "-n", "Charlie"])
    assert result.exit_code == 0
    assert result.stdout.count("Hello, Charlie!") == 2


def test_greet_invalid_count() -> None:
    """Test greet command with invalid count."""
    runner = CliRunner()
    result = runner.invoke(app, ["greet", "--count", "0"])
    assert result.exit_code != 0
    assert "Error" in result.stdout
