# Repository Guidelines

## Project Structure & Module Organization
- Template root contains template logic and tests: `hooks/`, `tests/`, `docs/`, `.github/`, `scripts/`, and `cookiecutter.json`.
- The rendered project lives under `{{cookiecutter.repo_name}}/` and shows the final layout (e.g., `src/{{cookiecutter.package_name}}/`, `tests/`, `docs/`, `.devcontainer/`).
- Edit template files (including Jinja tokens) in place; do not resolve `{{ ... }}` placeholders in the template repository.

## Build, Test, and Development Commands
- `uv sync --all-extras`: Create/update the dev environment for this repo.
- `uv run pytest -q`: Run the template’s test suite.
- `uv run ruff check .` / `uv run ruff format`: Lint and format code.
- `uv run pre-commit run --all-files`: Run all hooks locally.
- `uv run mkdocs serve -a 127.0.0.1:8000`: Preview docs from `docs/`.

## Coding Style & Naming Conventions
- Python 3.12+, 4‑space indentation, line length 88, double quotes (Ruff formatter enforced).
- Fully typed public APIs; use NumPy‑style docstrings.
- Naming: `snake_case` for modules/functions, `PascalCase` for classes, `CONSTANT_CASE` for constants.
- Keep template logic minimal and readable; prefer small, composable Jinja blocks.

## Testing Guidelines
- Framework: `pytest` (+ `pytest-cov`). Tests live in `tests/` and follow `test_*.py` naming.
- Add tests for new template features (e.g., new prompts, files, or flags). Include generation tests that run `cookiecutter . --no-input ...` and validate outputs.
- Aim to keep or improve coverage. Run: `uv run pytest -q --cov`.

## Commit & Pull Request Guidelines
- Use Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, etc.).
- Before pushing: `uv run ruff format && uv run ruff check . && uv run pre-commit run --all-files && uv run pytest`.
- PRs must include: clear description, rationale, linked issues, testing notes, and docs/README updates when applicable.

## Agent-Specific Tips
- Keep patches focused and minimal; avoid template‑wide reformatting.
- Never replace or hard‑code Jinja tokens (e.g., `{{cookiecutter.*}}`).
- Prefer editing the template under `{{cookiecutter.repo_name}}/` when changing generated output.
- Validate changes by running tests and, if needed, manually generating a sample project.
