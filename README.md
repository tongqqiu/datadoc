# CLI Project

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-1.7%2B-blue.svg)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern command-line interface example built with Python and Typer. This project demonstrates best practices for creating a Python CLI application, including:

- Modern Python features (type hints, f-strings)
- Rich terminal output
- Comprehensive testing
- Development tools (linting, formatting)
- Project structure and organization

## Features

- 🎨 Beautiful terminal output with Rich
- ✨ Type-safe CLI with Typer
- 🧪 Comprehensive test suite
- 🔍 Linting and formatting with Ruff
- 📝 Type checking with mypy
- 🛠️ Development tools (pre-commit, make)

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
make test
```

## Usage

After activating the virtual environment, you can use the CLI in two ways:

1. Using the entry point command:
```bash
cli-project hello
cli-project hello --name Alice
cli-project greet --count 3 --name Bob
```

2. Running the module directly:
```bash
python -m cli_project.cli hello
python -m cli_project.cli greet --count 3 --name Alice
```

You can also run commands without activating the virtual environment using:
```bash
poetry run cli-project hello
```

## Available Commands

- `hello`: Greet someone by name
  - Options:
    - `--name, -n`: Name to greet (default: "World")

- `greet`: Greet someone multiple times
  - Options:
    - `--count, -c`: Number of greetings (default: 1)
    - `--name, -n`: Name to greet (default: "World")

## Development

### Available Make Commands

```bash
make help        # Show all available commands
make install     # Install dependencies
make format      # Format code
make lint        # Run linter
make lint-fix    # Run linter and fix issues
make typecheck   # Run type checker
make test        # Run tests
make clean       # Clean up cache files
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality. Hooks include:
- Code formatting (Ruff)
- Linting (Ruff)
- Type checking (mypy)
- General git hooks (trailing whitespace, file endings, etc.)

## Project Structure

```
cli_project/
├── pyproject.toml          # Project configuration and dependencies
├── poetry.lock            # Locked dependencies
├── README.md              # Project documentation
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── Makefile               # Development commands
├── cli_project/           # Main package
│   ├── __init__.py
│   ├── cli.py            # CLI entry point
│   └── commands/         # Command modules
│       ├── __init__.py
│       └── greeting.py   # Greeting commands
└── tests/                # Test package
    ├── __init__.py
    └── test_cli.py      # CLI tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
