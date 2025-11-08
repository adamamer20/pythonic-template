from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"


def _read_pyproject_text() -> str:
    return PYPROJECT.read_text(encoding="utf-8")


def parse_requires_python(spec: str) -> tuple[str, str]:
    """Parse a requires-python spec and return (min, max) minors.

    Examples:
    - ">=3.10,<3.13" -> ("3.10", "3.12")
    - ">=3.12"       -> ("3.12", "3.12")
    """
    min_m = re.search(r">=?\s*3\.(\d+)", spec)
    max_m = re.search(r"<\s*3\.(\d+)", spec)
    lo = int(min_m.group(1)) if min_m else 10
    hi = (int(max_m.group(1)) - 1) if max_m else lo
    return f"3.{lo}", f"3.{hi}"


def compute_min_max() -> tuple[str, str]:
    text = _read_pyproject_text()
    m = re.search(r"requires-python\s*=\s*\"([^\"]+)\"", text)
    spec = m.group(1) if m else ">=3.10"
    return parse_requires_python(spec)


def json_blob() -> str:
    lo, hi = compute_min_max()
    return json.dumps({"min": lo, "max": hi})
