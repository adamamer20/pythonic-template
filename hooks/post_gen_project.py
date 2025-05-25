#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
Initializes git repository and sets up development environment.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, check: bool = True, shell: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            capture_output=True,
            text=True
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
    print(f"🚀 Initializing project in {project_dir}")
    
    # Initialize git repository
    try:
        run_command("git init -b main")
        print("✅ Git repository initialized")
    except subprocess.CalledProcessError:
        print("⚠️  Git initialization failed - you may need to install git")
    
    # Check if uv is available
    uv_available = False
    try:
        run_command("uv --version")
        uv_available = True
        print("✅ uv package manager detected")
    except subprocess.CalledProcessError:
        print("⚠️  uv not found - you may want to install it for faster package management")
        print("   Installation: curl -LsSf https://astral.sh/uv/install.sh | sh")
    
    # Install pre-commit if available
    try:
        if uv_available:
            run_command("uv tool install pre-commit")
        else:
            run_command("pip install pre-commit")
        
        run_command("pre-commit install")
        print("✅ Pre-commit hooks installed")
    except subprocess.CalledProcessError:
        print("⚠️  Pre-commit installation failed")
    
    # Create initial commit
    try:
        run_command("git add .")
        try:
            run_command('git commit -m "Initial commit from cookiecutter template"', check=False)
            print("✅ Initial commit created")
        except subprocess.CalledProcessError:
            # Pre-commit might modify files and fail the commit
            print("⚠️  Initial commit attempt with pre-commit failed, retrying...")
            run_command("git add .")
            run_command('git commit -m "Initial commit from cookiecutter template"', check=False)
    except subprocess.CalledProcessError:
        print("⚠️  Initial commit failed")
    
    print("\n🎉 Project successfully initialized!")
    print("\nNext steps:")
    print("1. Install development dependencies:")
    if uv_available:
        print("   uv pip install -e .[dev]")
    else:
        print("   pip install -e .[dev]")
    
    print("2. Set up your environment:")
    print("   cp .env.example .env")
    print("   # Edit .env with your settings")
    
    print("3. Run tests:")
    print("   pytest")
    
    print("4. Start developing!")
    print("   # Your code goes in src/{{ cookiecutter.package_name }}/")
    
    # Optional Docker setup
    use_docker = "{{ cookiecutter.use_docker }}" == "y"
    if use_docker:
        print("\n🐳 Docker support was enabled")
        print("   You can build the development container with:")
        print("   docker build -t {{ cookiecutter.repo_name }}-dev .")


if __name__ == "__main__":
    main()
