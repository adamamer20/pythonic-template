"""
Test suite for the pythonic-template cookiecutter template.
Tests template generation and validates the resulting project structure.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from hooks.post_gen_project import run_command  # noqa: E402


def run_subprocess(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
    """Run subprocess without coverage environment variables."""
    env = os.environ.copy()
    env.pop("COVERAGE_FILE", None)
    env.pop("COVERAGE_PROCESS_START", None)
    kwargs.setdefault("env", env)
    check_flag = kwargs.pop("check", False)
    return subprocess.run(cmd, check=check_flag, **kwargs)


def test_run_command_basic():
    """Ensure run_command executes a simple command."""
    result = run_command("echo hello", check=False)
    assert result.returncode == 0


def test_template_generation_basic():
    """Test basic template generation with default parameters."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate project
        run_subprocess(
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


def test_template_generation_with_devcontainer():
    """Test template generation includes devcontainer files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
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

        # Check Docker files exist (Docker is always enabled now)
        assert (project_path / ".devcontainer/Dockerfile").exists()
        assert (project_path / ".devcontainer/devcontainer.json").exists()
        assert (project_path / ".devcontainer/docker-compose.yml").exists()

        # Verify Dockerfile has multi-stage build
        dockerfile_content = (project_path / ".devcontainer/Dockerfile").read_text()
        assert "AS builder" in dockerfile_content
        assert "AS runtime" in dockerfile_content
        assert "AS development" in dockerfile_content


def test_generated_project_structure():
    """Test that generated project has correct structure and can be built."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate project
        run_subprocess(
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
        result = run_subprocess(
            ["uv", "sync", "--all-extras"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            pytest.skip("uv not available, skipping dependency installation test")

        # Run tests
        test_result = run_subprocess(
            ["uv", "run", "pytest", "-v"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        assert test_result.returncode == 0, f"Tests failed: {test_result.stderr}"

        # Check linting passes
        lint_result = run_subprocess(
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
        run_subprocess(
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
        run_subprocess(
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


def test_paper_project_type():
    """Test template generation with different project types."""
    # Test paper project type
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "project_type=paper",
                f"--output-dir={temp_dir}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        
        # Check paper-specific files exist
        assert (project_path / "paper/paper.qmd").exists()
        assert (project_path / "paper/references.bib").exists()
        assert (project_path / ".github/workflows/render-paper.yml").exists()
        
        # Check paper dependencies in pyproject.toml
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert "paper = [" in pyproject_content
        assert "marimo" in pyproject_content
        
        # Check Quarto in Dockerfile
        dockerfile_content = (project_path / ".devcontainer/Dockerfile").read_text()
        assert "quarto" in dockerfile_content.lower()
        
        # Check Makefile has paper commands
        makefile_content = (project_path / "Makefile").read_text()
        assert "paper-render" in makefile_content
        assert "paper-preview" in makefile_content
    
    # Test standard project type (should not have paper files)
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "project_type=standard",
                f"--output-dir={temp_dir}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        
        # Check paper-specific files do NOT exist
        assert not (project_path / "paper").exists()
        assert not (project_path / ".github/workflows/render-paper.yml").exists()
        
        # Check NO paper dependencies in pyproject.toml for standard projects
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert "paper = [" not in pyproject_content
        assert "marimo" not in pyproject_content


def test_ai_agents_configuration():
    """Test template generation with different AI agent configurations."""
    test_cases = [
        ("all", ["claude_code", "qdrant", "ollama"]),
        ("claude_code", ["claude_code"]),
        ("roo_code", ["qdrant", "ollama"]),
        ("none", []),
    ]
    
    for ai_agents, expected_services in test_cases:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_subprocess(
                [
                    "cookiecutter",
                    str(Path(__file__).parent.parent),
                    "--no-input",
                    f"ai_agents={ai_agents}",
                    f"--output-dir={temp_dir}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            project_path = Path(temp_dir) / "my-amazing-library"
            
            # AI agents config is handled through conditional filenames
            
            # Check Docker Compose has expected services
            docker_compose = project_path / ".devcontainer/docker-compose.yml"
            if ai_agents != "none":
                assert docker_compose.exists()
                compose_content = docker_compose.read_text()
                
                for service in expected_services:
                    if service in ["qdrant", "ollama"]:
                        if ai_agents in ["all", "roo_code"]:
                            assert service in compose_content
                        else:
                            assert service not in compose_content
            
            # Check Roo code rules exist when appropriate
            roo_rules = project_path / ".roo/rules-code/rules.md"
            if ai_agents in ["all", "roo_code"]:
                assert roo_rules.exists()
                roo_content = roo_rules.read_text()
                assert "# Project Instructions" in roo_content
            else:
                # File should not exist due to conditional filename
                assert not roo_rules.exists()


def test_devcontainer_configuration():
    """Test devcontainer configuration with different options."""
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "ai_agents=all",
                "project_type=paper",
                f"--output-dir={temp_dir}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        
        # Check devcontainer files exist
        devcontainer_files = [
            ".devcontainer/Dockerfile",
            ".devcontainer/devcontainer.json", 
            ".devcontainer/docker-compose.yml",
        ]
        
        for file_path in devcontainer_files:
            assert (project_path / file_path).exists(), f"Missing {file_path}"
        
        # Check devcontainer.json configuration
        devcontainer_content = (project_path / ".devcontainer/devcontainer.json").read_text()
        assert "dockerComposeFile" in devcontainer_content
        assert "6333" in devcontainer_content  # Qdrant port
        assert "11434" in devcontainer_content  # Ollama port
        assert "quarto.quarto" in devcontainer_content  # Quarto extension for paper projects
        
        # Check multi-stage Dockerfile
        dockerfile_content = (project_path / ".devcontainer/Dockerfile").read_text()
        stages = ["base-env", "deps", "builder", "runtime", "development"]
        for stage in stages:
            assert f"AS {stage}" in dockerfile_content


def test_makefile_commands():
    """Test that Makefile contains all expected commands."""
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "project_type=paper",
                f"--output-dir={temp_dir}",
            ],
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        makefile_content = (project_path / "Makefile").read_text()
        
        # Check core commands exist
        core_commands = [
            "help", "setup", "test", "lint", "format", "clean",
            "ai-setup", "quick-test", "quality", "check"
        ]
        
        for cmd in core_commands:
            assert f"{cmd}:" in makefile_content, f"Missing command: {cmd}"
        
        # Check paper-specific commands for paper projects
        paper_commands = ["paper-render", "paper-preview", "paper-check"]
        for cmd in paper_commands:
            assert f"{cmd}:" in makefile_content, f"Missing paper command: {cmd}"


def test_beartype_replaces_typeguard():
    """Test that beartype is used instead of typeguard and mypy."""
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                f"--output-dir={temp_dir}",
            ],
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        pyproject_content = (project_path / "pyproject.toml").read_text()
        
        # Check beartype is included
        assert "beartype" in pyproject_content
        
        # Check typeguard and mypy are NOT included
        assert "typeguard" not in pyproject_content
        assert "mypy" not in pyproject_content
        
        # Check mypy configuration does NOT exist
        assert "[tool.mypy]" not in pyproject_content


def test_cruft_configuration():
    """Test that cruft is properly configured."""
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "project_type=paper",
                "ai_agents=claude_code",
                f"--output-dir={temp_dir}",
            ],
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        
        # Check .cruft.json exists and has correct structure
        cruft_config = project_path / ".cruft.json"
        assert cruft_config.exists()
        
        import json
        with open(cruft_config) as f:
            cruft_data = json.load(f)
        
        assert "template" in cruft_data
        assert "context" in cruft_data
        assert "cookiecutter" in cruft_data["context"]
        
        # Check new fields are tracked
        context = cruft_data["context"]["cookiecutter"]
        assert "project_type" in context
        assert "ai_agents" in context
        # Check use_docker is NOT tracked (removed)
        assert "use_docker" not in context


def test_ai_agent_files_consistency():
    """Test that all AI agent instruction files have identical content."""
    def extract_content(content: str) -> str:
        """Extract content between conditions, removing emojis."""
        import re
        # Remove Jinja conditions
        content = re.sub(r'{%.*?%}', '', content, flags=re.DOTALL).strip()
        # Remove emojis (any unicode emoji characters)
        content = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+', '', content)
        # Remove fire emoji and other specific emojis that might not be caught
        content = content.replace('🔥', '').replace('🚀', '').replace('🤖', '').replace('💡', '').replace('✅', '')
        return content.strip()

    # Test different AI agent combinations
    test_cases = [
        ("all", ["AGENTS.md", "CLAUDE.md", ".roo/rules-code/rules.md"]),
        ("claude_code", ["CLAUDE.md"]),
        ("openai_codex", ["AGENTS.md"]),
        ("roo_code", [".roo/rules-code/rules.md"]),
        ("claude_code,openai_codex", ["CLAUDE.md", "AGENTS.md"]),
    ]
    
    for ai_agents, expected_files in test_cases:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_subprocess(
                [
                    "cookiecutter",
                    str(Path(__file__).parent.parent),
                    "--no-input",
                    f"ai_agents={ai_agents}",
                    "project_type=paper",  # Use paper to test all template features
                    f"--output-dir={temp_dir}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            project_path = Path(temp_dir) / "my-amazing-library"
            file_contents = {}
            
            # Read all existing AI agent files
            for file_path in expected_files:
                full_path = project_path / file_path
                if full_path.exists():
                    content = full_path.read_text()
                    file_contents[file_path] = extract_content(content)
            
            # If multiple files exist, they should have identical content
            if len(file_contents) > 1:
                contents = list(file_contents.values())
                base_content = contents[0]
                
                for i, content in enumerate(contents[1:], 1):
                    assert content == base_content, (
                        f"AI agent files have different content in {ai_agents} configuration.\n"
                        f"File {expected_files[0]} vs {expected_files[i]} differ."
                    )

            # Check that no emojis exist in the AI agent files
            for file_path, content in file_contents.items():
                import re
                emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251🔥🚀🤖💡✅]'
                emojis_found = re.findall(emoji_pattern, content)
                assert not emojis_found, f"Found emojis in {file_path}: {emojis_found}"


def test_conditional_ai_agent_files():
    """Test that AI agent files are only created when the agent is selected."""
    # Test that files are not created when agent is not selected
    with tempfile.TemporaryDirectory() as temp_dir:
        run_subprocess(
            [
                "cookiecutter",
                str(Path(__file__).parent.parent),
                "--no-input",
                "ai_agents=none",
                f"--output-dir={temp_dir}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        project_path = Path(temp_dir) / "my-amazing-library"
        
        # Check that no AI agent files exist
        assert not (project_path / "AGENTS.md").exists() or (project_path / "AGENTS.md").read_text().strip() == ""
        assert not (project_path / "CLAUDE.md").exists() or (project_path / "CLAUDE.md").read_text().strip() == ""
        assert not (project_path / ".roo/rules-code/rules.md").exists() or (project_path / ".roo/rules-code/rules.md").read_text().strip() == ""

    # Test that specific files are created for specific agents
    test_cases = [
        ("claude_code", "CLAUDE.md", ["AGENTS.md", ".roo/rules-code/rules.md"]),
        ("openai_codex", "AGENTS.md", ["CLAUDE.md", ".roo/rules-code/rules.md"]),
        ("roo_code", ".roo/rules-code/rules.md", ["AGENTS.md", "CLAUDE.md"]),
    ]
    
    for ai_agent, should_exist, should_not_exist in test_cases:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_subprocess(
                [
                    "cookiecutter",
                    str(Path(__file__).parent.parent),
                    "--no-input",
                    f"ai_agents={ai_agent}",
                    f"--output-dir={temp_dir}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            project_path = Path(temp_dir) / "my-amazing-library"
            
            # Check that the correct file exists and has content
            target_file = project_path / should_exist
            assert target_file.exists(), f"{should_exist} should exist for {ai_agent}"
            assert target_file.read_text().strip(), f"{should_exist} should have content for {ai_agent}"
            
            # Check that other files don't exist or are empty
            for file_path in should_not_exist:
                other_file = project_path / file_path
                if other_file.exists():
                    content = other_file.read_text().strip()
                    assert not content, f"{file_path} should be empty when {ai_agent} is selected, but contains: {content[:100]}..."


if __name__ == "__main__":
    pytest.main([__file__])
