"""Tests for the extract command."""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from datadoc.cli import app
from datadoc.commands.extract import map_spark_to_logical_type
from datadoc.models.odcs import LogicalType1

runner = CliRunner()


def test_map_spark_to_logical_type():
    """Test mapping Spark types to ODCS logical types."""
    assert map_spark_to_logical_type("string") == LogicalType1.string
    assert map_spark_to_logical_type("integer") == LogicalType1.integer
    assert map_spark_to_logical_type("double") == LogicalType1.number
    assert map_spark_to_logical_type("boolean") == LogicalType1.boolean
    assert map_spark_to_logical_type("date") == LogicalType1.date
    assert map_spark_to_logical_type("array") == LogicalType1.array
    assert map_spark_to_logical_type("struct") == LogicalType1.object
    assert map_spark_to_logical_type("unknown") == LogicalType1.string  # default case


def test_extract_command():
    """Test the extract command with a sample configuration and data file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample data file (CSV)
        data_content = """name,age,is_active,scores,address
John Doe,30,true,"[85, 90, 95]","{""street"": ""123 Main St"", ""city"": ""Boston""}"
"""
        data_file = Path(temp_dir) / "test.csv"
        data_file.write_text(data_content)

        # Create a configuration file
        config_content = f"""
data_path: "{str(data_file)}"
format: "csv"
"""
        config_file = Path(temp_dir) / "config.yaml"
        config_file.write_text(config_content)

        # Run the extract command
        result = runner.invoke(app, ["extract", str(config_file), "--output", str(Path(temp_dir) / "schema.yaml")])
        if result.exit_code != 0:
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)
        assert result.exit_code == 0

        # Check if schema file was created
        schema_file = Path(temp_dir) / "schema.yaml"
        assert schema_file.exists()

        # Read and verify schema content
        schema_content = schema_file.read_text()
        assert "name:" in schema_content
        assert "properties:" in schema_content
        assert "logicalType:" in schema_content


def test_extract_command_no_config():
    """Test the extract command with a non-existent configuration file."""
    result = runner.invoke(app, ["extract", "nonexistent.yaml"])
    assert result.exit_code in (1, 2)
    assert "Error" in result.stdout


def test_extract_command_invalid_config():
    """Test the extract command with invalid YAML configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an invalid YAML file
        config_file = Path(temp_dir) / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: {")

        # Run the extract command
        result = runner.invoke(app, ["extract", str(config_file)])
        assert result.exit_code in (1, 2)
        assert "Error" in result.stdout
