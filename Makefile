.PHONY: install format lint lint-fix typecheck test clean help generate-models

# Variables
PYTHON := poetry run python
RUFF := poetry run ruff
MYPY := poetry run mypy

help: ## Show this help message
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make format        - Format code"
	@echo "  make lint          - Run linter"
	@echo "  make lint-fix      - Run linter and fix issues"
	@echo "  make typecheck     - Run type checker"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean up cache files"
	@echo "  make generate-models - Generate Pydantic models from JSON schema"

install: ## Install dependencies
	poetry install

format: ## Format code using Ruff
	$(RUFF) format .

lint: ## Run Ruff linter
	$(RUFF) check .

lint-fix: ## Run Ruff linter and fix issues
	$(RUFF) check --fix .

typecheck: ## Run mypy type checker
	$(MYPY) .

test: ## Run tests
	$(PYTHON) -m pytest

clean: ## Clean up Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

watch: ## Watch files and run format/lint on changes
	$(PYTHON) -m watchfiles "$(RUFF) format ." "$(RUFF) check ." .

all: format lint typecheck ## Run all checks

generate-models:
	$(PYTHON) scripts/generate_models.py
