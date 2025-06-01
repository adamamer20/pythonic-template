# Contributing Guide

Thank you for your interest in contributing to the Pythonic Template! This guide will help you get started with contributing to the project.

## Development Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Git for version control

### Quick Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/pythonic-template.git
   cd pythonic-template
   ```

2. **Install development dependencies:**
   ```bash
   uv pip install -e .[dev]
   ```

3. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

4. **Verify the setup:**
   ```bash
   pytest
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes:**
   ```bash
   # Run tests
   pytest

   # Run linting
   ruff check .
   ruff format .

   # Test template generation
   cookiecutter . --no-input
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

### Testing Template Changes

When modifying the template itself, always test the generated project:

```bash
# Generate a test project
cookiecutter . --no-input --output-dir /tmp

# Test the generated project
cd /tmp/my-python-project
uv pip install -e .[dev]
pytest
```

## Coding Standards

### Code Style

- **Python 3.13+** syntax and features
- **Type hints** for all function signatures
- **NumPy-style docstrings** for all public functions
- **PEP 8** compliance (enforced by Ruff)
- **Maximum line length:** 88 characters

### Documentation Style

- **Clear, concise explanations**
- **Code examples** for complex features
- **Consistent formatting** using Markdown
- **Cross-references** between related sections

### Template Variables

When adding new template variables:

1. Add to `cookiecutter.json` with sensible defaults
2. Update the configuration documentation
3. Add validation in post-generation hooks if needed
4. Test with various input combinations

## Testing Guidelines

### Test Categories

1. **Unit Tests:** Test individual functions and classes
2. **Integration Tests:** Test template generation end-to-end
3. **Documentation Tests:** Verify code examples work

### Writing Tests

```python
import pytest
from pathlib import Path


def test_template_generation():
    """Test that the template generates successfully."""
    # Test implementation here
    pass


def test_generated_project_structure():
    """Verify the generated project has correct structure."""
    # Test implementation here
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run with verbose output
pytest -v
```

## Documentation Updates

### Building Documentation Locally

```bash
# Install documentation dependencies
uv pip install -e .[dev]

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### Documentation Structure

- **Getting Started:** Basic usage and setup
- **Features:** Detailed feature explanations
- **Development:** Contributing and development guides
- **Reference:** API documentation and template variables

## Pull Request Process

### Before Submitting

1. **Run the full test suite:**
   ```bash
   pytest
   pre-commit run --all-files
   ```

2. **Update documentation** if needed

3. **Test template generation** with your changes

4. **Write descriptive commit messages** following [Conventional Commits](https://www.conventionalcommits.org/)

### Pull Request Template

When creating a pull request, please include:

- **Clear description** of the changes
- **Motivation** for the changes
- **Testing performed** to verify the changes
- **Documentation updates** if applicable
- **Breaking changes** if any

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation review** for clarity

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

### Release Steps

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create release tag:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
4. **GitHub Actions** will handle the rest

## Community Guidelines

### Code of Conduct

Please be respectful and inclusive in all interactions. We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).

### Getting Help

- **GitHub Issues:** Bug reports and feature requests
- **GitHub Discussions:** Questions and general discussion
- **Documentation:** Check existing docs first

### Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for significant contributions

## Common Tasks

### Adding a New Feature

1. **Research** existing solutions and best practices
2. **Design** the feature with backward compatibility in mind
3. **Implement** with comprehensive tests
4. **Document** the feature thoroughly
5. **Get feedback** through draft pull request

### Fixing a Bug

1. **Reproduce** the bug with a test case
2. **Identify** the root cause
3. **Fix** the issue with minimal changes
4. **Verify** the fix doesn't break anything else
5. **Update tests** to prevent regression

### Updating Dependencies

1. **Check** for breaking changes in changelogs
2. **Update** `pyproject.toml` with new versions
3. **Test** thoroughly with new dependencies
4. **Update** documentation if APIs changed

## Questions?

If you have questions about contributing:

1. Check the existing documentation
2. Search through GitHub issues
3. Create a new issue with the "question" label
4. Join the discussion in GitHub Discussions

Thank you for contributing to the Pythonic Template! 🚀
