# Pythonic Template 🐍

A modern, comprehensive Cookiecutter template for Python projects that follows best practices and includes everything you need for professional Python development - now with **advanced devcontainer support**, **AI agent integration**, and **academic paper workflows**.

## Features

### ✨ **Key Features**

- **Modern Python tooling**: uv, Ruff, pytest, MkDocs Material, beartype
- **AI-powered development**: Claude Code CLI, OpenAI Codex, Roo Code integration
- **Advanced containerization**: Multi-stage Docker, VS Code devcontainers, service orchestration
- **Academic paper support**: Quarto integration, automatic rendering, citation management
- **Quality assurance**: Pre-commit hooks, GitHub Actions CI/CD, automated dependency updates
- **Developer experience**: Makefile-driven workflow, template synchronization with Cruft

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
   - Python version (default: 3.12; supports 3.12+)
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
| `author_email` | Your email | "<adam@example.com>" | Any email |
| `github_username` | Your GitHub username | "adamamer20" | Any username |
| `python_version` | Minimum Python version | "3.12" | Any 3.12+ version |
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

## GitHub Actions Workflows

The template includes CI/CD workflows for testing, building, publishing to PyPI, documentation deployment, and paper rendering (for academic projects).

Note: Supported Python versions are derived from `project.requires-python` in `pyproject.toml`. CI tests only the minimum and maximum supported minors.

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

## License

This template is licensed under the MIT License. Generated projects can use any license you choose.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Happy coding!** 🚀
