# Modern Development Stack

The Pythonic Template is built around the most modern and efficient Python development tools available. This page explains each tool and why it was chosen.

## Package Management: uv ⚡

**[uv](https://github.com/astral-sh/uv)** is an extremely fast Python package installer and resolver, written in Rust.

### Why uv?

- **🚀 Speed**: 10-100x faster than pip
- **🔒 Reliability**: Reliable dependency resolution
- **🧹 Clean**: No separate requirements.txt needed
- **🔄 Compatible**: Drop-in replacement for pip

### Usage in Generated Projects

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Add new dependency
uv add requests

# Install specific version
uv add "numpy>=1.24.0"

# Remove dependency
uv remove requests
```

### Configuration

```toml
# pyproject.toml - uv respects PEP 621
[project]
dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.8.0",
]
```

## Code Quality: Ruff 🦀

**[Ruff](https://github.com/astral-sh/ruff)** is an extremely fast Python linter and code formatter, written in Rust.

### Why Ruff?

- **⚡ Lightning Fast**: 10-100x faster than traditional tools
- **🔧 All-in-One**: Replaces flake8, isort, pydocstyle, and more
- **🎯 Comprehensive**: 700+ built-in rules
- **🔄 Compatible**: Drop-in replacement for existing tools

### Included Rules

The template configures Ruff with carefully selected rules:

```toml
[tool.ruff.lint]
select = [
    "E", "W",     # pycodestyle errors and warnings
    "F",          # pyflakes
    "I",          # isort (import sorting)
    "B",          # flake8-bugbear (likely bugs)
    "C4",         # flake8-comprehensions
    "UP",         # pyupgrade (modern Python)
    "SIM",        # flake8-simplify
    "TCH",        # flake8-type-checking
    "Q",          # flake8-quotes
    "PL",         # pylint
    "PT",         # flake8-pytest-style
]
```

### Usage

```bash
# Check code quality
ruff check .

# Fix automatically
ruff check . --fix

# Format code
ruff format .

# Check specific file
ruff check src/my_package/main.py
```

### Integration

Ruff is integrated everywhere:

- **Pre-commit hooks**: Automatic checking on commit
- **GitHub Actions**: CI/CD pipeline validation
- **VS Code**: Real-time linting and formatting
- **Make targets**: `make lint` and `make format`

## Testing: pytest 🧪

**[pytest](https://pytest.org/)** is the de facto standard for Python testing.

### Why pytest?

- **🎯 Simple**: Write tests as simple functions
- **🔧 Powerful**: Rich fixture system and plugins
- **📊 Detailed**: Excellent error reporting
- **🔗 Ecosystem**: Huge plugin ecosystem

### Configuration

```toml
[tool.pytest.ini_options]
minversion = "8.0"
pythonpath = "src"              # Find modules in src/
testpaths = ["tests"]           # Test discovery
filterwarnings = [              # Warning handling
    "error",
    "ignore::UserWarning",
    "ignore::DeprecationWarning"
]
```

### Testing Patterns

The template includes examples of modern testing patterns:

```python
# tests/test_example.py
import pytest
from my_package import process_data

class TestProcessData:
    """Test the process_data function."""

    def test_basic_functionality(self):
        """Test basic data processing."""
        input_data = [{"name": "test", "value": 42}]
        result = process_data(input_data)
        assert len(result) == 1

    @pytest.mark.parametrize("input_val,expected", [
        ([], []),
        ([{"key": "val"}], ["val"]),
        ([{"a": 1}, {"b": 2}], [1, 2]),
    ])
    def test_parametrized(self, input_val, expected):
        """Test with multiple parameter combinations."""
        result = process_data(input_val)
        assert result == expected

    def test_error_handling(self):
        """Test error conditions."""
        with pytest.raises(ValueError, match="Invalid input"):
            process_data(None)
```

### Coverage Integration

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Coverage configuration in pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Documentation: MkDocs Material 📚

**[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** provides beautiful, responsive documentation.

### Why MkDocs Material?

- **🎨 Beautiful**: Modern, professional design
- **📱 Responsive**: Works perfectly on all devices
- **⚡ Fast**: Static site generation
- **🔍 Smart Search**: Built-in search functionality
- **🎯 Python-focused**: Excellent Python integration

### Configuration

```yaml
# mkdocs.yml
site_name: My Project
site_url: https://username.github.io/my-project/

theme:
  name: material
  features:
    - navigation.sections    # Collapsible sections
    - navigation.tabs       # Top-level tabs
    - navigation.top        # Back to top button
    - search.highlight      # Highlight search terms
    - content.code.copy     # Copy code buttons

plugins:
  - search                  # Built-in search
  - mkdocstrings:          # API docs from docstrings
      handlers:
        python:
          options:
            docstring_style: numpy
            show_source: true
```

### API Documentation

The template automatically generates API documentation:

```markdown
<!-- docs/api.md -->
# API Reference

::: my_package
    options:
      show_source: true
      show_root_heading: true
      members_order: alphabetical
```

### Documentation Features

- **📝 NumPy-style docstrings**: Clear, standardized documentation
- **🔗 Auto-linking**: Automatic cross-references
- **💻 Code examples**: Syntax-highlighted code blocks
- **🎨 Admonitions**: Call-out boxes for important info
- **📊 Diagrams**: Mermaid diagram support

## Type Checking: Built-in Support 🔍

The template includes comprehensive type checking support.

### Type Annotations

Every generated file includes full type hints:

```python
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

def load_config(
    config_path: Path,
    defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Union[str, int, bool]]:
    """Load configuration from file.

    Parameters
    ----------
    config_path : Path
        Path to configuration file
    defaults : Optional[Dict[str, Any]], default=None
        Default configuration values

    Returns
    -------
    Dict[str, Union[str, int, bool]]
        Loaded configuration

    Raises
    ------
    FileNotFoundError
        If config file doesn't exist
    ValueError
        If config file is invalid
    """
```

### Runtime Type Checking

For critical applications, add runtime type checking:

```python
# Optional: Add beartype for runtime checking
from beartype import beartype

@beartype
def critical_function(data: List[int]) -> int:
    """Function with runtime type validation."""
    return sum(data)
```

### mypy Integration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Pre-commit Hooks 🪝

**[pre-commit](https://pre-commit.com/)** automatically runs quality checks before each commit.

### Why Pre-commit?

- **🛡️ Quality Gate**: Catch issues before they enter the repo
- **⚡ Fast Feedback**: Immediate feedback on code quality
- **🔄 Consistent**: Same checks for all developers
- **🎯 Configurable**: Customize checks for your needs

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### Usage

```bash
# Install hooks (done automatically in generated project)
pre-commit install

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff

# Update hook versions
pre-commit autoupdate
```

## Environment Management 🌍

The template includes comprehensive environment management.

### Virtual Environments

```bash
# Create virtual environment with uv
uv venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install project in development mode
uv pip install -e ".[dev]"
```

### Environment Variables

```bash
# .env.example (template)
PYTHONPATH=src
LOG_LEVEL=INFO
DEBUG=false

# Copy and customize
cp .env.example .env
```

### Python Version Management

The template supports modern Python versions:

```toml
# pyproject.toml
[project]
requires-python = ">=3.13"

# Support for multiple versions in CI
[tool.ruff]
target-version = "py313"
```

## IDE Integration 🔧

The template includes comprehensive IDE support.

### VS Code

Complete VS Code configuration:

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.testing.pytestEnabled": true,
    "ruff.enable": true,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

### Recommended Extensions

```json
// .vscode/extensions.json
{
    "recommendations": [
        "charliermarsh.ruff",           # Ruff linting
        "ms-python.python",            # Python support
        "ms-python.debugpy",           # Python debugging
        "yzhang.markdown-all-in-one",  # Markdown editing
        "tamasfe.even-better-toml",    # TOML support
    ]
}
```

## Performance Considerations ⚡

The chosen tools prioritize performance:

| Tool | Speed Improvement | Reason |
|------|------------------|---------|
| **uv** | 10-100x faster than pip | Rust implementation, better algorithms |
| **Ruff** | 10-100x faster than flake8 | Rust implementation, parallel processing |
| **pytest** | Baseline (already fast) | Efficient test discovery and execution |

### Benchmarks

On a typical Python project:

```bash
# Traditional stack timing
pip install: ~30s
flake8 + isort + black: ~5s
mypy: ~10s
Total: ~45s

# Modern stack timing
uv pip install: ~3s
ruff check + format: ~0.5s
mypy: ~10s
Total: ~13.5s

# 3x faster overall! 🚀
```

## Next Steps

Now that you understand the modern development stack:

1. **[Learn about quality assurance features](quality-assurance.md)**
2. **[Explore documentation features](documentation.md)**
3. **[Understand DevOps integration](devops.md)**
