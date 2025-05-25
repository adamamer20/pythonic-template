# Testing Guide

This guide covers testing strategies and best practices for both the template itself and projects generated from it.

## Testing Philosophy

The Pythonic Template emphasizes comprehensive testing at multiple levels:

- **Template Testing:** Verify the template generates correctly
- **Generated Project Testing:** Ensure generated projects work as expected
- **Documentation Testing:** Validate that examples actually work
- **Integration Testing:** Test the complete workflow

## Template Testing

### Testing Template Generation

Test that the template generates valid projects with different configurations:

```python
import tempfile
import subprocess
from pathlib import Path
import pytest


def test_default_generation():
    """Test template generation with default values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = subprocess.run([
            "cookiecutter", 
            ".", 
            "--no-input",
            "--output-dir", temp_dir
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        project_path = Path(temp_dir) / "my-python-project"
        assert project_path.exists()
        assert (project_path / "pyproject.toml").exists()


def test_custom_configuration():
    """Test template generation with custom values."""
    config = {
        "project_name": "custom-project",
        "author_name": "Test Author",
        "python_version": "3.11"
    }
    
    # Test with custom configuration
    # Implementation here...
```

### Testing Generated Project Structure

Verify that generated projects have the expected structure:

```python
def test_project_structure():
    """Test that generated project has correct structure."""
    expected_files = [
        "pyproject.toml",
        "README.md",
        "src/my_python_project/__init__.py",
        "tests/test_main.py",
        "docs/index.md",
        ".github/workflows/ci.yml",
        ".gitignore",
        ".pre-commit-config.yaml"
    ]
    
    for file_path in expected_files:
        assert (project_path / file_path).exists()


def test_pyproject_toml_content():
    """Test that pyproject.toml has correct content."""
    pyproject_path = project_path / "pyproject.toml"
    content = pyproject_path.read_text()
    
    assert "name = \"my-python-project\"" in content
    assert "python = \">=3.13\"" in content
    assert "[tool.ruff]" in content
```

### Testing Template Variables

Test that template variables are properly substituted:

```python
@pytest.mark.parametrize("variable,value,expected_file,expected_content", [
    ("project_name", "test-project", "pyproject.toml", "name = \"test-project\""),
    ("author_name", "Jane Doe", "pyproject.toml", "Jane Doe"),
    ("python_version", "3.11", "pyproject.toml", "python = \">=3.11\""),
])
def test_template_variable_substitution(variable, value, expected_file, expected_content):
    """Test that template variables are correctly substituted."""
    # Generate project with specific variable
    # Check that the value appears in the expected file
    pass
```

## Generated Project Testing

### Testing Project Setup

Verify that generated projects can be properly set up:

```python
def test_project_setup():
    """Test that generated project can be set up."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate project
        # Navigate to project directory
        # Run setup commands
        result = subprocess.run([
            "uv", "pip", "install", "-e", ".[dev]"
        ], cwd=project_path, capture_output=True, text=True)
        
        assert result.returncode == 0
```

### Testing Development Tools

Test that all development tools work correctly:

```python
def test_ruff_configuration():
    """Test that Ruff runs without errors."""
    result = subprocess.run([
        "ruff", "check", "."
    ], cwd=project_path, capture_output=True, text=True)
    
    assert result.returncode == 0


def test_pytest_execution():
    """Test that pytest runs successfully."""
    result = subprocess.run([
        "pytest", "-v"
    ], cwd=project_path, capture_output=True, text=True)
    
    assert result.returncode == 0


def test_mypy_type_checking():
    """Test that mypy passes without errors."""
    result = subprocess.run([
        "mypy", "src"
    ], cwd=project_path, capture_output=True, text=True)
    
    assert result.returncode == 0
```

### Testing Documentation Build

Verify that documentation builds successfully:

```python
def test_documentation_build():
    """Test that MkDocs builds without errors."""
    result = subprocess.run([
        "mkdocs", "build"
    ], cwd=project_path, capture_output=True, text=True)
    
    assert result.returncode == 0
    assert (project_path / "site").exists()
```

## Testing Workflows

### Continuous Integration Testing

Test that CI workflows work correctly:

```python
def test_github_actions_syntax():
    """Test that GitHub Actions workflows have valid syntax."""
    workflow_path = project_path / ".github/workflows/ci.yml"
    
    # You can use a YAML parser to validate syntax
    import yaml
    
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)
    
    assert "jobs" in workflow
    assert "test" in workflow["jobs"]
```

### Pre-commit Hook Testing

Test that pre-commit hooks are properly configured:

```python
def test_precommit_configuration():
    """Test that pre-commit configuration is valid."""
    config_path = project_path / ".pre-commit-config.yaml"
    
    import yaml
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    assert "repos" in config
    # Check for specific hooks
    repo_urls = [repo["repo"] for repo in config["repos"]]
    assert "https://github.com/astral-sh/ruff-pre-commit" in repo_urls
```

## Test Data and Fixtures

### Creating Test Fixtures

Use pytest fixtures for reusable test data:

```python
@pytest.fixture
def generated_project():
    """Generate a test project and clean up after test."""
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run([
            "cookiecutter", 
            ".", 
            "--no-input",
            "--output-dir", temp_dir
        ])
        
        project_path = Path(temp_dir) / "my-python-project"
        yield project_path


@pytest.fixture
def project_with_dependencies(generated_project):
    """Generate project and install dependencies."""
    subprocess.run([
        "uv", "pip", "install", "-e", ".[dev]"
    ], cwd=generated_project)
    
    return generated_project
```

### Parameterized Testing

Test multiple configurations efficiently:

```python
@pytest.mark.parametrize("config", [
    {"python_version": "3.11", "use_docker": "y"},
    {"python_version": "3.12", "use_docker": "n"},
    {"python_version": "3.13", "use_docker": "y"},
])
def test_different_configurations(config):
    """Test template with different configurations."""
    # Generate and test project with specific config
    pass
```

## Performance Testing

### Template Generation Performance

Test that template generation is reasonably fast:

```python
import time

def test_generation_performance():
    """Test that template generation completes quickly."""
    start_time = time.time()
    
    # Generate project
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run([
            "cookiecutter", 
            ".", 
            "--no-input",
            "--output-dir", temp_dir
        ])
    
    duration = time.time() - start_time
    assert duration < 10  # Should complete in under 10 seconds
```

## Testing Best Practices

### Test Organization

- **Group related tests** in the same file
- **Use descriptive test names** that explain what's being tested
- **Keep tests independent** - each test should work in isolation
- **Use fixtures** for common setup and teardown

### Test Coverage

Aim for high test coverage while focusing on critical paths:

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Mocking and Test Doubles

Use mocking sparingly and only when necessary:

```python
from unittest.mock import patch, MagicMock

def test_external_dependency():
    """Test behavior when external service is unavailable."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        # Test error handling
```

### Property-Based Testing

Consider using hypothesis for property-based testing:

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=50))
def test_project_name_validation(project_name):
    """Test project name validation with various inputs."""
    # Test that project name validation works correctly
    pass
```

## Integration Testing

### End-to-End Workflow Testing

Test the complete workflow from template generation to project deployment:

```python
def test_complete_workflow():
    """Test the complete development workflow."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Generate project
        # 2. Install dependencies
        # 3. Run linting
        # 4. Run tests
        # 5. Build documentation
        # 6. Build package
        pass
```

### Cross-Platform Testing

Test on different operating systems and Python versions:

```python
@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_windows_compatibility():
    """Test that template works on Windows."""
    pass


@pytest.mark.skipif(sys.platform != "linux", reason="Linux-specific test")
def test_linux_compatibility():
    """Test that template works on Linux."""
    pass
```

## Debugging Tests

### Running Specific Tests

```bash
# Run a specific test
pytest tests/test_template.py::test_default_generation

# Run tests matching a pattern
pytest -k "test_generation"

# Run with detailed output
pytest -v -s
```

### Debugging Failed Tests

```bash
# Drop into debugger on failure
pytest --pdb

# Show local variables in traceback
pytest --tb=long

# Capture output
pytest -s --capture=no
```

## Continuous Testing

### Test Automation

Set up automated testing for:

- **Pull requests** - Run full test suite
- **Scheduled runs** - Test with latest dependencies
- **Release preparation** - Comprehensive testing

### Test Environments

Test in environments that match production:

- **Multiple Python versions** (3.11, 3.12, 3.13)
- **Different operating systems** (Linux, macOS, Windows)
- **Various dependency versions**

### Performance Monitoring

Monitor test performance over time:

```bash
# Run tests with timing information
pytest --durations=10

# Profile test execution
pytest --profile
```

This comprehensive testing approach ensures that the Pythonic Template generates reliable, high-quality Python projects that follow best practices and work correctly across different environments.
