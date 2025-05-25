# Pythonic Template 🐍

A modern, comprehensive Cookiecutter template for Python projects that follows best practices and includes everything you need for professional Python development.

## Features

### 🚀 **Modern Python Stack**
- **uv** for ultra-fast package management and dependency resolution
- **Ruff** for lightning-fast linting and formatting
- **pytest** with comprehensive test configuration
- **MkDocs Material** for beautiful documentation
- **typeguard** for runtime type checking

### 🛡️ **Quality Assurance**
- Pre-commit hooks for automatic code quality
- GitHub Actions CI/CD pipelines
- Dependabot for automated dependency updates
- Full type hints with runtime validation
- Comprehensive test coverage

### 📚 **Documentation & Developer Experience**
- Material for MkDocs with modern theme
- VS Code configuration and recommended extensions
- Docker support with dev containers
- Environment variable management
- Professional project structure

### 🔧 **DevOps Ready**
- GitHub Actions for CI, building, and publishing
- Automated dependency updates with auto-merge
- PyPI publishing with trusted publishing
- Documentation deployment to GitHub Pages

## Quick Start

1. **Install Cookiecutter** (if not already installed):
   ```bash
   pip install cookiecutter
   # or
   uv tool install cookiecutter
   ```

2. **Generate your project**:
   ```bash
   cookiecutter https://github.com/adamamer20/pythonic-template
   ```

3. **Follow the prompts** to configure your project:
   - Project name: "My Amazing Library"
   - Package name: (auto-generated from project name)
   - Author information
   - License choice (MIT, Apache-2.0, BSD-3-Clause)
   - Docker support (optional)

4. **Navigate to your new project**:
   ```bash
   cd your-new-project
   ```

5. **Install development dependencies**:
   ```bash
   uv pip install -e .[dev]
   ```

6. **Start developing**! 🎉

## Template Configuration

The template prompts for these variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `project_name` | Human-readable project name | "My Amazing Library" |
| `package_name` | Python package name (auto-generated) | (derived from project_name) |
| `repo_name` | Repository name (auto-generated) | (derived from project_name) |
| `author_name` | Your name | "Adam Amer" |
| `author_email` | Your email | "adam@example.com" |
| `github_username` | Your GitHub username | "adamamer20" |
| `python_version` | Minimum Python version | "3.12" |
| `initial_version` | Starting version | "0.1.0" |
| `license` | License type | "MIT" |
| `use_docker` | Include Docker support | "n" |
| `project_short_description` | Brief description | "A modern Python package" |

## Generated Project Structure

```
your-project/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   └── dependabot.yml      # Dependency updates
├── .vscode/               # VS Code configuration
├── docs/                  # Documentation source
├── src/your_package/      # Your Python package
├── tests/                 # Test suite
├── .env.example          # Environment variables template
├── .gitignore            # Comprehensive gitignore
├── .pre-commit-config.yaml # Code quality hooks
├── Dockerfile            # Development container (optional)
├── Makefile              # Common development tasks
├── mkdocs.yml            # Documentation configuration
├── pyproject.toml        # Project configuration
└── README.md             # Project documentation
```

## Development Workflow

After generating your project:

### 1. **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Install dependencies
uv pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### 2. **Development Commands**
```bash
# Run tests
pytest

# Run tests with type checking
DEV_TYPECHECK=1 pytest

# Lint and format
ruff check .
ruff format .

# Serve documentation
mkdocs serve

# Run all quality checks
pre-commit run --all-files
```

### 3. **Make Commands**
The template includes a comprehensive Makefile:

```bash
make help          # Show available commands
make dev-install   # Install development dependencies  
make test          # Run tests
make test-cov      # Run tests with coverage
make test-type     # Run tests with type checking
make lint          # Run linting
make format        # Format code
make docs          # Serve documentation
make clean         # Clean build artifacts
make build         # Build package
```

## Key Features Explained

### 🔍 **Runtime Type Checking**
Set `DEV_TYPECHECK=1` in your `.env` file to enable runtime type validation with typeguard:

```python
# Your code with type hints
def process_data(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# typeguard will validate types at runtime in development
```

### 📦 **Modern Package Management**
- Uses **uv** for fast dependency resolution
- Lock files for reproducible environments
- Development dependency groups
- Easy extras configuration

### 🤖 **Automated Quality**
- **Ruff** for fast linting and formatting
- **Pre-commit** hooks prevent bad commits
- **Dependabot** keeps dependencies updated
- **GitHub Actions** for continuous integration

### 📚 **Beautiful Documentation**
- **Material for MkDocs** with modern theme
- **mkdocstrings** for automatic API documentation
- **MathJax** support for mathematical expressions
- **Mermaid** diagrams support

### 🐳 **Docker Support**
Optional Docker configuration with:
- Fish shell for better development experience
- Pre-configured development environment
- VS Code dev container support

## GitHub Actions Workflows

The template includes four workflows:

1. **CI** (`ci.yml`): Run tests, linting, and type checking on every push/PR
2. **Build** (`build.yml`): Build packages across multiple OS/Python versions
3. **Publish** (`publish.yml`): Publish to PyPI on release
4. **Docs** (`docs.yml`): Deploy documentation to GitHub Pages

## Best Practices Included

- ✅ **PEP 518** compliant `pyproject.toml`
- ✅ **Src layout** for proper package structure
- ✅ **Type hints** everywhere with runtime validation
- ✅ **Comprehensive testing** with pytest and coverage
- ✅ **Modern tooling** (uv, ruff, pre-commit)
- ✅ **Professional documentation** with MkDocs Material
- ✅ **CI/CD ready** with GitHub Actions
- ✅ **Security** with dependabot and automated updates
- ✅ **Developer experience** with VS Code configuration

## License

This template is licensed under the MIT License. Generated projects can use any license you choose.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Happy coding!** 🚀