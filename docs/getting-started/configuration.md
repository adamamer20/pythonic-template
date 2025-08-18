# Configuration Guide

This guide explains how to configure your generated project and customize the template to your needs.

## Template Configuration

When you run `cookiecutter`, you'll be asked to configure these variables:

### Project Information

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `project_name` | Human-readable project name | "My Amazing Project" | "Neural Network Library" |
| `repo_name` | Repository/package name (kebab-case) | Auto-generated | "neural-network-lib" |
| `package_name` | Python package name (snake_case) | Auto-generated | "neural_network_lib" |
| `project_description` | Brief project description | "A modern Python project" | "High-performance neural networks" |

### Author Information

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `author_name` | Your full name | "Your Name" | "Dr. Jane Smith" |
| `author_email` | Your email address | "your.email@example.com" | "jane@university.edu" |
| `github_username` | Your GitHub username | "yourusername" | "janesmith" |

### Technical Configuration

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `python_version` | Minimum Python version | "{{ cookiecutter.python_version }}" | "3.11", "3.12", "3.13", "3.14+" |
| `license` | Project license | "MIT" | "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause" |

### Features (y/n)

| Variable | Description | Default | When to disable |
|----------|-------------|---------|-----------------|
| `include_docker` | Docker support | "y" | Simple libraries only |
| `include_github_actions` | CI/CD workflows | "y" | Private/internal projects |
| `include_pre_commit` | Pre-commit hooks | "y" | Never (always recommended) |
| `include_docs` | MkDocs documentation | "y" | Internal tools only |

## Post-Generation Configuration

After generating your project, you'll need to configure several components:

### 1. Git Repository

```bash
cd your-project
git init
git add .
git commit -m "Initial commit from pythonic-template"

# Create GitHub repository and push
gh repo create your-username/your-project --public
git branch -M main
git remote add origin https://github.com/your-username/your-project.git
git push -u origin main
```

### 2. PyPI Configuration

For publishing packages to PyPI:

#### Using Trusted Publishing (Recommended)

1. Create your package on PyPI:
   - Go to [PyPI](https://pypi.org/manage/account/publishing/)
   - Add a "Pending Publisher" with your GitHub repo details

2. The included GitHub Actions will handle publishing automatically

#### Using API Tokens

```bash
# Store PyPI token as GitHub secret
gh secret set PYPI_API_TOKEN --body "pypi-your-token-here"
```

### 3. Documentation Deployment

The template includes GitHub Pages deployment:

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: "GitHub Actions"

2. **Configure domain** (optional):
   ```yaml
   # In mkdocs.yml
   site_url: https://yourusername.github.io/your-project/
   ```

### 4. Environment Variables

Configure these in your development environment:

#### Required for Development

```bash
# .env file (create in project root)
PYTHONPATH=src
```

#### Optional for Enhanced Features

```bash
# GPU support (if applicable)
CUDA_VISIBLE_DEVICES=0

# Logging configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 5. IDE Configuration

The template includes VS Code configuration, but you may want to customize:

#### VS Code Settings

```json
// .vscode/settings.json (auto-generated)
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": false,  // Using ruff instead
    "ruff.enable": true,
    "ruff.organizeImports": true
}
```

#### PyCharm Configuration

1. **Interpreter**: Point to `.venv/bin/python`
2. **Source roots**: Add `src` directory
3. **Test runner**: Configure pytest
4. **Code style**: Import the Ruff configuration

## Customizing the Template

You can customize the template itself by forking and modifying:

### Template Structure

```
pythonic-template/
├── cookiecutter.json          # Template variables
├── hooks/
│   └── post_gen_project.py   # Post-generation logic
└── {{cookiecutter.repo_name}}/
    ├── src/
    ├── tests/
    ├── pyproject.toml.j2      # Jinja2 templates
    └── ...
```

### Common Customizations

#### 1. Additional Dependencies

Edit `{{cookiecutter.repo_name}}/pyproject.toml`:

```toml
dependencies = [
    {% if cookiecutter.include_ml == "y" -%}
    "numpy>=1.24.0",
    "torch>=2.0.0",
    {%- endif %}
]
```

#### 2. Additional Cookiecutter Variables

Add to `cookiecutter.json`:

```json
{
    "include_ml": ["n", "y"],
    "target_gpu": ["none", "cuda", "rocm"]
}
```

#### 3. Custom Hooks

Modify `hooks/post_gen_project.py`:

```python
"""Post-generation project setup."""
import os
import subprocess

def setup_git():
    """Initialize git repository."""
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

if __name__ == "__main__":
    setup_git()
```

## Advanced Configuration

### 1. Custom Ruff Rules

Modify the generated `pyproject.toml`:

```toml
[tool.ruff.lint]
select = [
    "E", "W",    # pycodestyle
    "F",         # pyflakes  
    "I",         # isort
    "B",         # flake8-bugbear
    "C4",        # flake8-comprehensions
    "UP",        # pyupgrade
    "SIM",       # flake8-simplify
    # Add your custom rules
    "PD",        # pandas-vet
    "NPY",       # numpy-specific
]
```

### 2. Custom pytest Configuration

```toml
[tool.pytest.ini_options]
minversion = "8.0"
pythonpath = "src"
testpaths = ["tests"]
# Add custom markers
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "gpu: marks tests that require GPU",
]
# Custom test discovery
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*", "*Tests"]
python_functions = ["test_*"]
```

### 3. Custom Documentation Theme

```yaml
# mkdocs.yml
theme:
  name: material
  custom_dir: docs/overrides  # Custom templates
  palette:
    - scheme: default
      primary: indigo         # Your brand color
      accent: pink
```

## Next Steps

- **[Learn about the generated project structure](generated-project.md)**
- **[Explore the modern development stack](../features/modern-stack.md)**
- **[Follow best practices](../reference/best-practices.md)**
