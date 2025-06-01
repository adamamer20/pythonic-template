# Changelog

All notable changes to the Pythonic Template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation system with MkDocs Material
- Best practices guide for Python development
- Template variables reference documentation
- Generated project structure documentation
- Development guides (contributing, testing, release process)

### Changed
- Enhanced cookiecutter.json with better default values
- Improved project structure organization
- Updated documentation theme and navigation

## [2.0.0] - 2024-12-15

### Added
- Python 3.13 support as default version
- UV package manager integration for faster dependency management
- Enhanced Ruff configuration with comprehensive rule sets
- Strict mypy configuration for better type safety
- Pre-commit hooks with automated code quality checks
- Docker multi-stage builds for optimized container images
- GitHub Actions workflows with comprehensive CI/CD
- MkDocs Material documentation with API reference generation
- Security scanning with bandit and safety
- Comprehensive test structure with pytest fixtures
- Cross-platform testing (Linux, macOS, Windows)
- Dependabot configuration for automated dependency updates

### Changed
- **BREAKING:** Minimum Python version is now 3.13
- **BREAKING:** Replaced Poetry with UV for dependency management
- **BREAKING:** Updated project structure to follow modern Python packaging
- Enhanced README template with better badges and documentation
- Improved Docker configuration with security best practices
- Updated GitHub issue and PR templates
- Enhanced VS Code configuration with better settings

### Deprecated
- Python 3.10 and 3.11 support (will be removed in v3.0.0)
- Legacy configuration formats

### Removed
- **BREAKING:** Poetry support and pyproject.toml Poetry sections
- **BREAKING:** Old-style setup.py and setup.cfg files
- Outdated linting configurations (flake8, black)
- Legacy GitHub Actions workflow configurations

### Fixed
- Template variable substitution in all configuration files
- Cross-platform path handling in generated projects
- Documentation build issues with certain configurations
- Pre-commit hook compatibility with latest tools

### Security
- Updated all dependencies to latest secure versions
- Added security scanning to CI/CD pipeline
- Implemented non-root Docker user for containers
- Enhanced secret management in CI/CD workflows

## [1.5.2] - 2024-08-20

### Fixed
- Template generation errors on Windows
- Missing dependencies in development environment
- Documentation build failures with mkdocs-material 9.x

### Security
- Updated cookiecutter to fix template injection vulnerability
- Bumped all development dependencies to latest versions

## [1.5.1] - 2024-06-15

### Fixed
- Incorrect Python version constraints in generated pyproject.toml
- Missing .gitignore entries for common Python files
- Pre-commit hook configuration errors

### Changed
- Improved error messages in post-generation hooks
- Enhanced template validation

## [1.5.0] - 2024-05-10

### Added
- Support for Python 3.12
- Enhanced GitHub Actions workflows with caching
- Code coverage reporting with codecov
- Automated release workflows
- Enhanced documentation structure

### Changed
- Updated default Python version to 3.11
- Improved Docker configuration for development
- Enhanced VS Code settings and extensions

### Fixed
- Template variable escaping in YAML files
- Missing development dependencies
- Documentation generation errors

## [1.4.0] - 2024-02-28

### Added
- MkDocs Material documentation system
- API documentation generation with mkdocstrings
- Enhanced project templates with modern structure
- Support for different license types
- Comprehensive .gitignore template

### Changed
- Improved project organization and structure
- Enhanced README template with better documentation
- Updated CI/CD workflows for better performance

### Fixed
- Template rendering issues with special characters
- Missing configuration files in generated projects

## [1.3.0] - 2023-12-10

### Added
- Pre-commit hooks configuration
- Enhanced linting with Ruff
- Type checking with mypy
- Docker support with optimized Dockerfiles
- GitHub issue and PR templates

### Changed
- Migrated from Black + isort to Ruff for formatting
- Updated testing configuration with pytest
- Improved development workflow documentation

### Deprecated
- Black and isort configurations (use Ruff instead)

## [1.2.0] - 2023-09-15

### Added
- Python 3.11 support
- Enhanced GitHub Actions workflows
- Automated dependency updates with Dependabot
- Code quality badges in README
- Enhanced project structure

### Changed
- Updated default Python version to 3.10
- Improved package configuration in pyproject.toml
- Enhanced documentation structure

### Fixed
- Template generation issues with special characters
- Missing development dependencies
- Configuration file syntax errors

## [1.1.0] - 2023-06-20

### Added
- Support for different project licenses
- Enhanced project configuration options
- Improved documentation templates
- VS Code configuration files

### Changed
- Better default project structure
- Enhanced README template
- Improved testing configuration

### Fixed
- Template variable substitution errors
- Missing files in generated projects
- Configuration validation issues

## [1.0.0] - 2023-03-15

### Added
- Initial release of Pythonic Template
- Basic cookiecutter template structure
- Python 3.9+ support
- Poetry for dependency management
- Basic GitHub Actions CI/CD
- Testing setup with pytest
- Code formatting with Black and isort
- Basic documentation structure
- MIT license template
- Standard Python project structure

### Features
- Automated project generation with cookiecutter
- Modern Python packaging with pyproject.toml
- Code quality tools integration
- Basic testing framework
- CI/CD pipeline setup
- Documentation generation
- Development environment configuration

---

## Version History Summary

| Version | Release Date | Python Support | Key Features |
|---------|--------------|----------------|--------------|
| 2.0.0 | 2024-12-15 | 3.13+ | UV, Ruff, Enhanced Docker, Comprehensive CI/CD |
| 1.5.2 | 2024-08-20 | 3.9+ | Bug fixes, Security updates |
| 1.5.1 | 2024-06-15 | 3.9+ | Template fixes, Validation improvements |
| 1.5.0 | 2024-05-10 | 3.9+ | Python 3.12, Enhanced CI/CD, Documentation |
| 1.4.0 | 2024-02-28 | 3.9+ | MkDocs Material, API docs, Project structure |
| 1.3.0 | 2023-12-10 | 3.9+ | Pre-commit, Ruff, mypy, Docker |
| 1.2.0 | 2023-09-15 | 3.9+ | Python 3.11, GitHub Actions, Dependabot |
| 1.1.0 | 2023-06-20 | 3.9+ | License options, VS Code config |
| 1.0.0 | 2023-03-15 | 3.9+ | Initial release, Basic features |

## Migration Guides

### Migrating from 1.x to 2.0.0

The 2.0.0 release includes several breaking changes. Here's how to migrate:

#### 1. Update Python Version

```bash
# Update your Python version
pyenv install 3.13
pyenv global 3.13

# Or with conda
conda install python=3.13
```

#### 2. Migrate from Poetry to UV

```bash
# Remove Poetry files
rm poetry.lock pyproject.toml

# Regenerate project with new template
cookiecutter https://github.com/your-org/pythonic-template

# Install dependencies with UV
pip install uv
uv pip install -e .[dev]
```

#### 3. Update CI/CD Configuration

Replace your existing GitHub Actions workflows with the new comprehensive CI/CD pipeline included in the template.

#### 4. Update Development Tools

```bash
# Remove old tools
pip uninstall black isort flake8

# Install new tools (included in template)
uv pip install ruff mypy pre-commit
```

### Migrating from 1.4.x to 1.5.x

Minor updates required:

1. Update Python version constraints in `pyproject.toml`
2. Add missing .gitignore entries
3. Update pre-commit configuration

### Migrating from 1.2.x to 1.3.x

Replace linting tools:

```bash
# Remove old tools
pip uninstall black isort

# Install Ruff
pip install ruff

# Update configuration in pyproject.toml
```

## Release Notes Guidelines

### Format Standards

Each release includes:

- **Version number** following semantic versioning
- **Release date** in YYYY-MM-DD format
- **Changes categorized** as Added, Changed, Deprecated, Removed, Fixed, Security
- **Migration instructions** for breaking changes
- **Security updates** clearly highlighted

### Change Categories

- **Added:** New features and capabilities
- **Changed:** Changes in existing functionality
- **Deprecated:** Soon-to-be removed features
- **Removed:** Features removed in this version
- **Fixed:** Bug fixes and corrections
- **Security:** Security-related improvements

### Breaking Change Indicators

Breaking changes are marked with **BREAKING:** prefix and include:

- Clear description of what changed
- Migration instructions
- Version when change will take effect
- Workarounds for temporary compatibility

### Security Update Format

Security updates include:

- CVE numbers when applicable
- Severity level (Critical, High, Medium, Low)
- Affected versions
- Mitigation steps
- Credit to security researchers

## Contributing to Changelog

### When to Update

Update the changelog when:

- Adding new features
- Making breaking changes
- Fixing bugs
- Updating dependencies
- Improving security
- Deprecating features

### How to Update

1. Add changes to `[Unreleased]` section
2. Use appropriate category (Added, Changed, etc.)
3. Write clear, user-focused descriptions
4. Include migration notes for breaking changes
5. Reference issue numbers when applicable

### Release Process

When releasing a new version:

1. Move changes from `[Unreleased]` to new version section
2. Add release date
3. Update version links at bottom of file
4. Create git tag matching version number
5. Update documentation with new version

This changelog helps users understand what's changed between versions and how to migrate their projects when necessary.
