# Pythonic Template 🐍

A modern, comprehensive Cookiecutter template for Python projects that follows best practices and includes everything you need for professional Python development - now with **advanced devcontainer support**, **AI agent integration**, and **academic paper workflows**.

## Features

### 🚀 **Modern Python Stack**

- **uv** for ultra-fast package management and dependency resolution
- **Ruff** for lightning-fast linting and formatting
- **pytest** with comprehensive test configuration
- **MkDocs Material** for beautiful documentation
- **beartype** for runtime type checking

### 🤖 **AI-Powered Development**

- **Claude Code CLI** integration for AI-assisted coding
- **OpenAI Codex** support via AGENTS.md
- **Roo Code** with Qdrant vector database and Ollama
- Configurable AI agent selection (all, specific agents, or none)
- Automatic devcontainer setup for selected agents

### 🐳 **Advanced Container Development**

- **Multi-stage Dockerfile** with optimized caching
- **Docker Compose** orchestration for development services
- **VS Code devcontainer** with proper port forwarding
- **Conditional installations** based on project configuration
- **Docker-in-Docker** support for containerized workflows

### 📄 **Academic Paper Support**

- **Quarto** integration for scientific paper authoring
- **Marimo** for interactive data analysis and visualization
- **Automatic paper rendering** to HTML and PDF
- **GitHub Actions** for paper deployment
- **Citation management** with BibTeX support
- **Mathematical expressions** with MathJax

### 🛡️ **Quality Assurance**

- Pre-commit hooks for automatic code quality
- GitHub Actions CI/CD pipelines
- Dependabot for automated dependency updates
- Full type hints with runtime validation
- Comprehensive test coverage

### 📚 **Documentation & Developer Experience**

- Material for MkDocs with modern theme
- **Makefile-driven development** workflow
- **Cruft** for template synchronization
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
   # Using uv (recommended)
   uv tool install cookiecutter

   # Or using pip
   pip install cookiecutter
   ```

2. **Generate your project**:

   ```bash
   cookiecutter https://github.com/adamamer20/pythonic-template
   ```

3. **Follow the prompts** to configure your project:
   - Project name: "My Amazing Library"
   - Package name: (auto-generated from project name)
   - Author information
   - Python version (3.9-3.12, defaults to 3.12)
   - License choice (MIT, Apache-2.0, BSD-3-Clause)
   - **Project type**: "standard" or "paper" (for academic research)
   - **AI agents**: Choose from Claude Code, OpenAI Codex, Roo Code, or combinations

4. **Navigate to your new project**:

   ```bash
   cd your-new-project
   ```

5. **Initialize your development environment**:

   ```bash
   make setup  # Complete environment setup with dependencies and pre-commit
   ```

6. **Start developing**! 🎉

   ```bash
   # Show all available commands (ALWAYS start here!)
   make help

   # Run tests
   make test

   # For paper projects - render your paper
   make paper-render  # (only available for paper type projects)

   # Start coding in src/your_package/
   # Tests go in tests/
   # Papers go in paper/ (if using paper type)
   ```

## Template Configuration

The template prompts for these variables:

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `project_name` | Human-readable project name | "My Amazing Library" | Any string |
| `package_name` | Python package name (auto-generated) | (derived from project_name) | Auto-generated |
| `repo_name` | Repository name (auto-generated) | (derived from project_name) | Auto-generated |
| `author_name` | Your name | "Adam Amer" | Any string |
| `author_email` | Your email | "adam@example.com" | Any email |
| `github_username` | Your GitHub username | "adamamer20" | Any username |
| `python_version` | Minimum Python version | "3.12" | "3.9" to "3.13" |
| `initial_version` | Starting version | "0.1.0" | Any version string |
| `license` | License type | "MIT" | MIT, Apache-2.0, BSD-3-Clause |
| **`project_type`** | **Project type** | **"standard"** | **"standard", "paper"** |
| **`ai_agents`** | **AI agents to include** | **"all"** | **"all", "claude_code", "openai_codex", "roo_code", combinations, "none"** |
| `project_short_description` | Brief description | "A modern Python package" | Any string |

## Generated Project Structure

```text
your-project/
├── .devcontainer/              # 🐳 Advanced development containers
│   ├── Dockerfile              # Multi-stage container with conditional installs
│   ├── docker-compose.yml      # Service orchestration (Qdrant, Ollama)
│   ├── devcontainer.json       # VS Code devcontainer configuration
│   └── ai-agents-config.json   # AI agent setup configuration
├── .github/
│   ├── workflows/              # CI/CD pipelines
│   │   ├── ci.yml              # Standard CI
│   │   ├── render-paper.yml    # 📄 Paper rendering (paper projects only)
│   │   └── ...
│   └── dependabot.yml          # Dependency updates
├── .roo/                       # 🤖 Roo Code AI configuration (if selected)
│   └── rules-code/
│       └── rules.md            # Roo-specific development rules
├── .vscode/                    # VS Code configuration
├── docs/                       # Documentation source
├── paper/                      # 📄 Academic paper (paper projects only)
│   ├── paper.qmd               # Main paper in Quarto format
│   └── references.bib          # Bibliography
├── src/your_package/           # Your Python package
├── tests/                      # Test suite
├── .env.example               # Environment variables template
├── .gitignore                 # Comprehensive gitignore
├── .pre-commit-config.yaml    # Code quality hooks
├── .cruft.json                # Template synchronization config
├── AGENTS.md                  # 🤖 AI agent instructions
├── Makefile                   # 🔧 CENTRAL command hub (USE THIS!)
├── mkdocs.yml                 # Documentation configuration
├── pyproject.toml             # Project configuration
└── README.md                  # Project documentation
```

## Development Workflow

**CRITICAL: Always use `make` commands for development tasks!**

After generating your project:

### 1. **Quick Start**

```bash
# ALWAYS start here - see all available commands
make help

# Complete environment setup (replaces multiple manual steps)
make setup

# Start development
make dev
```

### 2. **Essential Make Commands**

The Makefile is the **CENTRAL HUB** for all development operations:

```bash
# Core workflow
make setup         # Complete development environment setup
make test          # Run tests with type checking
make quick-test    # Fast tests for development
make check         # Run all quality checks (lint + format + test)

# Development tasks
make lint          # Run linting and fix issues
make format        # Format code with ruff
make quality       # Run all quality checks

# Utilities
make clean         # Clean build artifacts
make sync          # Sync dependencies
make upgrade       # Upgrade all dependencies
make ai-setup      # Set up AI agents (Claude Code CLI, etc.)
```

### 3. **Paper Projects (if project_type="paper")**

```bash
make paper-render   # Render paper to HTML and PDF
make paper-preview  # Preview paper in browser
make paper-check    # Check paper for issues
```

### 4. **AI Agent Integration**

If you selected AI agents during setup:

- **Claude Code CLI**: Available via `claude-code` command
- **OpenAI Codex**: Uses AGENTS.md for instructions
- **Roo Code**: Uses `.roo/rules-code/rules.md` + Qdrant + Ollama

The devcontainer automatically configures your selected agents!

## Key Features Explained

### 🔍 **Runtime Type Checking**

The template uses **beartype** for runtime type safety:

```python
from beartype import beartype

@beartype
def process_data(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# beartype provides runtime type validation at function call time
```

Set `DEV_TYPECHECK=1` in your `.env` file to enable runtime type validation during testing.

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

### 🐳 **Advanced Docker Support**

Multi-stage Docker configuration with:

- **Base, deps, builder, runtime, development** stages for optimal caching
- **Fish shell** for better development experience
- **Conditional installations** based on project configuration
- **Docker Compose** orchestration for complex development environments
- **VS Code devcontainer** with automatic port forwarding
- **AI service integration** (Qdrant, Ollama) when using Roo Code

### 🤖 **AI Agent Integration**

Choose your AI development assistants:

- **Claude Code CLI**: Official Anthropic CLI for AI-assisted coding
- **OpenAI Codex**: Integration via AGENTS.md instructions
- **Roo Code**: Advanced AI with vector database and local LLM
- **Combinations**: Mix and match agents as needed
- **Automatic setup**: Devcontainer configures everything for you

### 📄 **Academic Paper Workflow**

For `project_type="paper"`:

- **Quarto integration** for scientific authoring
- **Marimo** for interactive data analysis and visualization
- **paper/paper.qmd** with comprehensive template
- **Automatic rendering** to HTML and PDF via GitHub Actions
- **Citation management** with BibTeX support
- **Mathematical expressions** with MathJax
- **Paper-specific Make commands**: `make paper-render`, `make paper-preview`

## GitHub Actions Workflows

The template includes comprehensive workflows:

1. **CI** (`ci.yml`): Run tests, linting, and type checking on every push/PR
2. **Build** (`build.yml`): Build packages across multiple OS/Python versions
3. **Publish** (`publish.yml`): Publish to PyPI on release
4. **Docs** (`docs.yml`): Deploy documentation to GitHub Pages
5. **Paper Rendering** (`render-paper.yml`): Automatically render academic papers (paper projects only)

## Template Synchronization

Projects generated from this template can stay synchronized with template updates using [Cruft](https://cruft.github.io/cruft/):

### Setup (included automatically)

Cruft is included in the generated project's development dependencies and configured with a `.cruft.json` file.

### Checking for Updates

```bash
make sync           # First sync your current dependencies
uv run cruft check  # Check for template updates
```

### Applying Updates

```bash
uv run cruft update  # Apply template updates
make setup          # Re-setup environment with new changes
```

This will apply template changes while preserving your customizations. The updated `.cruft.json` tracks your configuration for seamless updates.

## Best Practices Included

- ✅ **PEP 518** compliant `pyproject.toml`
- ✅ **Src layout** for proper package structure
- ✅ **Runtime type safety** with beartype
- ✅ **Makefile-driven development** workflow
- ✅ **Advanced containerization** with multi-stage Docker
- ✅ **AI agent integration** for modern development
- ✅ **Academic paper support** with Quarto
- ✅ **Template synchronization** with Cruft
- ✅ **Comprehensive testing** with pytest and coverage
- ✅ **Modern tooling** (uv, ruff, pre-commit)
- ✅ **Professional documentation** with MkDocs Material
- ✅ **CI/CD ready** with GitHub Actions
- ✅ **Security** with dependabot and automated updates
- ✅ **Outstanding developer experience** with VS Code devcontainers

## New in This Release

### 🚀 **Major Enhancements**

- **AI Agent Integration**: Claude Code CLI, OpenAI Codex, Roo Code support
- **Academic Paper Workflows**: Quarto integration for scientific authoring
- **Advanced Devcontainers**: Multi-stage Docker with service orchestration
- **Makefile-Centric Development**: Centralized command hub for all tasks
- **Enhanced Type Checking**: Replaced typeguard with beartype for runtime validation
- **Template Versioning**: Cruft integration for seamless updates

### 🔧 **Technical Improvements**

- Multi-stage Dockerfile with optimized layer caching
- Docker Compose for complex development environments
- Conditional installations based on project configuration
- Enhanced VS Code devcontainer with proper port forwarding
- Qdrant vector database and Ollama integration for AI workflows

## License

This template is licensed under the MIT License. Generated projects can use any license you choose.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Happy coding!** 🚀
