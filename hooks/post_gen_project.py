#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
Initializes git repository, sets up development environment, and dynamically
configures Python versions across the project.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
import hashlib


def run_command(
    cmd: str, check: bool = True, shell: bool = True
) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=shell, check=check, capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            raise
        return e


def run_silent(cmd: list[str]) -> tuple[int, str]:
    """Run command silently and return (returncode, stdout)."""
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if result.returncode != 0 and result.stderr:
            print(f"[DEBUG] Command failed: {' '.join(cmd)}\n{result.stderr}")
        return result.returncode, result.stdout or ""
    except Exception:
        return 1, ""


def normalize_version(version_str: str) -> str | None:
    """Normalize version string to X.Y.Z format."""
    version_str = version_str.strip()
    if not re.match(r"^\d+\.\d+\.\d+$", version_str):
        return None
    return version_str


def get_unique_minors(stable_versions: list[str]) -> list[str]:
    """Extract unique minor versions (X.Y) from stable versions, keeping latest patch."""
    best_versions = {}
    for version in stable_versions:
        major, minor, patch = map(int, version.split("."))
        key = f"{major}.{minor}"
        if key not in best_versions or (major, minor, patch) > best_versions[key]:
            best_versions[key] = (major, minor, patch)

    return sorted(best_versions.keys(), key=lambda x: tuple(map(int, x.split("."))))


def filter_min_versions(minors: list[str], required_min: str) -> list[str]:
    """Filter versions to only include those >= required minimum."""
    min_tuple = tuple(map(int, required_min.split(".")))
    filtered = [
        version for version in minors
        if tuple(map(int, version.split("."))) >= min_tuple
    ]
    return filtered or [required_min]


def discover_from_uv() -> list[str] | None:
    """Discover Python versions using uv."""
    returncode, output = run_silent(["uv", "python", "list", "--releases", "--format", "json"])
    if returncode != 0:
        return None

    try:
        data = json.loads(output)
    except Exception:
        return None

    stable_versions = []
    for entry in data:
        if entry.get("implementation") == "cpython":
            version = normalize_version(entry.get("version", ""))
            if version:
                stable_versions.append(version)

    return get_unique_minors(stable_versions) if stable_versions else None


def discover_from_pyenv() -> list[str] | None:
    """Discover Python versions using pyenv."""
    returncode, output = run_silent(["pyenv", "install", "-l"])
    if returncode != 0 or not output.strip():
        return None

    stable_versions = []
    for line in output.splitlines():
        version = normalize_version(line.strip())
        if version:
            stable_versions.append(version)

    return get_unique_minors(stable_versions) if stable_versions else None


def discover_from_endoflife() -> list[str] | None:
    """Discover Python versions using endoflife.date API (stdlib only)."""
    try:
        import urllib.request  # noqa: WPS433 (stdlib import inside function for portability)
        with urllib.request.urlopen("https://endoflife.date/api/python.json", timeout=5) as resp:
            output = resp.read().decode("utf-8")
        if not output.strip():
            return None
        data = json.loads(output)
    except Exception:
        return None

    stable_versions = []
    for entry in data:
        # Try latest version first
        latest = entry.get("latest", "")
        version = normalize_version(latest)
        if version:
            stable_versions.append(version)
        else:
            # Fallback to cycle.0 if latest is not parseable
            cycle = entry.get("cycle", "")
            if re.match(r"^\d+\.\d+$", cycle):
                stable_versions.append(f"{cycle}.0")

    return get_unique_minors(stable_versions) if stable_versions else None


def discover_python_versions() -> list[str]:
    """Discover available Python versions, falling back through multiple methods."""
    print("[PYTHON] Discovering available Python versions...")

    for method_name, method_func in [
        ("uv", discover_from_uv),
        ("pyenv", discover_from_pyenv),
        ("endoflife.date", discover_from_endoflife),
    ]:
        try:
            print(f"[PYTHON] Trying {method_name}...")
            versions = method_func()
            if versions:
                print(f"[PYTHON] Found versions via {method_name}: {versions}")
                return versions
        except Exception as e:
            print(f"[PYTHON] {method_name} failed: {e}")

    # Fallback to reasonable defaults
    fallback = ["3.12", "3.13", "3.14"]
    print(f"[PYTHON] Using fallback versions: {fallback}")
    return fallback


def setup_python_versions():
    """Set up Python version tokens using shared logic."""
    # Ensure we can import from generated project's scripts/lib
    proj_root = Path.cwd()
    lib_dir = proj_root / "scripts" / "lib"
    if lib_dir.exists():
        sys.path.insert(0, str(lib_dir.parent))  # add 'scripts' to path

    try:
        from scripts.lib.python_versions import parse_requires_python  # type: ignore
    except Exception:
        # Fallback: minimal local implementation (should rarely be needed)
        def parse_requires_python(spec: str):  # type: ignore
            m1 = re.search(r">=?\s*3\.(\d+)", spec)
            m2 = re.search(r"<\s*3\.(\d+)", spec)
            lo = int(m1.group(1)) if m1 else 12
            hi = (int(m2.group(1)) - 1) if m2 else lo
            return f"3.{lo}", f"3.{hi}"

    # Get min from template context
    min_version = "{{ cookiecutter.python_version }}".strip()
    print(f"[PYTHON] Minimum Python version from template: {min_version}")

    lo, hi = parse_requires_python(f">={min_version}")
    matrix_versions = [lo] if lo == hi else [lo, hi]
    max_version = hi

    tokens = {
        "__PY_MIN__": lo,
        "__PY_MATRIX__": json.dumps(matrix_versions),
        "__PY_MAX__": max_version,
        "__PY_SHORT__": lo.replace(".", ""),
        "__RELEASE_DATE__": date.today().strftime("%Y-%m-%d"),
    }

    classifiers = [f'    "Programming Language :: Python :: {v}",' for v in matrix_versions]
    tokens["__PY_CLASSIFIERS__"] = "\n".join(classifiers)

    print(f"[PYTHON] Computed tokens: {tokens}")

    target_files = [
        ".github/workflows/ci.yml",
        ".github/workflows/docs.yml",
        ".github/workflows/publish.yml",
        ".github/workflows/render-paper.yml",
        "README.md",
        "pyproject.toml",
        "docs/development/changelog.md",
        "docs/development/contributing.md",
    ]

    project_root = Path.cwd()
    for file_path in target_files:
        full_path = project_root / file_path
        if not full_path.exists():
            continue

        content = full_path.read_text(encoding="utf-8")
        original_content = content

        for token, replacement in tokens.items():
            content = content.replace(token, replacement)

        if content != original_content:
            full_path.write_text(content, encoding="utf-8")
            print(f"[PYTHON] Updated {file_path} with Python version tokens")

    print("[PYTHON] Python version setup completed!")


def _run_command(cmd: list[str], cwd: str | None = None) -> str | None:
    """Run a command and return stdout if successful, None otherwise."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, check=False, capture_output=True, text=True
        )
        return result.stdout.strip() if result.returncode == 0 and result.stdout else None
    except Exception:
        return None


def setup_cruft_tracking():
    """Populate .cruft.json 'commit' deterministically without altering 'template'."""
    cruft_path = Path.cwd() / ".cruft.json"
    if not cruft_path.exists():
        print("[CRUFT] No .cruft.json found; skipping")
        return

    try:
        # Load and parse .cruft.json safely
        data = json.loads(cruft_path.read_text(encoding="utf-8"))

        # If already set, leave it alone (idempotent)
        if data.get("commit"):
            print(f"[CRUFT] Commit already set: {data['commit'][:8]}")
            return

        template = data.get("template", "")
        known_commit = None

        # Prefer explicit environment-provided commit hashes (offline friendly)
        for env_var in ("COOKIECUTTER_TEMPLATE_COMMIT", "GITHUB_SHA"):
            val = os.environ.get(env_var)
            if val and re.fullmatch(r"[0-9a-f]{40}", val):
                known_commit = val
                print(f"[CRUFT] Using commit from env {env_var}: {val[:8]}")
                break

        # Method 1: If template is a local path, try to get its commit
        if not known_commit and template and Path(template).exists() and (Path(template) / ".git").exists():
            known_commit = _run_command(["git", "rev-parse", "HEAD"], cwd=template)
            if known_commit:
                print(f"[CRUFT] Found commit from template path: {template}")

        # Method 2: If template is a remote URL and no env override, try git ls-remote
        if not known_commit and isinstance(template, str) and template.startswith(("http://", "https://", "git@", "git://")):
            remote_output = _run_command(["git", "ls-remote", template, "HEAD"])
            if remote_output:
                known_commit = remote_output.split()[0]
                print(f"[CRUFT] Found commit from remote template: {template}")

        # Method 3: Last-ditch local probing (without persisting paths)
        if not known_commit:
            probes = [
                Path("..") / "pythonic-template",
                Path.home() / "pythonic-template",
            ]
            if isinstance(template, str) and template.startswith("https://github.com"):
                repo_name = template.rstrip("/").split("/")[-1]
                if repo_name:
                    probes.append(Path.home() / repo_name)
            for probe in probes:
                if probe and (probe / ".git").exists():
                    sha = _run_command(["git", "rev-parse", "HEAD"], cwd=str(probe))
                    if sha:
                        known_commit = sha
                        print(f"[CRUFT] Found local template at {probe} (not persisted in .cruft.json)")
                        break

        if not known_commit:
            # Offline-friendly deterministic fallback: hash the template URL/path
            basis = template if isinstance(template, str) and template else "pythonic-template"
            known_commit = hashlib.sha1(basis.encode("utf-8")).hexdigest()
            print("[CRUFT] Could not resolve template commit; using synthetic SHA")

        # Update only the commit field, preserving template URL
        data["commit"] = known_commit
        cruft_path.write_text(json.dumps(data, indent=4), encoding="utf-8")
        print(f"[CRUFT] Updated .cruft.json with commit: {known_commit[:8]}")

    except (json.JSONDecodeError, OSError) as e:
        print(f"[CRUFT] Failed to set up cruft tracking: {e}")


def main():
    """Initialize the project after generation."""
    project_dir = Path.cwd()
    print(f"[INIT] Initializing project in {project_dir}")

    # Set up dynamic Python version configuration first
    setup_python_versions()

    # Set up cruft tracking
    setup_cruft_tracking()

    # Clean up any placeholder files or directories left from template rendering
    for path in project_dir.rglob("__remove__*"):
        if path.is_dir():
            import shutil
            shutil.rmtree(path)
        else:
            path.unlink()

    # Initialize git repository
    try:
        run_command("git init -b main")
        print("[OK] Git repository initialized")
    except subprocess.CalledProcessError:
        print("[WARN] Git initialization failed - you may need to install git")

    # Check if uv is available, install if not
    uv_available = False
    try:
        run_command("uv --version")
        uv_available = True
        print("[OK] uv package manager detected")
    except subprocess.CalledProcessError:
        print("[INSTALL] Installing uv package manager...")
        try:
            # Install uv via pipx
            run_command("pip install --user pipx")
            run_command("pipx install uv")
            uv_available = True
            print("[OK] uv installed successfully")
        except subprocess.CalledProcessError:
            print("[WARN] uv installation failed - falling back to pip")

    # Sync dependencies and install pre-commit
    try:
        if uv_available:
            print("[INSTALL] Syncing dependencies with uv...")
            run_command("uv sync --all-extras")
            run_command("uv tool install pre-commit")
        else:
            print("[INSTALL] Installing dependencies with pip...")
            run_command("pip install -e .[dev]")
            run_command("pip install pre-commit")

        run_command("pre-commit install")
        print("[OK] Pre-commit hooks installed")
    except subprocess.CalledProcessError:
        print("[WARN] Dependency installation failed")

    # Create initial commit
    try:
        run_command("git add .")
        try:
            run_command(
                'git commit -m "Initial commit from cookiecutter template"', check=False
            )
            print("[OK] Initial commit created")
        except subprocess.CalledProcessError:
            # Pre-commit might modify files and fail the commit
            print("[WARN] Initial commit attempt with pre-commit failed, retrying...")
            run_command("git add .")
            run_command(
                'git commit -m "Initial commit from cookiecutter template"', check=False
            )
    except subprocess.CalledProcessError:
        print("[WARN] Initial commit failed")

    print("\n[SUCCESS] Project successfully initialized!")
    print("\nNext steps:")
    print("1. Run tests:")
    print("   pytest")

    print("2. Start developing!")
    print("   # Your code goes in src/{{ cookiecutter.package_name }}/")

    # Docker setup (always enabled)
    print("\n[DOCKER] Docker development environment is available")
    print("   Use VS Code's dev container extension or run:")
    print("   docker compose -f .devcontainer/docker-compose.yml up -d")


if __name__ == "__main__":
    main()
