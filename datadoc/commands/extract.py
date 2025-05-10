"""Extract schema from data files using Spark."""

import glob
from pathlib import Path

import typer
from pyspark.sql import SparkSession
from rich.console import Console
from rich.table import Table

from datadoc.models.odcs import (
    LogicalType1,
    SchemaBaseProperty,
    SchemaObject,
)

app = typer.Typer()
console = Console()


def detect_schema(file_path: str) -> dict:
    """Detect schema from a file using Spark."""
    spark = SparkSession.builder.appName("SchemaDetection").getOrCreate()

    # Read the file and infer schema
    df = spark.read.format("yaml").load(file_path)
    schema = df.schema

    # Convert Spark schema to ODCS format
    properties = []
    for field in schema.fields:
        # Map Spark types to ODCS logical types
        logical_type = map_spark_to_logical_type(field.dataType.typeName())

        prop = SchemaBaseProperty(
            name=field.name,
            logicalType=logical_type,
            physicalType=str(field.dataType),
            required=not field.nullable,
            description=f"Detected from {file_path}",
        )
        properties.append(prop)

    return {
        "name": Path(file_path).stem,
        "properties": properties,
    }


def map_spark_to_logical_type(spark_type: str) -> LogicalType1:
    """Map Spark data types to ODCS logical types."""
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


def convert_to_odcs_schema(schema_dict: dict) -> SchemaObject:
    """Convert detected schema to ODCS SchemaObject."""
    return SchemaObject(
        name=schema_dict["name"],
        logicalType=LogicalType1.object,
        properties=schema_dict["properties"],
    )


@app.command()
def extract(
    file_pattern: str = typer.Argument(..., help="File pattern to process (e.g., 'data/*.yaml')"),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for the schema (default: schema.yaml)",
    ),
) -> None:
    """Extract schema from YAML files using Spark and convert to ODCS format."""
    spark = None
    try:
        # Find all matching files
        files = glob.glob(file_pattern)
        if not files:
            console.print(f"[red]No files found matching pattern: {file_pattern}[/red]")
            raise typer.Exit(1)

        # Initialize Spark session
        spark = SparkSession.builder.appName("SchemaDetection").getOrCreate()

        # Process each file
        schemas = []
        for file_path in files:
            console.print(f"Processing [blue]{file_path}[/blue]...")
            schema_dict = detect_schema(file_path)
            schema = convert_to_odcs_schema(schema_dict)
            schemas.append(schema)

        # Create output schema
        output_schema = {
            "schema": schemas,
        }

        # Save to file
        output_path = output or Path("schema.yaml")
        with open(output_path, "w") as f:
            import yaml

            yaml.dump(output_schema, f, sort_keys=False)

        console.print(f"\n[green]Schema extracted and saved to {output_path}[/green]")

        # Display summary
        table = Table(title="Extracted Schemas")
        table.add_column("File", style="cyan")
        table.add_column("Properties", style="magenta")

        for schema in schemas:
            table.add_row(schema.name, str(len(schema.properties)) if schema.properties else "0")

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)
    finally:
        # Stop Spark session
        if spark is not None:
            spark.stop()
