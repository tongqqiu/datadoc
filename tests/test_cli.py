"""Tests for CLI commands."""

import json
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from datadoc.cli import app


def test_generate_models_success(tmp_path: Path) -> None:
    """Test successful model generation."""
    # Create a temporary schema file
    schema_file = tmp_path / "schema.json"
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}
    schema_file.write_text(json.dumps(schema))

    # Create output directory
    output_dir = tmp_path / "models"
    output_dir.mkdir()
    output_file = output_dir / "test_models.py"

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        runner = CliRunner()
        result = runner.invoke(app, ["generate-models", str(schema_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert "Successfully generated models" in result.stdout
        mock_run.assert_called_once()


def test_generate_models_error(tmp_path: Path) -> None:
    """Test model generation with error."""
    import subprocess

    # Create a temporary schema file
    schema_file = tmp_path / "schema.json"
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}
    schema_file.write_text(json.dumps(schema))

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, ["datamodel-codegen"])  # Simulate process error
        runner = CliRunner()
        result = runner.invoke(app, ["generate-models", str(schema_file)])

        assert result.exit_code == 1
        assert "Error generating models" in result.stdout
        mock_run.assert_called_once()


def test_generate_models_default_output(tmp_path: Path) -> None:
    """Test model generation with default output path."""
    # Create a temporary schema file
    schema_file = tmp_path / "schema.json"
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}
    schema_file.write_text(json.dumps(schema))

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        runner = CliRunner()
        result = runner.invoke(app, ["generate-models", str(schema_file)])

        assert result.exit_code == 0
        assert "Successfully generated models" in result.stdout
        mock_run.assert_called_once()
        # Check that default output path was used
        cmd_args = mock_run.call_args[0][0]
        output_index = cmd_args.index("--output")
        assert cmd_args[output_index + 1] == "models/odcs.py"
