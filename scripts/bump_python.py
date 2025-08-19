from __future__ import annotations

import pathlib
import re
import sys
import tomllib

import tomli_w

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"


def main() -> None:
    if "--to" not in sys.argv:
        sys.exit("Usage: bump_python.py --to MAJOR.MINOR (e.g. 3.12)")

    idx = sys.argv.index("--to")
    if idx + 1 >= len(sys.argv):
        sys.exit("Error: --to requires a value.\n"
                 "Usage: bump_python.py --to MAJOR.MINOR (e.g. 3.12)")

    to = sys.argv[idx + 1]
    if not re.fullmatch(r"\d+\.\d+", to):
        sys.exit(
            f"Error: invalid Python version '{to}'. Expected MAJOR.MINOR like 3.12"
        )

    text = PYPROJECT.read_text(encoding="utf-8")
    doc = tomllib.loads(text)
    proj = doc.setdefault("project", {})

    old = proj.get("requires-python", ">=3.10")
    new = re.sub(r">=?\s*3\.\d+", f">={to}", old) if ">=" in old else f">={to}"
    proj["requires-python"] = new

    PYPROJECT.write_text(tomli_w.dumps(doc), encoding="utf-8")
    print(f"Updated requires-python={proj['requires-python']} for {to}")


if __name__ == "__main__":
    main()
