# Pythonic Template Documentation 🐍

Welcome to **Pythonic Template** — a modern, comprehensive Cookiecutter template for Python projects that follows best practices and includes everything you need for professional Python development.

## What is Pythonic Template?

Pythonic Template is a carefully crafted [Cookiecutter](https://cookiecutter.readthedocs.io/) template that generates Python projects with:

- ✨ **Modern tooling** (uv, Ruff, pytest)
- 🛡️ **Quality assurance** (pre-commit, GitHub Actions, type hints)
- 📚 **Professional documentation** (MkDocs Material)
- 🚀 **DevOps ready** (CI/CD, automated publishing)

## Philosophy

Following the principles of clarity over cleverness, this template generates:

- **Crystal-clear, Pythonic code** that feels like readable English
- **Fully-typed projects** with PEP 484/695 type hints everywhere
- **DRY, atomic, modular** components that are loosely coupled
- **Test-first development** with comprehensive pytest configuration
- **Automated quality control** with pre-commit hooks and CI/CD

## Quick Start

```bash
# Install cookiecutter
pip install cookiecutter
# or
uv tool install cookiecutter

# Generate your project
cookiecutter https://github.com/adamamer20/pythonic-template

# Follow the prompts to configure your project
```

## What You Get

When you use this template, you get a fully configured Python project with:

### Modern Development Stack
- **[uv](https://github.com/astral-sh/uv)** - Ultra-fast Python package management
- **[Ruff](https://github.com/astral-sh/ruff)** - Lightning-fast linting and formatting
- **[pytest](https://pytest.org/)** - Comprehensive testing framework
- **[pre-commit](https://pre-commit.com/)** - Automated code quality checks

### Professional Documentation
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** - Beautiful, responsive documentation
- **[mkdocstrings](https://mkdocstrings.github.io/)** - Automatic API documentation from docstrings
- **NumPy-style docstrings** - Clear, comprehensive documentation standards

### DevOps & CI/CD
- **GitHub Actions** - Automated testing, building, and publishing
- **Dependabot** - Automated dependency updates
- **PyPI publishing** - Trusted publishing workflow
- **Docker support** - Containerized development and deployment

## Target Environment

This template is optimized for:

- **Python {{ cookiecutter.python_version }}+** with modern features
- **Pop OS 24.04** (but works on any Linux/macOS/Windows)
- **CUDA 12** support for GPU-accelerated projects
- **Professional development workflows**

## Core Principles

1. **Clarity over cleverness** - Code should be immediately understandable
2. **Type safety everywhere** - Full type hints with runtime validation
3. **DRY and modular** - Each component does one thing well
4. **Test-driven development** - Tests come first, implementation follows
5. **Automated quality** - Let tools handle formatting, linting, and checks
6. **Documentation-first** - Every public API is documented with examples

## Get Started

Ready to create your next Python project? Head over to the [Quick Start Guide](getting-started/quick-start.md) to begin!

## Contributing

This template is open source and welcomes contributions! See our [Contributing Guide](development/contributing.md) for details on how to help improve the template.

---

*Built with ❤️ by [Adam Amer](https://github.com/adamamer20) following modern Python best practices.*
