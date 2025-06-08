"""
Test suite for the pythonic-template cookiecutter template.
Tests template generation and validates the resulting project structure.
"""

import subprocess
import tempfile
from pathlib import Path

import pytest


def test_template_generation_basic():
    """Test basic template generation with default parameters."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate project
        subprocess.run(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                f"--output-dir={temp_dir}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        assert project_path.exists()

        # Check essential files exist
        essential_files = [
            "pyproject.toml",
            "README.md",
            "LICENSE",
            "src/my_amazing_library/__init__.py",
            "tests/test_sample.py",
            ".gitignore",
            ".pre-commit-config.yaml",
            "Makefile",
        ]

        for file_path in essential_files:
            assert (project_path / file_path).exists(), f"Missing {file_path}"


def test_template_generation_with_docker():
    """Test template generation with Docker enabled."""
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "use_docker=y",
                f"--output-dir={temp_dir}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"

        # Check Docker files exist
        assert (project_path / "Dockerfile").exists()
        assert (project_path / ".devcontainer/devcontainer.json").exists()

        # Verify Dockerfile has multi-stage build
        dockerfile_content = (project_path / "Dockerfile").read_text()
        assert "as builder" in dockerfile_content
        assert "as runtime" in dockerfile_content
        assert "as development" in dockerfile_content


def test_generated_project_structure():
    """Test that generated project has correct structure and can be built."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate project
        subprocess.run(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                f"--output-dir={temp_dir}",
            ],
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"

        # Test that the project can be installed and tested
        result = subprocess.run(
            ["uv", "sync", "--all-extras"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            pytest.skip("uv not available, skipping dependency installation test")

        # Run tests
        test_result = subprocess.run(
            ["uv", "run", "pytest", "-v"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        assert test_result.returncode == 0, f"Tests failed: {test_result.stderr}"

        # Check linting passes
        lint_result = subprocess.run(
            ["uv", "run", "ruff", "check", "."],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        assert lint_result.returncode == 0, f"Linting failed: {lint_result.stderr}"


def test_pyproject_toml_validity():
    """Test that generated pyproject.toml is valid."""
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                f"--output-dir={temp_dir}",
            ],
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        pyproject_path = project_path / "pyproject.toml"

        # Test that pyproject.toml can be parsed
        import tomllib

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        # Check required sections exist
        assert "project" in pyproject
        assert "build-system" in pyproject
        assert "tool" in pyproject
        assert "ruff" in pyproject["tool"]
        assert "pytest" in pyproject["tool"]
        assert "hatch" in pyproject["tool"]

        # Check project metadata
        project = pyproject["project"]
        assert project["name"] == "my_amazing_library"  # Package name is normalized
        assert project["requires-python"] == ">=3.9"
        assert "dependency-groups" in pyproject
        assert "dev" in pyproject["dependency-groups"]


def test_custom_parameters():
    """Test template generation with custom parameters."""
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "project_name=Custom Project",
                "author_name=Test Author",
                "author_email=test@example.com",
                "python_version=3.11",
                f"--output-dir={temp_dir}",
            ],
            check=True,
        )

        project_path = Path(temp_dir) / "custom-project"
        assert project_path.exists()

        # Check customizations are applied
        pyproject_path = project_path / "pyproject.toml"
        content = pyproject_path.read_text()

        assert "custom-project" in content
        assert "Test Author" in content
        assert "test@example.com" in content


if __name__ == "__main__":
    pytest.main([__file__])
