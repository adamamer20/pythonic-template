## Daily Commands

Use the Makefile for all tasks — it is the single source of truth for development.

| Command                         | Description                       |
| ------------------------------- | --------------------------------- |
| `make help`                     | List all available commands       |
| `make setup`                    | One-time environment setup        |
| `make dev`                      | Start the development environment |
| `make check`                    | Run all quality checks and tests  |
| `make test` / `make quick-test` | Run the full or fast test suite   |
| `make format` / `make lint`     | Format and lint the code          |
| `make sync` / `make upgrade`    | Sync or upgrade dependencies      |
| `make clean`                    | Remove build artifacts            |

## Philosophy

* Prefer clarity over cleverness.
* Keep a single, stable type per variable.
* Use full PEP 484/695 type hints.
* Write small, modular, reusable functions.
* Never hard-code paths, GPUs, or URLs — always read from environment variables.
* Inline comments should explain *why*, not *what* (keep lines under 80 characters).

## Environment and Tooling

* Dependency management: **uv** (handles lockfiles).
* Formatting and linting: **ruff** via **pre-commit**.
* Runtime type checking: **beartype** (no mypy required).
* Configuration: load from `.env` and/or `pyproject.toml`.
* Use Fish shell if available.
* Prefer `pathlib` over `os.path`; keep imports at the top of files.

**Direct `uv` commands (when Make doesn’t cover it):**

```bash
uv add <package>      # Add dependency and update lockfile
uv remove <package>   # Remove dependency and update lockfile
uv run <command>      # Run a command within the project environment
```

## Testing and Continuous Integration

* Use **pytest** and follow test-driven development when practical.
* Coverage reports: `make test-cov`.
* Local CI pipeline: `make ci` (mirrors GitHub Actions).
* GitHub Actions runs:

  ```bash
  uv sync --all-extras --dev
  make check
  ```
* Enable **pre-commit.ci** to automatically fix linting issues on pull requests.

## Data and Performance

* Prefer **Polars** over Pandas.
* Vectorize heavy numerical work with Polars; fall back to NumPy only if necessary.
* Benchmark before keeping explicit loops.


## Code Style and Structure

* Control the public API with explicit `__all__`.
* Write NumPy-style docstrings including *Parameters*, *Returns*, *Raises*, and *Examples*.
* Keep examples minimal and runnable with `pytest -q`.
* Use `argparse` for CLI tools and always include a `--help` option.
* Avoid global state and implicit side effects.

## Safety and Logging

* Never use `eval` or `exec`.
* Use parameterized SQL queries.
* Store secrets in environment variables only.
* Each module should define a logger with configurable level and format.

## Configuration Models

* Prefer `@dataclass(slots=True)` for lightweight configuration objects.
* Use `pydantic.BaseModel` v2 for validated and coercive models.

## Development Containers

* Multi-stage Dockerfile: development, builder, and runtime stages.
* Docker Compose for service orchestration.
* VS Code devcontainer with recommended extensions and settings.
* Support for port forwarding for development servers and AI services.
