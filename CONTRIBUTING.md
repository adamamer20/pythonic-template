# Contributing to Pythonic Template

Thank you for your interest in contributing to Pythonic Template! This document provides guidelines and information for contributors.

## 🌟 **Our Mission**

Generate crystal‑clear, Pythonic, fully‑typed, test‑first code that is easy to swap, automate, and scale — never monolithic, always DRY.

## 🚀 Getting Started

### Prerequisites

- Python {{ cookiecutter.python_version }}+
- [uv](https://github.com/astral-sh/uv) for package management
- Git

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/pythonic-template.git
   cd pythonic-template
   ```

2. **Install development dependencies**:
   ```bash
   uv pip install -e .[dev]
   ```

3. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

4. **Test the template**:
   ```bash
   # Test generating a project
   cookiecutter . --no-input
   
   # Test with different configurations
   cookiecutter . --no-input license=Apache-2.0 use_docker=y
   ```

## 📝 Development Guidelines

### Code Quality Standards

- ✨ **Clarity > cleverness** - Code should read like English
- 📚 **Full type hints** everywhere (PEP 484/695)
- 🔄 **DRY, atomic, modular** - Each component does one thing well
- 🌐 **Environment agnostic** - No hard-coded paths or configurations
- 📝 **Meaningful comments** ≤ 80 chars explaining **why**, not **what**

### Tools and Standards

- **Package Management**: uv only, no manual requirements.txt
- **Code Quality**: Ruff for linting and formatting
- **Testing**: pytest with comprehensive coverage
- **Type Checking**: beartype for runtime type checking
- **Documentation**: NumPy-style docstrings, MkDocs Material
- **Git Hooks**: pre-commit for automated quality checks

### Testing Philosophy

- 🧪 **Test-Driven Development**: Write failing tests first
- ✅ **Comprehensive Coverage**: Aim for high test coverage
- 🔄 **Template Testing**: Test generated projects work correctly
- 🎯 **Edge Cases**: Test different configuration combinations

## 🛠️ Development Workflow

### 1. Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our guidelines

3. **Test your changes**:
   ```bash
   # Run tests
   pytest -v
   
   # Test template generation
   make test-template
   
   # Run all quality checks
   pre-commit run --all-files
   ```

4. **Update documentation** if needed

### 2. Template Testing

Test different configurations:

```bash
# Basic template
cookiecutter . --no-input

# With Docker
cookiecutter . --no-input use_docker=y

# Different license
cookiecutter . --no-input license=Apache-2.0

# Test the generated project
cd my-amazing-library
uv pip install -e .[dev]
pre-commit run --all-files
pytest
```

### 3. Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)
- Add docstrings for any Python code (NumPy style)
- Update cookiecutter.json documentation if adding new variables

## 📋 Pull Request Process

1. **Ensure all tests pass**:
   ```bash
   pytest
   pre-commit run --all-files
   ```

2. **Update documentation** as needed

3. **Add changelog entry** in the "Unreleased" section

4. **Create descriptive PR**:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference any related issues
   - Include testing instructions

5. **Wait for review** - maintainers will review and provide feedback

## 🐛 Bug Reports

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, uv version)
- **Generated project structure** if relevant
- **Error messages** and stack traces

## 💡 Feature Requests

For new features:

- **Describe the use case** - what problem does it solve?
- **Provide examples** of how it would be used
- **Consider alternatives** - why is this the best approach?
- **Check existing issues** to avoid duplicates

## 🏷️ Release Process

1. **Update version** in pyproject.toml
2. **Update CHANGELOG.md** with release date
3. **Create release PR** with all changes
4. **Merge to main** after approval
5. **Tag release** and push tags
6. **GitHub Actions** will handle PyPI publishing

## 📊 Quality Metrics

We maintain high standards:

- **Test Coverage**: Aim for >90%
- **Type Coverage**: 100% type hints
- **Ruff Score**: 10/10 (no warnings)
- **Documentation**: All public APIs documented
- **Template Quality**: Generated projects must pass all checks

## 🔧 GitHub Actions Version Policy

We maintain consistency across GitHub Actions versions:

### Action Version Standards

- **Pin to major versions** (e.g., `@v5`, `@v6`) for stability
- **Use latest stable versions** of all actions
- **Update consistently** across all workflows
- **Use Dependabot** for automated updates

### Current Standard Versions

| Action | Version | Purpose |
|--------|---------|----------|
| `actions/checkout` | `@v4` | Repository checkout |
| `actions/setup-python` | `@v5` | Python setup |
| `astral-sh/setup-uv` | `@v6` | UV package manager |
| `codecov/codecov-action` | `@v5` | Coverage reporting |
| `actions/configure-pages` | `@v5` | GitHub Pages setup |
| `actions/deploy-pages` | `@v5` | GitHub Pages deployment |
| `actions/upload-pages-artifact` | `@v3` | Pages artifact upload |

### Updating Action Versions

When updating actions:

1. **Check release notes** for breaking changes
2. **Update all workflows** consistently
3. **Test thoroughly** with template generation
4. **Update this documentation** with new versions

## 🎯 Areas for Contribution

Looking for ways to help? Consider:

- 📝 **Documentation improvements**
- 🧪 **Additional test cases**
- 🔧 **New template features**
- 🐛 **Bug fixes and edge cases**
- 🚀 **Performance improvements**
- 📦 **Dependency updates**
- 🏗️ **CI/CD enhancements**

## 💬 Getting Help

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Create issues for bugs and feature requests
- **Documentation**: Check the docs at our GitHub Pages site

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow Python community standards

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor insights

---

**Thank you for contributing to Pythonic Template!** 🚀

Together we're making Python development more efficient, enjoyable, and professional.
