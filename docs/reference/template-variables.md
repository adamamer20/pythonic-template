# Template Variables Reference

This reference provides comprehensive documentation for all variables available in the Pythonic Template.

## Overview

Template variables are defined in `cookiecutter.json` and can be customized during project generation. Each variable has a default value and specific validation rules.

## Project Information

### `project_name`

**Type:** String
**Default:** `"my-python-project"`
**Validation:** Must be a valid Python package name (lowercase, hyphens allowed)

The name of your Python project. This will be used for:

- Repository name
- Package directory in `src/`
- PyPI package name
- Documentation title
- Docker image name

**Examples:**

```bash
# Valid names
data-analysis-toolkit
web-scraper
ml-pipeline
awesome-python-lib

# Invalid names
My-Project  # Capital letters
123-project  # Starts with number
project_name  # Underscores not recommended
```

**Generated Files Affected:**

- `pyproject.toml` - package name
- `src/{project_name}/` - source directory
- `README.md` - title and installation commands
- `docs/index.md` - documentation title
- `.github/workflows/` - workflow names

### `project_description`

**Type:** String
**Default:** `"A modern Python project"`
**Validation:** 10-100 characters recommended

A brief description of your project's purpose and functionality.

**Usage:**

- PyPI package description
- README.md subtitle
- Documentation homepage
- GitHub repository description

**Best Practices:**

```bash
# Good descriptions
"A fast and flexible data processing library"
"Modern web scraping toolkit with async support"
"Machine learning utilities for time series analysis"

# Avoid
"My project"  # Too generic
"This is a very long description that goes on and on..."  # Too verbose
```

### `author_name`

**Type:** String
**Default:** `"Your Name"`
**Validation:** 2-50 characters

The primary author or maintainer of the project.

**Used In:**

- `pyproject.toml` - author field
- `LICENSE` - copyright holder
- Documentation - author information
- Package metadata

### `author_email`

**Type:** String
**Default:** `"your.email@example.com"`
**Validation:** Must be valid email format

Contact email for the project maintainer.

**Used In:**

- `pyproject.toml` - author email
- Documentation - contact information
- Package metadata for PyPI

## Technical Configuration

### `python_version`

**Type:** String (Choice)
**Default:** `"3.12"`
**Options:** `["3.11", "3.12", "3.13"]`

Minimum Python version required for the project.

**Impact:**

- `pyproject.toml` - Python version constraint
- CI/CD workflows - test matrix
- Documentation - installation requirements
- Type hints - available features

**Version Feature Matrix:**

| Feature | 3.11 | 3.12 | 3.13 |
|---------|------|------|------|
| `tomllib` | ✅ | ✅ | ✅ |
| PEP 695 Type Parameters | ❌ | ✅ | ✅ |
| f-string improvements | ❌ | ✅ | ✅ |
| Better error messages | ❌ | ✅ | ✅ |
| Performance improvements | ❌ | ❌ | ✅ |

### `use_docker`

**Type:** String (Choice)
**Default:** `"y"`
**Options:** `["y", "n"]`

Whether to include Docker support in the generated project.

**When enabled (`"y"`):**

- `.devcontainer/Dockerfile` - optimized multi-stage build
- `docker-compose.yml` - development environment
- `.dockerignore` - exclude unnecessary files
- Documentation section on Docker usage

**Docker Configuration:**

```dockerfile
# Generated Dockerfile features:
- Multi-stage build for smaller images
- Non-root user for security
- UV for fast dependency installation
- Health checks
- Proper signal handling
```

### `use_github_actions`

**Type:** String (Choice)
**Default:** `"y"`
**Options:** `["y", "n"]`

Whether to include GitHub Actions CI/CD workflows.

**When enabled (`"y"`):**

- `.github/workflows/ci.yml` - comprehensive CI pipeline
- `.github/workflows/release.yml` - automated releases
- `.github/dependabot.yml` - dependency updates
- `.github/ISSUE_TEMPLATE/` - issue templates
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template

**CI Pipeline Features:**

- Multi-platform testing (Linux, macOS, Windows)
- Multiple Python versions
- Code quality checks (Ruff, mypy)
- Security scanning
- Documentation building
- Coverage reporting

### `use_pre_commit`

**Type:** String (Choice)
**Default:** `"y"`
**Options:** `["y", "n"]`

Whether to include pre-commit hooks for code quality.

**When enabled (`"y"`):**

- `.pre-commit-config.yaml` - hook configuration
- Automatic formatting with Ruff
- Import sorting
- Type checking with mypy
- Security checks with bandit
- Trailing whitespace removal

**Hook Configuration:**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
```

## Advanced Configuration

### `project_slug`

**Type:** String (Computed)
**Default:** Derived from `project_name`
**Validation:** Auto-generated, cannot be directly set

A Python-compatible version of the project name used for package imports.

**Transformation Rules:**

```python
# project_name → project_slug
"my-awesome-project" → "my_awesome_project"
"data-science-toolkit" → "data_science_toolkit"
"WebScraper" → "webscraper"
```

**Used In:**

- `src/{project_slug}/` - package directory
- Import statements in examples
- Test file imports

### `repository_url`

**Type:** String (Computed)
**Default:** `"https://github.com/{author_name}/{project_name}"`
**Validation:** Auto-generated from author and project name

The GitHub repository URL for the project.

**Used In:**

- `pyproject.toml` - project URLs
- Documentation - source links
- README.md - repository badges
- Issue templates

### `documentation_url`

**Type:** String (Computed)
**Default:** `"https://{author_name}.github.io/{project_name}"`
**Validation:** Auto-generated for GitHub Pages

The URL where documentation will be hosted.

**Used In:**

- `pyproject.toml` - documentation URL
- README.md - documentation links
- MkDocs configuration

## License Configuration

### `license`

**Type:** String (Choice)
**Default:** `"MIT"`
**Options:** `["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Proprietary"]`

The license for your project.

**License Matrix:**

| License | Permissive | Copyleft | Commercial Use |
|---------|------------|----------|----------------|
| MIT | ✅ | ❌ | ✅ |
| Apache-2.0 | ✅ | ❌ | ✅ |
| GPL-3.0 | ❌ | ✅ | ⚠️ |
| BSD-3-Clause | ✅ | ❌ | ✅ |
| Proprietary | ❌ | ❌ | ✅ |

**Generated Files:**

- `LICENSE` - full license text
- `pyproject.toml` - license classifier
- README.md - license badge

## Development Tools Configuration

### `ruff_config`

**Type:** Dictionary (Internal)
**Default:** Comprehensive Ruff configuration

Internal configuration for Ruff linting and formatting.

**Features:**

```toml
[tool.ruff]
line-length = 88
target-version = "py311"  # Based on python_version

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
```

### `mypy_config`

**Type:** Dictionary (Internal)
**Default:** Strict mypy configuration

Internal configuration for type checking.

**Settings:**

```toml
[tool.mypy]
python_version = "3.11"  # Based on python_version
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### `pytest_config`

**Type:** Dictionary (Internal)
**Default:** Comprehensive pytest configuration

Internal configuration for testing.

**Settings:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
]
```

## Documentation Configuration

### `mkdocs_theme`

**Type:** String (Internal)
**Default:** `"material"`

The MkDocs theme used for documentation.

**Theme Features:**

- Material Design
- Dark/light mode toggle
- Search functionality
- Navigation sidebar
- Social media integration
- Code syntax highlighting

### `mkdocs_features`

**Type:** List (Internal)
**Default:** Comprehensive feature set

Enabled MkDocs Material features:

```yaml
theme:
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy
    - content.code.annotate
```

## Computed Variables

These variables are automatically computed from other inputs:

### `year`

**Type:** String
**Default:** Current year
**Usage:** Copyright notices, license files

### `package_name`

**Type:** String
**Default:** Normalized version of `project_name`
**Usage:** Python package imports

### `class_name`

**Type:** String
**Default:** PascalCase version of `project_name`
**Usage:** Main class names in generated code

## Validation Rules

### Project Name Validation

```python
def validate_project_name(name: str) -> bool:
    """Validate project name follows Python packaging conventions."""
    import re

    # Must be lowercase with hyphens
    if not re.match(r'^[a-z][a-z0-9\-]*[a-z0-9]$', name):
        return False

    # Cannot be Python reserved word
    reserved = ['and', 'or', 'not', 'if', 'else', 'def', 'class', ...]
    if name.replace('-', '_') in reserved:
        return False

    # Reasonable length
    if not (3 <= len(name) <= 50):
        return False

    return True
```

### Email Validation

```python
def validate_email(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

## Default Values Summary

```json
{
    "project_name": "my-python-project",
    "project_description": "A modern Python project",
    "author_name": "Your Name",
    "author_email": "your.email@example.com",
    "python_version": "3.13",
    "use_docker": "y",
    "use_github_actions": "y",
    "use_pre_commit": "y",
    "license": "MIT"
}
```

## Customization Examples

### Minimal Project

```bash
cookiecutter https://github.com/your-org/pythonic-template \
    --no-input \
    project_name="simple-tool" \
    author_name="Jane Doe" \
    use_docker="n" \
    use_github_actions="n"
```

### Enterprise Project

```bash
cookiecutter https://github.com/your-org/pythonic-template \
    --no-input \
    project_name="enterprise-api" \
    project_description="High-performance enterprise API framework" \
    author_name="Enterprise Team" \
    author_email="team@enterprise.com" \
    python_version="3.12" \
    license="Proprietary"
```

### Data Science Project

```bash
cookiecutter https://github.com/your-org/pythonic-template \
    --no-input \
    project_name="ml-pipeline" \
    project_description="Machine learning pipeline for predictive analytics" \
    python_version="3.13" \
    use_docker="y"
```

This reference provides complete information about all template variables, helping users customize the Pythonic Template for their specific needs.
