#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
Initializes git repository, sets up development environment, and dynamically
configures Python versions across the project.
"""

import json
import re
import subprocess
from datetime import date
from pathlib import Path


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
        return result.returncode, result.stdout or ""
    except Exception:
        return 1, ""


def normalize_version(version_str: str) -> str | None:
    """Normalize version string to X.Y.Z format, filtering out dev/pre-releases."""
    version_str = version_str.strip()
    if not re.match(r"^\d+\.\d+\.\d+$", version_str):
        return None
    if re.search(r"[abrc]|dev", version_str, re.I):
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
    """Discover Python versions using endoflife.date API."""
    returncode, output = run_silent(["curl", "-sS", "https://endoflife.date/api/python.json"])
    if returncode != 0 or not output.strip():
        return None
    
    try:
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
    """Set up dynamic Python version configuration."""
    # Get template variable
    min_version = "{{ cookiecutter.python_version }}".strip()
    print(f"[PYTHON] Minimum Python version from template: {min_version}")
    
    # Discover available versions
    all_versions = discover_python_versions()
    matrix_versions = filter_min_versions(all_versions, min_version)
    max_version = matrix_versions[-1]
    
    # Compute tokens
    tokens = {
        "__PY_MIN__": min_version,
        "__PY_MATRIX__": json.dumps(matrix_versions),
        "__PY_MAX__": max_version,
        "__PY_SHORT__": min_version.replace(".", ""),  # For ruff target-version
        "__RELEASE_DATE__": date.today().strftime("%Y-%m-%d"),
    }
    
    # Generate Python classifiers
    classifiers = []
    for version in matrix_versions:
        classifiers.append(f'    "Programming Language :: Python :: {version}",')
    tokens["__PY_CLASSIFIERS__"] = "\n".join(classifiers)
    
    print(f"[PYTHON] Computed tokens: {tokens}")
    
    # Files to update
    target_files = [
        ".github/workflows/ci.yml",
        ".github/workflows/docs.yml", 
        ".github/workflows/publish.yml",
        "README.md",
        "pyproject.toml",
        "docs/development/changelog.md",
    ]
    
    # Replace tokens in files
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


def main():
    """Initialize the project after generation."""
    project_dir = Path.cwd()
    print(f"[INIT] Initializing project in {project_dir}")

    # Set up dynamic Python version configuration first
    setup_python_versions()

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
