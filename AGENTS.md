# Project Instructions

This file summarizes coding and project guidelines. Apply it to this template and any projects generated from it.

## Project Generation

1. Install `cookiecutter` via `uv tool install cookiecutter`.
2. Generate a project:

   ```bash
   cookiecutter https://github.com/adamamer20/pythonic-template
```

3. Enter the new project directory and install dependencies:

   ```bash
   uv sync --all-extras
   ```


Keep a copy of this file in child projects so these rules apply everywhere.
## Philosophy and General Principles

- Prefer clarity over cleverness.
- Keep a single type per variable.
- Use PEP 484/695 type hints throughout.
- Write small, modular functions and avoid duplication.
- Do not hard-code paths, GPUs or URLs; read from environment variables.
- Inline comments should explain why, and stay under 80 characters.

## Environment and Tooling

- Manage dependencies with `uv`; let it handle lockfiles.
- Assume Pop OS 24.04 and CUDA 12 on an RTX 3090. If CUDA is missing, raise an error.
- Load configuration from `.env` or `pyproject.toml`.
- Enforce formatting and linting with ruff via pre-commit.
### Common uv commands
- `uv run <package>` runs a package from the current environment.
- `uv add <package>` adds a dependency and updates the lockfile.
- `uv remove <package>` removes a dependency and updates the lockfile.

## Testing and Continuous Integration

- Follow test-driven development using pytest.
- A GitHub Actions workflow should install dependencies with `uv pip install -e .[dev]`, run pre-commit, and execute `pytest -q`.
- Enable pre-commit.ci for automatic lint fixes on pull requests.

## Data and Performance

- Use polars instead of pandas when possible.
- Vectorise heavy numerical work with numpy; benchmark loops before keeping them.
- Provide small matplotlib helper functions for plots.

## Documentation and Structure

- Control the public API with explicit `__all__` exports.
- Write NumPy-style docstrings with parameters, returns, raises and examples.
- Keep examples small and runnable with `pytest -q`.
- Use argparse for CLI interfaces and add a `--help` option.
- Place imports at the top of each file.

## Safety and Best Practices

- Avoid `eval` and `exec`; use parameterised queries for SQL.
- Keep secrets in environment variables.
- Add a module-level logger with configurable log format.

## Extras

- Use `dataclasses.dataclass(slots=True, frozen=False)` or `pydantic.BaseModel` v2 for configuration.
- Provide a Makefile or `tasks.py` with targets such as `test`, `lint` and `ci`.
