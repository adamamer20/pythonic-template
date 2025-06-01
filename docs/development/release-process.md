# Release Process

This document outlines the release process for the Pythonic Template, ensuring consistent, high-quality releases.

## Release Philosophy

Our release process emphasizes:

- **Semantic Versioning** for predictable version numbers
- **Automated Testing** before any release
- **Comprehensive Documentation** for each release
- **Backward Compatibility** whenever possible
- **Clear Communication** about changes

## Versioning Strategy

### Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR:** Breaking changes that require user action
- **MINOR:** New features that are backward compatible
- **PATCH:** Bug fixes that are backward compatible

### Version Examples

```bash
# Bug fix release
1.0.0 → 1.0.1

# New feature release
1.0.1 → 1.1.0

# Breaking change release
1.1.0 → 2.0.0
```

### Pre-release Versions

For development and testing:

```bash
# Alpha releases (early testing)
2.0.0-alpha.1

# Beta releases (feature complete)
2.0.0-beta.1

# Release candidates (final testing)
2.0.0-rc.1
```

## Release Cycle

### Regular Releases

- **Minor releases:** Monthly (if features are ready)
- **Patch releases:** As needed for critical bugs
- **Major releases:** When significant breaking changes accumulate

### Emergency Releases

For critical security fixes or major bugs:

1. **Immediate assessment** of impact
2. **Fast-track testing** on affected areas
3. **Patch release** within 24-48 hours
4. **Post-mortem** to prevent similar issues

## Pre-Release Checklist

### Code Quality Checks

- [ ] All tests passing on CI/CD
- [ ] Code coverage above 90%
- [ ] No critical security vulnerabilities
- [ ] Ruff linting passes without errors
- [ ] Type checking with mypy passes
- [ ] Documentation builds successfully

### Template Testing

- [ ] Template generates without errors
- [ ] Generated project structure is correct
- [ ] All template variables work properly
- [ ] Generated project passes its own tests
- [ ] Development tools work in generated projects

### Documentation Updates

- [ ] CHANGELOG.md updated with all changes
- [ ] Version number updated in pyproject.toml
- [ ] Documentation reflects new features
- [ ] Migration guide for breaking changes (if applicable)
- [ ] README.md updated if needed

### Cross-Platform Testing

- [ ] Tested on Linux
- [ ] Tested on macOS
- [ ] Tested on Windows
- [ ] Tested with Python 3.11, 3.12, 3.13
- [ ] Tested with latest dependency versions

## Release Process Steps

### 1. Preparation Phase

```bash
# Create release branch
git checkout -b release/v1.2.0

# Update version in pyproject.toml
sed -i 's/version = "1.1.0"/version = "1.2.0"/' pyproject.toml

# Update CHANGELOG.md
# Add release notes for version 1.2.0
```

### 2. Testing Phase

```bash
# Run comprehensive tests
pytest --cov=src --cov-report=term

# Test template generation
cookiecutter . --no-input --output-dir /tmp

# Test generated project
cd /tmp/my-python-project
uv pip install -e .[dev]
pytest
ruff check .
mypy src
mkdocs build
```

### 3. Documentation Update

```bash
# Build and verify documentation
mkdocs build
mkdocs serve  # Manual review

# Update changelog
cat >> CHANGELOG.md << EOF
## [1.2.0] - $(date +%Y-%m-%d)

### Added
- New feature X
- Enhanced Y functionality

### Changed
- Improved Z performance

### Fixed
- Bug in A component
EOF
```

### 4. Release Commit

```bash
# Commit release changes
git add .
git commit -m "chore: prepare release v1.2.0"

# Push release branch
git push origin release/v1.2.0
```

### 5. Create Pull Request

Create a pull request from release branch to main:

- **Title:** "Release v1.2.0"
- **Description:** Include changelog and testing summary
- **Labels:** "release"
- **Reviewers:** Assign maintainers

### 6. Final Review and Merge

- [ ] All CI checks pass
- [ ] Code review completed
- [ ] Documentation review completed
- [ ] Testing sign-off received

```bash
# Merge to main
git checkout main
git merge release/v1.2.0
git push origin main
```

### 7. Create Git Tag

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release version 1.2.0

This release includes:
- New feature X
- Enhanced Y functionality
- Bug fixes for A component

See CHANGELOG.md for full details."

# Push tag
git push origin v1.2.0
```

### 8. GitHub Release

Create GitHub release from tag:

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Select tag v1.2.0
4. Title: "v1.2.0"
5. Description: Copy from CHANGELOG.md
6. Mark as pre-release if applicable
7. Publish release

### 9. Post-Release

```bash
# Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0

# Update version to next development version
sed -i 's/version = "1.2.0"/version = "1.3.0-dev"/' pyproject.toml
git add pyproject.toml
git commit -m "chore: bump version to 1.3.0-dev"
git push origin main
```

## Automated Release Pipeline

### GitHub Actions Workflow

Our release pipeline includes:

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12, 3.13]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]
      - name: Run tests
        run: pytest --cov=src
      - name: Test template generation
        run: |
          cookiecutter . --no-input --output-dir /tmp
          cd /tmp/my-python-project
          uv pip install -e .[dev]
          pytest

  release:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
          files: |
            CHANGELOG.md
```

### Automated Checks

The pipeline automatically:

- **Runs tests** on multiple Python versions
- **Tests template generation** end-to-end
- **Validates generated projects** work correctly
- **Creates GitHub release** with automated notes
- **Notifies team** of successful release

## Release Communication

### Changelog Format

We follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.2.0] - 2024-01-15

### Added
- New Docker support in generated projects
- Enhanced GitHub Actions workflows
- Support for Python 3.13

### Changed
- Updated Ruff configuration for better performance
- Improved MkDocs Material theme customization
- Enhanced type checking with stricter mypy settings

### Deprecated
- Old configuration format (will be removed in v2.0.0)

### Fixed
- Bug in template variable substitution
- Issue with Windows path handling
- Documentation build errors with certain configurations

### Security
- Updated dependencies to fix security vulnerabilities
```

### Release Notes Template

```markdown
# Release v1.2.0

This release focuses on improving developer experience and adding modern tooling support.

## 🚀 New Features

- **Docker Support**: Generated projects now include optimized Dockerfile and docker-compose configurations
- **Enhanced CI/CD**: Improved GitHub Actions workflows with better caching and parallel execution
- **Python 3.13**: Full support for the latest Python version

## 🔧 Improvements

- **Better Performance**: Ruff configuration optimized for faster linting
- **Enhanced Documentation**: MkDocs Material theme with better navigation and search
- **Stricter Type Checking**: Improved mypy configuration for better code quality

## 🐛 Bug Fixes

- Fixed template variable substitution in certain edge cases
- Resolved Windows path handling issues
- Fixed documentation build problems with special characters

## 🔐 Security

- Updated all dependencies to latest secure versions
- Added security scanning to CI/CD pipeline

## 📚 Documentation

- Updated getting started guide with new features
- Added troubleshooting section
- Improved configuration examples

## 🙏 Contributors

Thanks to all contributors who made this release possible!

## 📦 Installation

```bash
pip install cookiecutter
cookiecutter https://github.com/your-org/pythonic-template
```

For full installation instructions, see our [Getting Started Guide](../getting-started/quick-start.md).
```

### Communication Channels

- **GitHub Releases:** Detailed technical changelog
- **README.md:** Update with latest version info
- **Documentation:** Update all version references
- **Social Media:** Announce major releases (optional)

## Hotfix Process

### Critical Bug Fixes

For urgent fixes that can't wait for the next regular release:

1. **Create hotfix branch** from latest release tag
2. **Apply minimal fix** with tests
3. **Fast-track testing** on affected functionality
4. **Increment patch version**
5. **Release immediately**

```bash
# Create hotfix branch from tag
git checkout -b hotfix/v1.2.1 v1.2.0

# Apply fix and test
# Update version: 1.2.0 → 1.2.1
# Update CHANGELOG.md

# Commit and tag
git commit -m "fix: critical bug in template generation"
git tag v1.2.1
git push origin v1.2.1

# Merge back to main
git checkout main
git merge hotfix/v1.2.1
git push origin main
```

## Release Metrics

### Success Criteria

- **Zero failed tests** in CI/CD
- **Template generation success rate** > 99%
- **Documentation builds** without errors
- **No critical security vulnerabilities**
- **Community feedback** is positive

### Monitoring

Track release health with:

- **Download/usage statistics**
- **Issue reports** after release
- **Community feedback** and questions
- **Template generation success rates**

## Rollback Procedure

If a release causes critical issues:

1. **Assess impact** and affected users
2. **Prepare rollback** to previous stable version
3. **Communicate clearly** about the rollback
4. **Fix issues** in next release
5. **Post-mortem** to prevent similar problems

```bash
# Emergency rollback
git tag v1.2.0-rollback v1.1.0
git push origin v1.2.0-rollback

# Communicate rollback
# Fix issues
# Prepare new release
```

This structured release process ensures that each version of the Pythonic Template is thoroughly tested, well-documented, and provides a smooth experience for users creating new Python projects.
