# Generated Project Structure

This reference provides a complete overview of the project structure generated by the Pythonic Template.

## Overview

The Pythonic Template generates a well-organized Python project with modern tooling and best practices. The structure follows established conventions while providing flexibility for different project types.

## Complete Directory Tree

```text
my-python-project/                 # Root project directory
├── .github/                       # GitHub-specific files
│   ├── ISSUE_TEMPLATE/            # Issue templates
│   │   ├── bug_report.md          # Bug report template
│   │   └── feature_request.md     # Feature request template
│   ├── workflows/                 # GitHub Actions workflows
│   │   ├── ci.yml                 # Continuous integration
│   │   └── release.yml            # Release automation
│   ├── dependabot.yml             # Dependency updates
│   └── PULL_REQUEST_TEMPLATE.md   # PR template
├── docs/                          # Documentation source
│   ├── api/                       # API documentation
│   ├── getting-started/           # User guides
│   │   ├── installation.md        # Installation guide
│   │   ├── quick-start.md         # Quick start guide
│   │   └── configuration.md       # Configuration guide
│   ├── development/               # Developer docs
│   │   ├── contributing.md        # Contributing guide
│   │   └── testing.md             # Testing guide
│   ├── assets/                    # Documentation assets
│   │   └── images/                # Images and diagrams
│   └── index.md                   # Documentation homepage
├── src/                           # Source code
│   └── my_python_project/         # Main package
│       ├── __init__.py            # Package initialization
│       ├── main.py                # Main module
│       ├── core/                  # Core functionality
│       │   ├── __init__.py
│       │   └── base.py            # Base classes
│       └── utils/                 # Utility modules
│           ├── __init__.py
│           └── helpers.py         # Helper functions
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── test_main.py               # Main module tests
│   ├── core/                      # Core module tests
│   │   ├── __init__.py
│   │   └── test_base.py
│   └── utils/                     # Utility tests
│       ├── __init__.py
│       └── test_helpers.py
├── scripts/                       # Development scripts
│   ├── setup.sh                   # Environment setup
│   ├── test.sh                    # Test runner
│   └── build.sh                   # Build script
├── .vscode/                       # VS Code configuration
│   ├── settings.json              # Editor settings
│   ├── launch.json                # Debug configuration
│   └── extensions.json            # Recommended extensions
├── .gitignore                     # Git ignore rules
├── .pre-commit-config.yaml        # Pre-commit hooks
├── .devcontainer/
│   └── Dockerfile                 # Docker image definition
├── docker-compose.yml             # Docker Compose setup
├── LICENSE                        # License file
├── README.md                      # Project README
├── CHANGELOG.md                   # Change log
├── CONTRIBUTING.md                # Contributing guidelines
├── pyproject.toml                 # Project configuration
└── mkdocs.yml                     # Documentation config
```

## Core Files

### `pyproject.toml`

Central configuration file following PEP 518:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-python-project"
version = "0.1.0"
description = "A modern Python project"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.13"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    # Runtime dependencies
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "pre-commit>=3.0.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.24.0",
]

[project.urls]
"Homepage" = "https://github.com/your-name/my-python-project"
"Documentation" = "https://your-name.github.io/my-python-project"
"Repository" = "https://github.com/your-name/my-python-project"
"Bug Tracker" = "https://github.com/your-name/my-python-project/issues"

[project.scripts]
my-python-project = "my_python_project.main:main"

[tool.ruff]
line-length = 88
target-version = "py313"
src = ["src"]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "D",   # pydocstyle
]
ignore = [
    "D100", # Missing docstring in public module
    "D104", # Missing docstring in public package
]

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
]
```

### `README.md`

Comprehensive project README:

```markdown
# My Python Project

[![CI](https://github.com/your-name/my-python-project/workflows/CI/badge.svg)](https://github.com/your-name/my-python-project/actions)
[![Coverage](https://codecov.io/gh/your-name/my-python-project/branch/main/graph/badge.svg)](https://codecov.io/gh/your-name/my-python-project)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://your-name.github.io/my-python-project)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/adamamer20/pythonic-template/blob/main/LICENSE)

A modern Python project with best practices and modern tooling.

## Features

- 🚀 Modern Python (3.13+) with type hints
- 📦 Dependency management with UV
- 🧹 Code formatting with Ruff
- 🔍 Static analysis with mypy
- 🧪 Testing with pytest
- 📚 Documentation with MkDocs Material
- 🔄 CI/CD with GitHub Actions
- 🐳 Docker support
- 📋 Pre-commit hooks for code quality

## Quick Start

### Installation

```bash
pip install my-python-project
```

### Usage

```python
from my_python_project import main

# Your code here
```

## Development

### Setup

```bash
git clone https://github.com/your-name/my-python-project.git
cd my-python-project
pip install uv
uv pip install -e .[dev]
pre-commit install
```

### Testing

```bash
pytest
```

### Documentation

```bash
mkdocs serve
```

## Contributing

See [CONTRIBUTING.md](https://github.com/adamamer20/pythonic-template/blob/main/CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](https://github.com/adamamer20/pythonic-template/blob/main/LICENSE) for details.

## Source Code Structure

### Main Package (`src/my_python_project/`)

#### `__init__.py`

Package initialization with version and public API:

```python
"""My Python Project - A modern Python project."""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .main import main

__all__ = ["main"]
```

#### `main.py`

Main application entry point:

```python
"""Main module for My Python Project."""

import argparse
import sys
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main entry point for the application.

    Parameters
    ----------
    argv : Optional[Sequence[str]]
        Command line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit code (0 for success, non-zero for error).
    """
    parser = argparse.ArgumentParser(
        description="A modern Python project"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args(argv)

    print("Hello from My Python Project!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

#### `core/base.py`

Base classes and core functionality:

```python
"""Core base classes and functionality."""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class Processor(Protocol):
    """Protocol for data processors."""

    def process(self, data: Any) -> Any:
        """Process the input data."""
        ...


class BaseProcessor(ABC):
    """Abstract base class for processors.

    This class provides a template for implementing
    data processing components.
    """

    def __init__(self, name: str) -> None:
        """Initialize the processor.

        Parameters
        ----------
        name : str
            Name of the processor.
        """
        self.name = name

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process the input data.

        Parameters
        ----------
        data : Any
            Input data to process.

        Returns
        -------
        Any
            Processed data.
        """
```

#### `utils/helpers.py`

Utility functions and helpers:

```python
"""Utility functions and helpers."""

import logging
from pathlib import Path
from typing import Union


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.

    Parameters
    ----------
    level : str, default="INFO"
        Logging level.
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Parameters
    ----------
    path : Union[str, Path]
        Directory path to ensure exists.

    Returns
    -------
    Path
        The directory path as a Path object.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
```

## Test Structure

### `tests/conftest.py`

Pytest configuration and shared fixtures:

```python
"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path
import tempfile
from typing import Generator


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing.

    Yields
    ------
    Path
        Temporary directory path.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_data() -> dict:
    """Sample data for testing.

    Returns
    -------
    dict
        Sample data dictionary.
    """
    return {
        "name": "test",
        "value": 42,
        "items": ["a", "b", "c"]
    }
```

### `tests/test_main.py`

Main module tests:

```python
"""Tests for the main module."""

import pytest
from my_python_project.main import main


def test_main_returns_zero():
    """Test that main returns 0 on success."""
    result = main([])
    assert result == 0


def test_main_with_version(capsys):
    """Test main with --version flag."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "0.1.0" in captured.out


def test_main_help(capsys):
    """Test main with --help flag."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "A modern Python project" in captured.out
```

## Documentation Structure

### `docs/index.md`

Documentation homepage:

```markdown
# My Python Project

Welcome to My Python Project documentation!

This project demonstrates modern Python development practices
with comprehensive tooling and documentation.

## Features

- Modern Python 3.13+ with type hints
- Fast development with UV
- Code quality with Ruff and mypy
- Comprehensive testing with pytest
- Beautiful documentation with MkDocs Material

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Quick Start](getting-started/quick-start.md)
- [API Reference](api/)
- [Contributing](development/contributing.md)

## Getting Started

Install the package:

```bash
pip install my-python-project
```

Basic usage:

```python
from my_python_project import main

# Use the package
main()
```

## Support

- [GitHub Issues](https://github.com/your-name/my-python-project/issues)
- [Documentation](https://your-name.github.io/my-python-project)
- [Discussions](https://github.com/your-name/my-python-project/discussions)

### `mkdocs.yml`

Documentation configuration:

```yaml
site_name: My Python Project
site_description: A modern Python project with best practices
site_url: https://your-name.github.io/my-python-project
repo_url: https://github.com/your-name/my-python-project
repo_name: your-name/my-python-project

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
    - Configuration: getting-started/configuration.md
  - Development:
    - Contributing: development/contributing.md
    - Testing: development/testing.md
  - API Reference: api/

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: light-blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      accent: light-blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy
    - content.code.annotate

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: numpy
            show_source: true
            show_root_heading: true

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
```

## CI/CD Structure

### `.github/workflows/ci.yml`

Comprehensive CI pipeline:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.11, 3.12, 3.13]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install UV
      run: pip install uv

    - name: Install dependencies
      run: uv pip install -e .[dev]

    - name: Run linting
      run: ruff check .

    - name: Run formatting check
      run: ruff format --check .

    - name: Run type checking
      run: mypy src

    - name: Run tests
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.13
    - name: Install dependencies
      run: |
        pip install uv
        uv pip install -e .[dev]
    - name: Build documentation
      run: mkdocs build --strict
```

## Docker Structure

### `Dockerfile`

Multi-stage Docker build:

```dockerfile
# Build stage
FROM python:3.13-slim as builder

WORKDIR /app

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system .

# Runtime stage
FROM python:3.13-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy source code
COPY src/ ./src/

# Set ownership
RUN chown -R app:app /app

USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import my_python_project; print('OK')" || exit 1

ENTRYPOINT ["python", "-m", "my_python_project"]
```

### `docker-compose.yml`

Development environment:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/.venv
    environment:
      - PYTHONPATH=/app/src
    command: python -m my_python_project

  docs:
    build: .
    ports:
      - "8001:8000"
    volumes:
      - .:/app
    command: mkdocs serve --dev-addr 0.0.0.0:8000

  test:
    build: .
    volumes:
      - .:/app
    command: pytest
```

This comprehensive structure provides a solid foundation for any Python project, with modern tooling, best practices, and comprehensive documentation.
