# {{ cookiecutter.project_name }}

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/workflows/CI/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/actions/workflows/ci.yml)
[![Documentation](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/workflows/Documentation/badge.svg)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.repo_name }}/)
[![PyPI version](https://badge.fury.io/py/{{ cookiecutter.package_name }}.svg)](https://badge.fury.io/py/{{ cookiecutter.package_name }})
[![Python versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.package_name }}.svg)](https://pypi.org/project/{{ cookiecutter.package_name }}/)
{%- if cookiecutter.license == "MIT" %}
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
{%- elif cookiecutter.license == "Apache-2.0" %}
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
{%- elif cookiecutter.license == "BSD-3-Clause" %}
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
{%- endif %}

{{ cookiecutter.project_short_description }}

## Features

- ✨ **Modern Python**: Built with Python 3.9+ support
- 🚀 **Fast Development**: Powered by `uv` package manager
- 🛡️ **Type Safe**: Full type hints with runtime validation via `beartype`
- 🧪 **Well Tested**: Comprehensive test suite with pytest
- 📚 **Documentation**: Beautiful docs with Material for MkDocs
- 🔧 **Developer Experience**: Pre-commit hooks, automated formatting, and linting
- 🏗️ **CI/CD Ready**: GitHub Actions workflows for testing, building, and publishing

## Installation

Install from PyPI:

```bash
pip install {{ cookiecutter.package_name }}
```

Or with `uv`:

```bash
uv add {{ cookiecutter.package_name }}
```

## Quick Start

```python
import {{ cookiecutter.package_name }}

# Your code here
print(f"{{ cookiecutter.project_name }} version: {{ "{" }}{{ cookiecutter.package_name }}.__version__{{ "}" }}")
```

## Development

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}.git
   cd {{ cookiecutter.repo_name }}
   ```

2. Install dependencies:
   ```bash
   uv pip install -e .[dev]
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Development Commands

```bash
# Run tests
pytest

# Run tests with type checking
DEV_TYPECHECK=1 pytest

# Run linting and formatting
ruff check .
ruff format .

# Run pre-commit on all files
pre-commit run --all-files

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### Environment Variables

Create a `.env` file based on `.env.example`:

- `DEV_TYPECHECK=1`: Enable enhanced type validation for beartype
- `LOG_LEVEL=INFO`: Set logging level

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.repo_name }}/development/contributing/) for details.

## License

This project is licensed under the {{ cookiecutter.license }} License. See the [LICENSE](LICENSE) file for details.

## Links

- [Documentation](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.repo_name }}/)
- [PyPI Package](https://pypi.org/project/{{ cookiecutter.package_name }}/)
- [Source Code](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }})
- [Issue Tracker](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/issues)
