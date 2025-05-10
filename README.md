# datadoc

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-1.7%2B-blue.svg)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/tongqqiu/datadoc/actions/workflows/ci.yml/badge.svg)](https://github.com/tongqqiu/datadoc/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/tongqqiu/datadoc?include_prereleases&sort=semver)](https://github.com/tongqqiu/datadoc/releases)

A modern command-line interface for validating and generating Open Data Contract Standard (ODCS) models, built with Python and Typer.

## Features

- 🎨 Beautiful terminal output with Rich
- ✨ Type-safe CLI with Typer
- 🧪 Comprehensive test suite
- 🔍 Linting and formatting with Ruff
- 📝 Type checking with mypy
- 🛠️ Development tools (pre-commit, Poetry)
- ✅ Continuous Integration with GitHub Actions

## Installation

First, configure Poetry to create the virtual environment in the project directory:
```bash
poetry config virtualenvs.in-project true
```

Then install the project:
```bash
poetry install
```

## Development Setup

1. Install development dependencies:
```bash
poetry install --with dev
```

2. Install pre-commit hooks:
```bash
poetry run pre-commit install
```

3. Run tests:
```bash
poetry run pytest
```

## Usage

After activating the virtual environment, you can use the CLI in two ways:

1. Using the entry point command:
```bash
datadoc validate path/to/contract.yaml

datadoc generate-models path/to/schema.json
```

2. Running the module directly:
```bash
python -m datadoc.cli validate path/to/contract.yaml
python -m datadoc.cli generate-models path/to/schema.json
```

You can also run commands without activating the virtual environment using:
```bash
poetry run datadoc validate path/to/contract.yaml
```

## Available Commands

- `validate`: Validate a YAML file against the ODCS schema
  - Arguments:
    - `file`: Path to the YAML file to validate
  - Options:
    - `--verbose, -v`: Show detailed validation errors

- `generate-models`: Generate Pydantic models from a JSON schema file
  - Arguments:
    - `schema_file`: Path to the JSON schema file
  - Options:
    - `--output, -o`: Path to the output Python file (default: models/odcs.py)
    - `--python-version, -p`: Target Python version for generated code (default: 3.11)

## Continuous Integration

This project uses GitHub Actions for CI. On every push and pull request to `main`, the following checks are run:
- Linting with Ruff
- Type checking with mypy
- Tests with pytest and coverage

See `.github/workflows/ci.yml` for details.

## Project Structure

```
datadoc/
├── __init__.py
├── cli.py                # CLI entry point
├── models/
│   ├── __init__.py
│   └── odcs.py           # Pydantic models (generated)
├── commands/
│   └── __init__.py
├── ...
.github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI workflow
mypy.ini                  # mypy configuration (ignores generated code)
pyproject.toml            # Project configuration and dependencies
README.md                 # Project documentation
tests/
    ├── __init__.py
    └── test_cli.py       # CLI tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Releases

This project uses semantic versioning. To create a new release:

1. Update the version in `pyproject.toml`:
   ```bash
   poetry version patch  # for bug fixes
   poetry version minor  # for new features
   poetry version major  # for breaking changes
   ```

2. Create and push a new tag:
   ```bash
   git tag v$(poetry version -s)
   git push origin v$(poetry version -s)
   ```

3. The GitHub Actions release workflow will automatically:
   - Build the package
   - Create a GitHub release
   - Upload the built package files
   - Generate release notes

You can find all releases on the [GitHub Releases page](https://github.com/tongqqiu/datadoc/releases).
