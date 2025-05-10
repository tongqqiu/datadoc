.PHONY: install format lint lint-fix typecheck test clean help

# Variables
PYTHON := poetry run python
RUFF := poetry run ruff
MYPY := poetry run mypy

help: ## Show this help message
	@echo 'Usage:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	poetry install --with dev

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
