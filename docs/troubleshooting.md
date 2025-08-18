# Troubleshooting Guide

This guide helps you resolve common issues when using the Pythonic Template.

## Installation Issues

### Cookiecutter Not Found

**Error:**
```bash
cookiecutter: command not found
```

**Solution:**
```bash
# Install cookiecutter
pip install cookiecutter

# Or with conda
conda install -c conda-forge cookiecutter

# Or with brew (macOS)
brew install cookiecutter
```

### Python Version Issues

**Error:**
```bash
Python {{ cookiecutter.python_version }}+ is required but Python 3.10 found
```

**Solution:**
```bash
# Install Python {{ cookiecutter.python_version }} with pyenv
pyenv install {{ cookiecutter.python_version }}.0
pyenv global {{ cookiecutter.python_version }}.0

# Or with conda
conda install python={{ cookiecutter.python_version }}

# Verify version
python --version
```

### UV Installation Problems

**Error:**
```bash
uv: command not found
```

**Solution:**
```bash
# Install UV
pip install uv

# Or with curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with powershell (Windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

## Template Generation Issues

### Template Variables Not Substituted

**Problem:** Variables like `{{cookiecutter.project_name}}` appear literally in generated files.

**Causes & Solutions:**

1. **Incorrect template syntax:**
   ```bash
   # Wrong
   name = {{cookiecutter.project_name}}
   
   # Correct
   name = "{{cookiecutter.project_name}}"
   ```

2. **Missing quotes in YAML/JSON:**
   ```yaml
   # Wrong
   title: {{cookiecutter.project_name}}
   
   # Correct
   title: "{{cookiecutter.project_name}}"
   ```

3. **Escaping issues in shell scripts:**
   ```bash
   # Wrong
   echo "Project: {{cookiecutter.project_name}}"
   
   # Correct
   echo "Project: {{cookiecutter.project_name}}"
   ```

### Invalid Project Names

**Error:**
```bash
Project name contains invalid characters
```

**Valid naming rules:**
- Use lowercase letters
- Use hyphens for word separation
- Start with a letter
- 3-50 characters long
- No spaces or special characters

**Examples:**
```bash
# Valid
my-awesome-project
data-analysis-tool
web-scraper

# Invalid
My Project          # Spaces and capitals
123-project        # Starts with number
project_name       # Underscores
very-very-very-long-project-name-that-exceeds-limit
```

### Permission Errors

**Error:**
```bash
Permission denied: '/path/to/output'
```

**Solutions:**
```bash
# Change directory permissions
chmod 755 /path/to/output

# Use a different output directory
cookiecutter . --output-dir ~/projects

# Run with sudo (not recommended)
sudo cookiecutter .
```

## Development Environment Issues

### Pre-commit Hooks Failing

**Error:**
```bash
ruff....................................................................Failed
```

**Solutions:**

1. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

2. **Update hooks:**
   ```bash
   pre-commit autoupdate
   ```

3. **Run hooks manually:**
   ```bash
   pre-commit run --all-files
   ```

4. **Fix formatting issues:**
   ```bash
   ruff format .
   ruff check --fix .
   ```

### Dependency Installation Errors

**Error:**
```bash
Failed to install package dependencies
```

**Solutions:**

1. **Clear UV cache:**
   ```bash
   uv cache clean
   ```

2. **Update UV:**
   ```bash
   pip install --upgrade uv
   ```

3. **Install dependencies individually:**
   ```bash
   uv pip install pytest
   uv pip install ruff
   uv pip install mypy
   ```

4. **Check Python version compatibility:**
   ```bash
   python --version
   uv pip check
   ```

### Import Errors

**Error:**
```bash
ModuleNotFoundError: No module named 'my_project'
```

**Solutions:**

1. **Install in development mode:**
   ```bash
   uv pip install -e .
   ```

2. **Check PYTHONPATH:**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

3. **Verify package structure:**
   ```bash
   ls -la src/
   ls -la src/my_project/
   ```

## Testing Issues

### Tests Not Found

**Error:**
```bash
collected 0 items
```

**Solutions:**

1. **Check test discovery pattern:**
   ```bash
   pytest -v  # Verbose output
   pytest --collect-only  # Show what would be collected
   ```

2. **Verify test file naming:**
   ```bash
   # Correct naming
   test_*.py
   *_test.py
   
   # Functions should start with test_
   def test_my_function():
       pass
   ```

3. **Check working directory:**
   ```bash
   # Run from project root
   cd /path/to/project
   pytest
   ```

### Coverage Issues

**Error:**
```bash
Coverage.py warning: No data to report
```

**Solutions:**

1. **Install coverage:**
   ```bash
   uv pip install pytest-cov
   ```

2. **Run with coverage:**
   ```bash
   pytest --cov=src
   ```

3. **Check source paths:**
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

### Fixture Errors

**Error:**
```bash
fixture 'my_fixture' not found
```

**Solutions:**

1. **Check conftest.py location:**
   ```
   tests/
   ├── conftest.py      # Fixtures available to all tests
   ├── test_module.py
   └── subdir/
       ├── conftest.py  # Fixtures for subdir tests
       └── test_sub.py
   ```

2. **Import fixtures explicitly:**
   ```python
   from conftest import my_fixture
   ```

3. **Check fixture scope:**
   ```python
   @pytest.fixture(scope="function")  # Default
   @pytest.fixture(scope="module")
   @pytest.fixture(scope="session")
   ```

## Type Checking Issues

### Mypy Errors

**Error:**
```bash
error: Cannot find implementation or library stub for module named 'requests'
```

**Solutions:**

1. **Install type stubs:**
   ```bash
   uv pip install types-requests
   ```

2. **Update mypy configuration:**
   ```toml
   [tool.mypy]
   ignore_missing_imports = true
   ```

3. **Check import paths:**
   ```python
   # Use absolute imports
   from my_project.utils import helper
   
   # Not relative imports in production code
   from .utils import helper
   ```

### Type Annotation Issues

**Common patterns and solutions:**

```python
# Wrong: Missing return type
def process_data(data):
    return data.strip()

# Correct: With type hints
def process_data(data: str) -> str:
    return data.strip()

# Wrong: Any type everywhere
def complex_function(data: Any) -> Any:
    pass

# Correct: Specific types
from typing import List, Dict, Optional

def complex_function(data: Dict[str, str]) -> Optional[List[str]]:
    pass
```

## Docker Issues

### Build Failures

**Error:**
```bash
Docker build failed at step X
```

**Solutions:**

1. **Check Docker version:**
   ```bash
   docker --version
   # Ensure version 20.10+
   ```

2. **Clear Docker cache:**
   ```bash
   docker system prune -a
   ```

3. **Build with verbose output:**
   ```bash
   docker build --progress=plain .
   ```

4. **Check file permissions:**
   ```bash
   # Make sure files are readable
   chmod -R 755 .
   ```

### Container Runtime Issues

**Error:**
```bash
Permission denied in container
```

**Solutions:**

1. **Check user in Dockerfile:**
   ```dockerfile
   # Create and use non-root user
   RUN useradd --create-home --shell /bin/bash app
   USER app
   ```

2. **Fix file ownership:**
   ```dockerfile
   COPY --chown=app:app src/ ./src/
   ```

3. **Mount volumes correctly:**
   ```bash
   docker run -v $(pwd):/app:Z my-project
   ```

## Documentation Issues

### MkDocs Build Failures

**Error:**
```bash
Config value: 'theme': Unrecognised theme name: 'material'
```

**Solutions:**

1. **Install MkDocs Material:**
   ```bash
   uv pip install mkdocs-material
   ```

2. **Install all documentation dependencies:**
   ```bash
   uv pip install -e .[dev]
   ```

3. **Check mkdocs.yml syntax:**
   ```bash
   mkdocs build --strict
   ```

### API Documentation Issues

**Error:**
```bash
mkdocstrings: Could not find module 'my_project'
```

**Solutions:**

1. **Install package in development mode:**
   ```bash
   uv pip install -e .
   ```

2. **Check module path in mkdocs.yml:**
   ```yaml
   plugins:
     - mkdocstrings:
         handlers:
           python:
             options:
               paths: [src]
   ```

3. **Verify docstring format:**
   ```python
   def my_function(arg: str) -> str:
       """Process the argument.
       
       Parameters
       ----------
       arg : str
           The input argument.
           
       Returns
       -------
       str
           The processed result.
       """
       return arg.upper()
   ```

## CI/CD Issues

### GitHub Actions Failures

**Error:**
```bash
Run uv pip install -e .[dev]
ERROR: File "pyproject.toml" not found
```

**Solutions:**

1. **Check file paths in workflow:**
   ```yaml
   steps:
     - uses: actions/checkout@v4  # This is required
     - name: Install dependencies
       run: uv pip install -e .[dev]
   ```

2. **Verify pyproject.toml exists:**
   ```bash
   git ls-files | grep pyproject.toml
   ```

3. **Check working directory:**
   ```yaml
   - name: Install dependencies
     working-directory: ./project-directory
     run: uv pip install -e .[dev]
   ```

### Permission Issues in CI

**Error:**
```bash
Permission denied: cannot create directory
```

**Solutions:**

1. **Use correct permissions in Dockerfile:**
   ```dockerfile
   RUN mkdir -p /app && chown app:app /app
   USER app
   ```

2. **Set correct permissions in GitHub Actions:**
   ```yaml
   - name: Set permissions
     run: chmod -R 755 .
   ```

## Performance Issues

### Slow Template Generation

**Symptoms:** Template generation takes several minutes.

**Solutions:**

1. **Use local template:**
   ```bash
   # Clone locally first
   git clone https://github.com/your-org/pythonic-template.git
   cookiecutter ./pythonic-template
   ```

2. **Clear cookiecutter cache:**
   ```bash
   rm -rf ~/.cookiecutters/
   ```

3. **Check network connectivity:**
   ```bash
   ping github.com
   ```

### Slow Dependency Installation

**Symptoms:** `uv pip install` takes very long.

**Solutions:**

1. **Use UV's speed features:**
   ```bash
   uv pip install -e .[dev] --no-deps  # Skip dependency resolution
   uv pip install -e .[dev] --offline  # Use cached packages
   ```

2. **Clear UV cache:**
   ```bash
   uv cache clean
   ```

3. **Use index URL:**
   ```bash
   uv pip install -i https://pypi.org/simple/ -e .[dev]
   ```

## Getting Help

If you're still experiencing issues:

1. **Check the documentation:** Read through all sections carefully
2. **Search existing issues:** Look for similar problems in GitHub issues
3. **Create a minimal reproduction:** Provide exact steps to reproduce the issue
4. **Include environment details:**
   ```bash
   python --version
   uv --version
   cookiecutter --version
   uname -a  # On Linux/macOS
   ```
5. **Open an issue:** Use the issue template with all requested information

### Useful Debugging Commands

```bash
# Environment information
python --version
uv --version
cookiecutter --version

# Check package installation
uv pip list
uv pip check

# Verbose testing
pytest -v -s --tb=long

# Detailed linting
ruff check --verbose .

# Type checking with details
mypy --verbose src

# Documentation build with details
mkdocs build --verbose
```

Remember: Most issues are caused by environment setup, missing dependencies, or configuration errors. Work through the basics first before diving into complex solutions.
