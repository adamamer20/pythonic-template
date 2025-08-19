#!/usr/bin/env python3
"""
Validate template invariants that are easy to break:

- GitHub Actions workflow files in the template must wrap GitHub expressions
  (`${{ ... }}`) in Jinja `{% raw %}...{% endraw %}` blocks so Cookiecutter does
  not try to render them and YAML parsers don't choke.
- README in the template must use `__PY_MIN__` (double-underscore token) and not
  the bare `PY_MIN` string which will not be replaced by post-gen hooks.

Exit with non-zero if any violations are found.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "{{cookiecutter.repo_name}}"


def _workflow_files() -> list[Path]:
    """Return sorted list of workflow files with .yml and .yaml extensions."""
    workflows_dir = TEMPLATE_ROOT / ".github" / "workflows"
    files = set(workflows_dir.glob("*.yml")) | set(workflows_dir.glob("*.yaml"))
    return sorted(files, key=lambda p: p.name)


def check_workflows_raw_wrapping() -> list[str]:
    errors: list[str] = []
    for yml in _workflow_files():
        in_raw = False
        for lineno, line in enumerate(yml.read_text(encoding="utf-8").splitlines(), 1):
            if "{% raw %}" in line:
                in_raw = True
            if "{% endraw %}" in line:
                in_raw = False
            if "${{" in line and not in_raw:
                errors.append(
                    f"{yml}: line {lineno}: `${{` must be inside Jinja raw block"
                )
    return errors


def check_readme_py_min_token() -> list[str]:
    errors: list[str] = []
    readme = TEMPLATE_ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        # flag bare PY_MIN not wrapped with underscores
        if re.search(r"(?<!_)\bPY_MIN\b(?!_)", text):
            errors.append(f"{readme}: use __PY_MIN__ token, not bare PY_MIN")
    return errors


def check_template_workflows_are_valid_yaml() -> list[str]:
    errors: list[str] = []
    for yml in _workflow_files():
        try:
            yaml.safe_load(yml.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{yml}: invalid YAML: {e}")
    return errors


def main() -> int:
    violations = []
    violations += check_workflows_raw_wrapping()
    violations += check_readme_py_min_token()
    violations += check_template_workflows_are_valid_yaml()

    if violations:
        print("Template validation failed:")
        for msg in violations:
            print("- ", msg)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
