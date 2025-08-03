#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
Initializes git repository and sets up development environment.
"""

import subprocess
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


def main():
    """Initialize the project after generation."""
    project_dir = Path.cwd()
    print(f"[INIT] Initializing project in {project_dir}")

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
