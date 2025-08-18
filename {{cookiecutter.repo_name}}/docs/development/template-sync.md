# Template Synchronization

This project was generated from the [pythonic-template](https://github.com/{{ cookiecutter.github_username }}/pythonic-template) cookiecutter template. This guide explains how to keep your project synchronized with template updates.

## Using Cruft

[Cruft](https://cruft.github.io/cruft/) allows you to update your project when the template evolves. It's included in the development dependencies.

### Installation

Cruft is already included in the development dependencies:

```bash
uv sync --all-extras
```

### Checking for Updates

To check if your project is up to date with the template:

```bash
uv run cruft check
```

### Updating from Template

To update your project with the latest template changes:

```bash
uv run cruft update
```

This will:

1. Fetch the latest template version
2. Apply changes to your project
3. Show you any conflicts that need manual resolution

### Handling Conflicts

If there are conflicts during update:

1. Review the changes carefully
2. Resolve conflicts manually
3. Test your project thoroughly
4. Commit the updates

### Configuration

The `.cruft.json` file tracks your template configuration:

- **template**: The template repository URL
- **commit**: The template commit hash your project is based on
- **context**: The cookiecutter variables used when generating your project

## Post-Generation Processing

The template includes dynamic processing that happens after project generation to customize workflow files and documentation based on your Python version configuration.

### Token Replacement

During project generation, the post-generation hook (`hooks/post_gen_project.py`) automatically replaces these tokens in your project files:

| Token | Description | Example |
|-------|-------------|----------|
| `__PY_MIN__` | Minimum Python version | `{{ cookiecutter.python_version }}` |
| `__PY_MATRIX__` | Python version matrix for CI | `["{{ cookiecutter.python_version }}", "3.14"]` |
| `__PY_MAX__` | Maximum supported Python version | Latest available version |
| `__PY_SHORT__` | Digits-only short version used to build Ruff target | `{% raw %}{{ cookiecutter.python_version | replace('.', '') }}{% endraw %}` |
| `__PY_CLASSIFIERS__` | Python classifier strings for pyproject.toml | Generated based on supported versions |
| `__RELEASE_DATE__` | Current date for changelog | Today's date in YYYY-MM-DD format |

### Files Affected by Token Replacement

The following files are processed for token replacement:

- `.github/workflows/ci.yml` - CI matrix and Python version references
- `.github/workflows/docs.yml` - Documentation build Python version
- `.github/workflows/publish.yml` - Publishing workflow Python version
- `.github/workflows/render-paper.yml` - Paper rendering workflow Python version (when `project_type` is "paper")
- `README.md` - Python version requirements
- `pyproject.toml` - Python version constraints and classifiers
- `docs/development/changelog.md` - Release date placeholder

### Understanding the Process

This token replacement system enables:

1. **Dynamic CI matrices**: Your CI automatically tests against the Python versions you specify
2. **Consistent versioning**: All files stay in sync with your chosen minimum Python version
3. **Future compatibility**: Easy updates when new Python versions are released
4. **Template flexibility**: Same template works for different Python version requirements

### Customizing Token Processing

If you need to modify this behavior, you can:

1. **Update the hook**: Edit `hooks/post_gen_project.py` in the template
2. **Add new tokens**: Define additional replacements in the token dictionary
3. **Extend file coverage**: Add more files to the `target_files` list

**Note**: These tokens are replaced only during initial project generation. When updating via Cruft, you may need to manually reconcile changes related to Python version configuration.

## Alternative: Manual Updates

If you prefer not to use Cruft, you can manually sync changes:

1. Check the [template changelog](https://github.com/{{ cookiecutter.github_username }}/pythonic-template/blob/main/CHANGELOG.md)
2. Review differences between template versions
3. Apply relevant changes to your project manually
4. Test thoroughly

## Best Practices

- **Regular Updates**: Check for template updates regularly
- **Test After Updates**: Always run your full test suite after updating
- **Review Changes**: Don't blindly accept all changes - review what's being updated
- **Backup First**: Consider creating a branch before major template updates
- **Custom Modifications**: Document any custom changes that might conflict with template updates

## Getting Help

If you encounter issues with template synchronization:

1. Check the [template documentation](https://github.com/{{ cookiecutter.github_username }}/pythonic-template)
2. Review the [Cruft documentation](https://cruft.github.io/cruft/)
3. Open an issue in the template repository
