# Best Practices Guide

This guide outlines best practices for Python development using the Pythonic Template, covering code quality, project organization, and development workflows.

## Code Quality Standards

### Type Hints and Static Analysis

Always use type hints for better code clarity and IDE support:

```python
from typing import Optional, List, Dict, Any
from pathlib import Path

def process_data(
    input_file: Path,
    output_dir: Optional[Path] = None,
    config: Dict[str, Any] = None
) -> List[str]:
    """Process data from input file.
    
    Parameters
    ----------
    input_file : Path
        Path to the input file.
    output_dir : Optional[Path], default=None
        Output directory. If None, uses current directory.
    config : Dict[str, Any], default=None
        Processing configuration.
        
    Returns
    -------
    List[str]
        List of processed items.
    """
    if config is None:
        config = {}
    
    if output_dir is None:
        output_dir = Path.cwd()
    
    # Implementation here
    return []
```

### Documentation Standards

#### Docstring Format

Use NumPy-style docstrings for consistency:

```python
def calculate_metrics(
    data: List[float],
    method: str = "mean",
    weights: Optional[List[float]] = None
) -> Dict[str, float]:
    """Calculate statistical metrics for the given data.
    
    This function computes various statistical metrics based on the
    specified method and optional weights.
    
    Parameters
    ----------
    data : List[float]
        Input data points for calculation.
    method : str, default="mean"
        Calculation method. Options: "mean", "median", "weighted".
    weights : Optional[List[float]], default=None
        Weights for weighted calculations. Must match data length.
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing calculated metrics with keys:
        - "value": The calculated metric value
        - "std": Standard deviation
        - "count": Number of data points
        
    Raises
    ------
    ValueError
        If data is empty or weights length doesn't match data.
    TypeError
        If method is not a valid string option.
        
    Examples
    --------
    >>> data = [1.0, 2.0, 3.0, 4.0, 5.0]
    >>> result = calculate_metrics(data, method="mean")
    >>> result["value"]
    3.0
    
    >>> weights = [1, 2, 3, 2, 1]
    >>> result = calculate_metrics(data, method="weighted", weights=weights)
    >>> round(result["value"], 2)
    2.89
    """
```

#### Code Comments

Write clear, purposeful comments:

```python
# Good: Explains why, not what
# Use exponential backoff to handle rate limiting
retry_delay = 2 ** attempt

# Bad: States the obvious
# Increment counter by 1
counter += 1

# Good: Explains complex logic
# Calculate weighted average where recent values have higher weights
# using exponential decay (newer values get weight closer to 1.0)
weights = [math.exp(-0.1 * i) for i in range(len(values))]
```

### Error Handling

#### Exception Hierarchy

Create meaningful exception hierarchies:

```python
class ProjectError(Exception):
    """Base exception for project-specific errors."""
    pass

class ConfigurationError(ProjectError):
    """Raised when configuration is invalid."""
    pass

class ProcessingError(ProjectError):
    """Raised when data processing fails."""
    pass

class ValidationError(ProjectError):
    """Raised when data validation fails."""
    pass
```

#### Error Handling Patterns

Use specific exception handling:

```python
from pathlib import Path
import json

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from JSON file.
    
    Parameters
    ----------
    config_path : Path
        Path to configuration file.
        
    Returns
    -------
    Dict[str, Any]
        Configuration dictionary.
        
    Raises
    ------
    ConfigurationError
        If file doesn't exist, is not valid JSON, or has invalid structure.
    """
    try:
        with config_path.open() as f:
            config = json.load(f)
    except FileNotFoundError:
        raise ConfigurationError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise ConfigurationError(f"Invalid JSON in config file: {e}")
    except PermissionError:
        raise ConfigurationError(f"Permission denied reading config: {config_path}")
    
    # Validate configuration structure
    required_keys = ["database", "api", "logging"]
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ConfigurationError(f"Missing required config keys: {missing_keys}")
    
    return config
```

## Project Organization

### Package Structure

Organize code logically with clear separation of concerns:

```
src/my_project/
├── __init__.py              # Package initialization and public API
├── main.py                  # CLI entry point
├── config.py                # Configuration management
├── exceptions.py            # Custom exceptions
├── core/                    # Core business logic
│   ├── __init__.py
│   ├── models.py           # Data models
│   ├── services.py         # Business services
│   └── processors.py       # Data processors
├── data/                   # Data handling
│   ├── __init__.py
│   ├── loaders.py          # Data loading
│   ├── validators.py       # Data validation
│   └── transformers.py     # Data transformation
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── helpers.py          # General helpers
│   ├── decorators.py       # Custom decorators
│   └── constants.py        # Project constants
└── integrations/           # External integrations
    ├── __init__.py
    ├── database.py         # Database connections
    ├── api_client.py       # API clients
    └── storage.py          # File/object storage
```

### Configuration Management

Use structured configuration with validation:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os

@dataclass
class DatabaseConfig:
    """Database configuration."""
    host: str
    port: int
    database: str
    username: str
    password: str
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")
        if not self.database:
            raise ValueError("Database name cannot be empty")

@dataclass
class AppConfig:
    """Application configuration."""
    debug: bool = False
    log_level: str = "INFO"
    data_dir: Path = Path("data")
    database: Optional[DatabaseConfig] = None
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            data_dir=Path(os.getenv("DATA_DIR", "data")),
            database=DatabaseConfig(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "5432")),
                database=os.getenv("DB_NAME", "myproject"),
                username=os.getenv("DB_USER", "user"),
                password=os.getenv("DB_PASSWORD", ""),
            ) if os.getenv("DB_HOST") else None
        )
```

## Testing Best Practices

### Test Organization

Structure tests to mirror source code:

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_main.py             # Test main module
├── test_config.py           # Test configuration
├── core/                    # Test core modules
│   ├── test_models.py
│   ├── test_services.py
│   └── test_processors.py
├── data/                    # Test data modules
│   ├── test_loaders.py
│   ├── test_validators.py
│   └── test_transformers.py
├── utils/                   # Test utilities
│   ├── test_helpers.py
│   └── test_decorators.py
├── integration/             # Integration tests
│   ├── test_database.py
│   └── test_api.py
└── fixtures/                # Test data files
    ├── sample_data.json
    └── test_config.yaml
```

### Test Writing Guidelines

Write clear, focused tests:

```python
import pytest
from unittest.mock import Mock, patch
from my_project.core.services import DataService
from my_project.exceptions import ValidationError

class TestDataService:
    """Test suite for DataService."""
    
    def test_process_valid_data_returns_expected_result(self):
        """Test that valid data is processed correctly."""
        # Arrange
        service = DataService()
        input_data = {"value": 10, "multiplier": 2}
        expected = {"result": 20, "status": "success"}
        
        # Act
        result = service.process(input_data)
        
        # Assert
        assert result == expected
    
    def test_process_invalid_data_raises_validation_error(self):
        """Test that invalid data raises ValidationError."""
        # Arrange
        service = DataService()
        invalid_data = {"value": "not_a_number"}
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.process(invalid_data)
        
        assert "Invalid value type" in str(exc_info.value)
    
    @patch('my_project.core.services.external_api_call')
    def test_process_with_external_api_failure(self, mock_api):
        """Test handling of external API failures."""
        # Arrange
        mock_api.side_effect = ConnectionError("API unavailable")
        service = DataService()
        data = {"value": 10}
        
        # Act & Assert
        with pytest.raises(ProcessingError) as exc_info:
            service.process(data)
        
        assert "External service unavailable" in str(exc_info.value)
        mock_api.assert_called_once()
```

### Fixtures and Test Data

Create reusable fixtures:

```python
# conftest.py
import pytest
from pathlib import Path
import tempfile
import json

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "database": "test_db"
        },
        "api": {
            "timeout": 30,
            "retries": 3
        }
    }

@pytest.fixture
def config_file(temp_dir, sample_config):
    """Create a temporary config file."""
    config_path = temp_dir / "config.json"
    with config_path.open("w") as f:
        json.dump(sample_config, f)
    return config_path

@pytest.fixture
def mock_database():
    """Mock database connection."""
    return Mock()
```

## Performance Best Practices

### Efficient Data Processing

Use appropriate data structures and algorithms:

```python
from collections import defaultdict, Counter
from typing import List, Dict, Set
import bisect

def find_duplicates_efficient(items: List[str]) -> Set[str]:
    """Find duplicate items efficiently using Counter."""
    counts = Counter(items)
    return {item for item, count in counts.items() if count > 1}

def group_by_key_efficient(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    """Group items by key efficiently using defaultdict."""
    groups = defaultdict(list)
    for item in items:
        groups[item[key]].append(item)
    return dict(groups)

def binary_search_insert(sorted_list: List[int], value: int) -> int:
    """Insert value into sorted list maintaining order."""
    index = bisect.bisect_left(sorted_list, value)
    sorted_list.insert(index, value)
    return index
```

### Memory Management

Handle large datasets efficiently:

```python
from typing import Iterator, Any
import csv

def process_large_file_generator(file_path: Path) -> Iterator[Dict[str, Any]]:
    """Process large CSV file using generator to save memory."""
    with file_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Process row
            processed_row = transform_row(row)
            if is_valid_row(processed_row):
                yield processed_row

def batch_process(items: Iterator[Any], batch_size: int = 1000) -> Iterator[List[Any]]:
    """Process items in batches to control memory usage."""
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    if batch:  # Yield remaining items
        yield batch
```

## Security Best Practices

### Input Validation

Always validate and sanitize inputs:

```python
import re
from pathlib import Path
from typing import Any, Dict

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    # Remove directory traversal attempts
    filename = filename.replace('..', '')
    filename = filename.replace('/', '_')
    filename = filename.replace('\\', '_')
    
    # Remove null bytes
    filename = filename.replace('\x00', '')
    
    # Limit length
    return filename[:255]

def validate_config_schema(config: Dict[str, Any]) -> None:
    """Validate configuration against expected schema."""
    required_fields = ['database', 'api_key', 'timeout']
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Required field missing: {field}")
    
    if not isinstance(config['timeout'], (int, float)):
        raise ValueError("Timeout must be a number")
    
    if config['timeout'] <= 0:
        raise ValueError("Timeout must be positive")
```

### Secrets Management

Handle secrets securely:

```python
import os
from pathlib import Path
from typing import Optional

def get_secret(secret_name: str, default: Optional[str] = None) -> str:
    """Get secret from environment or file."""
    # Try environment variable first
    value = os.getenv(secret_name)
    if value:
        return value
    
    # Try Docker secrets
    secret_path = Path(f"/run/secrets/{secret_name.lower()}")
    if secret_path.exists():
        return secret_path.read_text().strip()
    
    # Use default if provided
    if default is not None:
        return default
    
    raise ValueError(f"Secret not found: {secret_name}")

# Usage
DATABASE_PASSWORD = get_secret("DATABASE_PASSWORD")
API_KEY = get_secret("API_KEY")
```

## Deployment Best Practices

### Docker Optimization

Create efficient Docker images:

```dockerfile
# Multi-stage build for smaller images
FROM python:3.13-slim as builder

# Install UV for fast dependency resolution
RUN pip install uv

WORKDIR /app

# Copy only dependency files first (better caching)
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv pip install --system .

# Runtime stage
FROM python:3.13-slim

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

WORKDIR /app

# Copy source code
COPY src/ ./src/

# Set proper ownership
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import my_project; print('OK')" || exit 1

# Use exec form for proper signal handling
ENTRYPOINT ["python", "-m", "my_project"]
```

### Environment Configuration

Use environment-specific configurations:

```python
import os
from enum import Enum

class Environment(Enum):
    """Application environments."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

def get_environment() -> Environment:
    """Get current environment."""
    env_name = os.getenv("ENVIRONMENT", "development").lower()
    try:
        return Environment(env_name)
    except ValueError:
        raise ValueError(f"Invalid environment: {env_name}")

def get_config_for_environment(env: Environment) -> Dict[str, Any]:
    """Get configuration for specific environment."""
    base_config = {
        "log_level": "INFO",
        "debug": False,
        "timeout": 30,
    }
    
    env_configs = {
        Environment.DEVELOPMENT: {
            "log_level": "DEBUG",
            "debug": True,
            "database_url": "sqlite:///dev.db",
        },
        Environment.TESTING: {
            "log_level": "WARNING",
            "database_url": "sqlite:///:memory:",
        },
        Environment.PRODUCTION: {
            "log_level": "ERROR",
            "database_url": get_secret("DATABASE_URL"),
            "timeout": 60,
        },
    }
    
    config = base_config.copy()
    config.update(env_configs.get(env, {}))
    return config
```

## Continuous Integration

### Comprehensive Testing Pipeline

Configure thorough CI checks:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: 3.13
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]
      - name: Run Ruff linting
        run: ruff check .
      - name: Run Ruff formatting
        run: ruff format --check .
      - name: Run mypy
        run: mypy src

  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.11, 3.12, 3.13]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.13'
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: 3.13
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]
      - name: Run security checks
        run: bandit -r src
      - name: Check for vulnerabilities
        run: safety check
```

These best practices ensure that projects generated from the Pythonic Template are maintainable, secure, and follow modern Python development standards.
