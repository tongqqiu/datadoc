"""Extract schema from YAML files using Spark."""

from pathlib import Path
from typing import Any, Optional  # noqa: UP

import typer
import yaml
from pyspark.sql import SparkSession
from rich.console import Console
from rich.table import Table

from datadoc.models.odcs import LogicalType1

console = Console()


def read_config(config_path: str) -> dict[str, Any]:
    """Read and parse the YAML configuration file."""
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise typer.BadParameter(f"Error reading configuration file: {str(e)}")


def detect_schema(spark: SparkSession, data_path: str, format: str) -> dict:
    """Detect schema from data file using Spark and return a dict in ODCS shape."""
    df = spark.read.format(format).load(data_path)
    spark_schema = df.schema
    properties = []
    for field in spark_schema.fields:
        properties.append(
            {
                "name": field.name,
                "logicalType": str(map_spark_to_logical_type(field.dataType.typeName())),
                "physicalType": str(field.dataType),
                "required": not field.nullable,
            }
        )
    schema = {"name": "extracted_schema", "logicalType": "object", "properties": properties}
    return schema


def map_spark_to_logical_type(spark_type: str) -> LogicalType1:
    """Map Spark data type to ODCS logical type."""
    type_mapping = {
        "string": LogicalType1.string,
        "integer": LogicalType1.integer,
        "long": LogicalType1.integer,
        "double": LogicalType1.number,
        "float": LogicalType1.number,
        "boolean": LogicalType1.boolean,
        "date": LogicalType1.date,
        "timestamp": LogicalType1.date,
        "array": LogicalType1.array,
        "struct": LogicalType1.object,
        "map": LogicalType1.object,
    }
    return type_mapping.get(spark_type.lower(), LogicalType1.string)


def extract(
    config_path: str = typer.Argument(..., help="Path to the YAML configuration file"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Path to save the extracted schema"),  # noqa: UP
) -> None:
    """Extract schema from data files using Spark."""
    spark = None
    try:
        config = read_config(config_path)
        data_path = config.get("data_path")
        format = config.get("format", "csv")
        if not data_path:
            raise typer.BadParameter("data_path is required in configuration")
        console.print(f"Processing data from {data_path}...")
        spark = SparkSession.builder.appName("SchemaExtractor").getOrCreate()
        schema = detect_schema(spark, data_path, format)
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                yaml.dump(schema, f, sort_keys=False)
            console.print(f"Schema saved to {output_path}")
        table = Table(title="Extracted Schema")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Required", style="green")
        for prop in schema["properties"]:
            table.add_row(prop["name"], prop["logicalType"], str(prop["required"]))
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        raise typer.Exit(1)
    finally:
        if spark:
            spark.stop()
