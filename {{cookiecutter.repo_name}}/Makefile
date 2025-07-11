.PHONY: help dev-install test test-cov lint format quality pre-commit docs docs-build clean build publish upgrade {% if cookiecutter.project_type == "paper" %} paper-render paper-preview paper-check{% endif %}

help: ## Show this help message and available commands
	@echo "🚀 {{ cookiecutter.project_name }} - Development Commands"
	@echo "=================================================="
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "💡 Use 'make <command>' to run any command above"
	@echo "💡 All commands use the Makefile for consistency and ease of use"

dev-install: ## Install the package in development mode with all dependencies  
	@echo "📦 Installing development dependencies..."
	uv sync --all-extras --dev

test: ## Run tests with type checking
	@echo "🧪 Running tests..."
	uv run env DEV_TYPECHECK=1 pytest

test-cov: ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	uv run pytest --cov={{ cookiecutter.package_name }} --cov-report=html --cov-report=xml
	@echo "📊 Coverage report generated in htmlcov/"

lint: ## Run linting and fix issues
	@echo "🔍 Running linter..."
	uv run ruff check --fix .

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	uv run ruff format .

quality: lint format pre-commit ## Run all quality checks (lint, format)
	@echo "✅ All quality checks completed!"

pre-commit: ## Run pre-commit hooks on all files
	@echo "🔄 Running pre-commit hooks..."
	uv run pre-commit run --all-files

docs: ## Serve documentation locally
	@echo "📚 Starting documentation server..."
	uv run mkdocs serve

docs-build: ## Build documentation
	@echo "🏗️  Building documentation..."
	uv run mkdocs build

clean: ## Clean build artifacts and cache
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup completed!"

build: ## Build the package
	@echo "🏗️  Building package..."
	uv build

publish: ## Publish package to PyPI (requires authentication)
	@echo "🚀 Publishing to PyPI..."
	uv publish

# Development workflow commands

upgrade: ## Upgrade all dependencies
	@echo "⬆️  Upgrading dependencies..."
	uv sync --upgrade

{% if cookiecutter.project_type == "paper" %}
# Paper-specific commands
paper-render: ## Render Quarto paper to HTML and PDF
	@echo "📄 Rendering paper..."
	cd paper && quarto render paper.qmd --to html --to pdf
	@echo "✅ Paper rendered successfully!"

paper-preview: ## Preview paper in browser
	@echo "👀 Previewing paper..."
	cd paper && quarto preview paper.qmd

paper-check: ## Check paper for issues
	@echo "🔍 Checking paper..."
	cd paper && quarto check paper.qmd
{% endif %}