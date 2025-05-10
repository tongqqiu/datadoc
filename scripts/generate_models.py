"""Script to generate Pydantic models from ODCS JSON schema."""

import json
import subprocess
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = PROJECT_ROOT / "schema" / "odcs-json-schema-latest.json"
OUTPUT_PATH = PROJECT_ROOT / "cli_project" / "models" / "odcs.py"


def main() -> None:
    """Generate Pydantic models from ODCS JSON schema."""
    # Read the schema file
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    # Generate models using datamodel-code-generator
    cmd = [
        "poetry",
        "run",
        "datamodel-codegen",
        "--input",
        str(SCHEMA_PATH),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(OUTPUT_PATH),
        "--target-python-version",
        "3.11",
        "--use-standard-collections",
        "--use-schema-description",
        "--use-field-description",
        "--use-default",
        "--use-title-as-name",
        "--use-annotated",
        "--use-union-operator",
        "--output-model-type",
        "pydantic_v2.BaseModel",
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully generated models at {OUTPUT_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating models: {e}")
        raise


if __name__ == "__main__":
    main()
