"""
{{ cookiecutter.project_name }}: {{ cookiecutter.project_short_description }}
"""

import os
from importlib import metadata as _metadata

__all__ = ["__version__"]

try:
    __version__: str = _metadata.version(__name__)
except _metadata.PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0+dev"

# -- Development-only runtime type-checking ------------------------------
if os.getenv("DEV_TYPECHECK", "0") == "1":
    from beartype.claw import beartype_this_package

    beartype_this_package()  # Enforce type hints across entire package
# ------------------------------------------------------------------------
