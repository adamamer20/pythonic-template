# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Installation

You can install `{{ cookiecutter.package_name }}` from PyPI:

```bash
pip install {{ cookiecutter.package_name }}
```

For development installation:

```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}.git
cd {{ cookiecutter.repo_name }}
uv pip install -e .[dev]
```

## Quick Start

```python
import {{ cookiecutter.package_name }}

print({{ cookiecutter.package_name }}.__version__)
```

## Features

- ✨ Modern Python package structure
- 🔧 Automated testing and CI/CD
- 📚 Beautiful documentation with Material for MkDocs
- 🛡️ Type checking with runtime validation
- 🚀 Fast development with uv package manager

## License

This project is licensed under the {{ cookiecutter.license }} License.
