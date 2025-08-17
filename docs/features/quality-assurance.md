# Quality Assurance

The Pythonic Template implements comprehensive quality assurance measures to ensure your code is reliable, maintainable, and follows best practices.

## Code Quality Framework 🛡️

The template implements a multi-layered quality assurance approach:

1. **Static Analysis** - Catch issues before runtime
2. **Type Safety** - Prevent type-related bugs
3. **Testing** - Verify functionality works correctly
4. **Formatting** - Maintain consistent code style
5. **Automation** - Run checks automatically

## Static Analysis with Ruff 🔍

Ruff provides comprehensive static analysis covering hundreds of potential issues.

### Rule Categories

The template enables carefully selected rule categories:

```toml
[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors (PEP 8)
    "W",      # pycodestyle warnings
    "F",      # pyflakes (undefined names, unused imports)
    "I",      # isort (import sorting)
    "B",      # flake8-bugbear (likely bugs)
    "C4",     # flake8-comprehensions (better comprehensions)
    "UP",     # pyupgrade (modern Python syntax)
    "SIM",    # flake8-simplify (simplification suggestions)
    "TCH",    # flake8-type-checking (type checking imports)
    "Q",      # flake8-quotes (quote consistency)
    "PL",     # pylint (comprehensive code analysis)
    "PT",     # flake8-pytest-style (pytest best practices)
]
```

### Common Issues Caught

**Undefined Variables**
```python
# ❌ Ruff catches this
def process_data():
    return unknown_variable  # F821: undefined name

# ✅ Correct
def process_data():
    data = load_data()
    return data
```

**Unused Imports**
```python
# ❌ Ruff catches this
import os
import sys  # F401: unused import

def main():
    print(os.getcwd())

# ✅ Ruff auto-fixes
import os

def main():
    print(os.getcwd())
```

**Inefficient Code**
```python
# ❌ Ruff suggests improvement
items = []
for item in data:
    items.append(item.name)  # C401: use list comprehension

# ✅ Better
items = [item.name for item in data]
```

**Modern Python Syntax**
```python
# ❌ Old-style formatting
message = "Hello {}".format(name)  # UP032: use f-strings

# ✅ Modern
message = f"Hello {name}"
```

### Configuration

```toml
[tool.ruff]
line-length = 88          # Black-compatible line length
target-version = "py313"  # Target Python version
fix = true               # Auto-fix when possible

[tool.ruff.lint]
ignore = [
    "E501",   # line-too-long (handled by formatter)
    "PLR0913", # too-many-arguments (sometimes necessary)
]
```

## Type Safety 🔒

The template enforces comprehensive type safety using modern Python typing.

### Type Annotations Everywhere

```python
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import logging

logger: logging.Logger = logging.getLogger(__name__)

def load_config(
    config_path: Path,
    encoding: str = "utf-8",
    defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Union[str, int, float, bool]]:
    """Load configuration from a file.
    
    Parameters
    ----------
    config_path : Path
        Path to the configuration file
    encoding : str, default="utf-8"
        File encoding to use
    defaults : Optional[Dict[str, Any]], default=None
        Default values to use if keys are missing
        
    Returns
    -------
    Dict[str, Union[str, int, float, bool]]
        Loaded configuration data
        
    Raises
    ------
    FileNotFoundError
        If the configuration file doesn't exist
    ValueError
        If the configuration file is malformed
    """
    if defaults is None:
        defaults = {}
        
    try:
        with config_path.open(encoding=encoding) as f:
            # Implementation here
            pass
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
```

### mypy Integration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
strict_optional = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

### Runtime Type Checking (Optional)

For critical applications, enable runtime type checking:

```python
from beartype import beartype

@beartype
def calculate_risk(
    portfolio: List[Dict[str, float]],
    market_data: Dict[str, float]
) -> float:
    """Calculate portfolio risk with runtime type validation."""
    # beartype will validate types at runtime
    return sum(asset["weight"] * market_data[asset["symbol"]] 
               for asset in portfolio)
```

## Comprehensive Testing 🧪

The template includes a robust testing framework with pytest.

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures and configuration
├── test_unit/           # Unit tests
│   ├── test_core.py
│   └── test_utils.py
├── test_integration/    # Integration tests
│   └── test_api.py
└── test_performance/    # Performance tests
    └── test_benchmarks.py
```

### Test Categories

**Unit Tests**
```python
# tests/test_unit/test_core.py
import pytest
from my_package.core import DataProcessor

class TestDataProcessor:
    """Test the DataProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create a DataProcessor instance."""
        return DataProcessor(config={"debug": True})
    
    def test_initialization(self, processor):
        """Test processor initializes correctly."""
        assert processor.config["debug"] is True
        assert processor.is_ready() is True
    
    @pytest.mark.parametrize("input_data,expected", [
        ([1, 2, 3], 6),
        ([0], 0),
        ([], 0),
    ])
    def test_sum_data(self, processor, input_data, expected):
        """Test data summation with various inputs."""
        result = processor.sum_data(input_data)
        assert result == expected
    
    def test_invalid_data_raises_error(self, processor):
        """Test that invalid data raises appropriate error."""
        with pytest.raises(ValueError, match="Data must be numeric"):
            processor.sum_data(["invalid", "data"])
```

**Integration Tests**
```python
# tests/test_integration/test_api.py
import pytest
import tempfile
from pathlib import Path
from my_package import load_config, process_data

class TestAPIIntegration:
    """Test API components working together."""
    
    @pytest.fixture
    def config_file(self):
        """Create a temporary config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"processing": {"enabled": true, "batch_size": 100}}')
            yield Path(f.name)
        Path(f.name).unlink()
    
    def test_end_to_end_processing(self, config_file):
        """Test complete data processing workflow."""
        # Load configuration
        config = load_config(config_file)
        assert config["processing"]["enabled"] is True
        
        # Process data using configuration
        test_data = list(range(1000))
        result = process_data(test_data, config)
        
        # Verify results
        assert len(result) == 10  # 1000 items / batch_size 100
        assert all(isinstance(batch, list) for batch in result)
```

**Performance Tests**
```python
# tests/test_performance/test_benchmarks.py
import pytest
import time
from my_package import heavy_computation

class TestPerformance:
    """Performance benchmarks and regression tests."""
    
    @pytest.mark.slow
    def test_computation_performance(self):
        """Ensure computation stays under performance threshold."""
        start_time = time.time()
        result = heavy_computation(size=10000)
        duration = time.time() - start_time
        
        assert duration < 1.0  # Should complete in under 1 second
        assert len(result) == 10000
    
    @pytest.mark.parametrize("size", [100, 1000, 10000])
    def test_scaling_performance(self, size):
        """Test performance scaling with input size."""
        start_time = time.time()
        result = heavy_computation(size=size)
        duration = time.time() - start_time
        
        # Performance should scale linearly (or better)
        max_expected_time = size / 10000  # 1 second per 10k items
        assert duration <= max_expected_time
```

### Test Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "8.0"
pythonpath = "src"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "gpu: marks tests that require GPU",
]
filterwarnings = [
    "error",
    "ignore::UserWarning",
    "ignore::DeprecationWarning",
]
addopts = [
    "--strict-markers",        # Require marker definitions
    "--strict-config",         # Require valid config
    "--durations=10",         # Show 10 slowest tests
]
```

### Coverage Analysis

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term --cov-fail-under=90

# Coverage configuration
[tool.coverage.run]
source = ["src"]
omit = [
    "tests/*",
    "*/migrations/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

## Pre-commit Quality Gates 🚪

Pre-commit hooks ensure quality standards are maintained automatically.

### Hook Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # Ruff for linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Basic file quality checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
        args: [--strict]

  # Security checks
  - repo: https://github.com/PyCQA/bandit
    rev: '1.7.5'
    hooks:
      - id: bandit
        args: ["-r", "src/"]
        exclude: tests/

  # Documentation
  - repo: https://github.com/pycqa/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        args: [--convention=numpy]
```

### Quality Metrics

The template enforces these quality metrics:

| Metric | Target | Tool | Action |
|--------|--------|------|--------|
| **Code Coverage** | ≥90% | pytest-cov | Fail build if below |
| **Type Coverage** | 100% | mypy | Require all functions typed |
| **Linting Score** | 10/10 | ruff | Fix automatically |
| **Security Score** | No issues | bandit | Block dangerous patterns |
| **Documentation** | 100% | pydocstyle | Require all public APIs documented |

## Continuous Integration 🔄

GitHub Actions provide automated quality assurance in CI/CD.

### CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.13"
    
    - name: Install uv
      run: pip install uv
    
    - name: Install dependencies
      run: uv pip install -e ".[dev]" --system
    
    - name: Run pre-commit
      run: pre-commit run --all-files
    
    - name: Run tests with coverage
      run: pytest --cov=src --cov-report=xml --cov-fail-under=90
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Quality Gates

The CI pipeline enforces these quality gates:

1. **All tests must pass** - No broken functionality
2. **Coverage ≥90%** - Adequate test coverage
3. **No linting errors** - Code quality standards
4. **Type checking passes** - Type safety
5. **Security scan clean** - No security vulnerabilities

## Documentation Quality 📚

The template ensures documentation meets professional standards.

### Docstring Standards

```python
def calculate_metrics(
    data: List[Dict[str, Any]],
    weights: Optional[List[float]] = None,
    method: str = "weighted_average"
) -> Dict[str, float]:
    """Calculate performance metrics from data.
    
    This function computes various performance metrics from input data
    using the specified calculation method. Supports weighted calculations
    when weights are provided.
    
    Parameters
    ----------
    data : List[Dict[str, Any]]
        Input data containing metric values. Each dictionary should have
        at least a 'value' key with numeric data.
    weights : Optional[List[float]], default=None
        Optional weights for each data point. If None, all points are
        weighted equally. Length must match data length.
    method : str, default="weighted_average"
        Calculation method to use. Supported methods:
        - "weighted_average": Weighted average of values
        - "median": Median value (weights ignored)
        - "geometric_mean": Geometric mean of values
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing calculated metrics:
        - "result": Primary metric value
        - "confidence": Confidence score (0-1)
        - "sample_size": Number of data points used
        
    Raises
    ------
    ValueError
        If data is empty, weights length doesn't match data length,
        or method is not supported.
    TypeError
        If data contains non-numeric values.
        
    Examples
    --------
    Basic usage with equal weights:
    
    >>> data = [{"value": 1.0}, {"value": 2.0}, {"value": 3.0}]
    >>> result = calculate_metrics(data)
    >>> result["result"]
    2.0
    
    Weighted calculation:
    
    >>> weights = [0.1, 0.3, 0.6]
    >>> result = calculate_metrics(data, weights=weights)
    >>> result["result"]
    2.5
    
    See Also
    --------
    process_data : Process raw data before metric calculation
    validate_data : Validate data format and values
    
    Notes
    -----
    The weighted average calculation uses the formula:
    
    .. math:: \\bar{x} = \\frac{\\sum_{i=1}^{n} w_i x_i}{\\sum_{i=1}^{n} w_i}
    
    Where :math:`w_i` are the weights and :math:`x_i` are the values.
    """
```

### Documentation Automation

```yaml
# .github/workflows/docs.yml
name: Documentation
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.13"
    
    - name: Install dependencies
      run: |
        pip install uv
        uv pip install -e ".[dev]" --system
    
    - name: Build documentation
      run: mkdocs build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./site
```

## Quality Reporting 📊

The template includes comprehensive quality reporting.

### Coverage Reports

```bash
# Generate detailed coverage report
pytest --cov=src --cov-report=html --cov-report=term --cov-report=json

# View HTML report
open htmlcov/index.html
```

### Code Quality Metrics

```bash
# Comprehensive quality check
make quality

# Individual checks
make lint          # Ruff linting
make format        # Code formatting
make type-check    # mypy type checking
make test          # Run test suite
make security      # Security analysis
```

### Quality Dashboard

The template generates quality metrics that can be tracked:

- **Test Coverage**: Percentage of code covered by tests
- **Type Coverage**: Percentage of code with type annotations
- **Complexity Score**: Cyclomatic complexity metrics
- **Security Score**: Number of security issues found
- **Documentation Score**: Percentage of public APIs documented

## Next Steps

Now that you understand quality assurance:

1. **[Learn about documentation features](documentation.md)**
2. **[Explore DevOps integration](devops.md)**
3. **[Follow best practices](../reference/best-practices.md)**
