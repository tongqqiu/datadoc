"""Script to generate Pydantic models from ODCS JSON schema."""

import subprocess
from pathlib import Path


def main() -> None:
    """Generate Pydantic models from JSON schema."""
    project_root = Path(__file__).parent.parent
    schema_file = project_root / "schema" / "odcs-json-schema-latest.json"
    output_file = project_root / "datadoc" / "models" / "odcs.py"

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate models using datamodel-codegen
    cmd = [
        "poetry",
        "run",
        "datamodel-codegen",
        "--input",
        str(schema_file),
        "--input-file-type",
        "json",
        "--output",
        str(output_file),
        "--target-python-version",
        "3.11",
        "--use-collections",
        "--use-schema-description",
        "--use-field-description",
        "--use-typed-dict",
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully generated models at {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating models: {e}")
        raise


if __name__ == "__main__":
    main()
