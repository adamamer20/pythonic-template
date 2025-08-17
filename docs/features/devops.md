# DevOps Integration

The Pythonic Template provides comprehensive DevOps integration with automated CI/CD pipelines, deployment workflows, and infrastructure management using modern tools and best practices.

## CI/CD Philosophy 🔄

The template implements a robust CI/CD strategy based on these principles:

- **🚀 Automate everything** - From testing to deployment
- **🛡️ Quality gates** - Block bad code from reaching production
- **📦 Consistent builds** - Reproducible across environments
- **🔄 Fast feedback** - Quick notification of issues
- **🎯 Zero-downtime deployment** - Seamless updates

## GitHub Actions Workflows 🤖

The template includes comprehensive GitHub Actions workflows for all aspects of the development lifecycle.

### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv pip install -e ".[dev]" --system

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Check types with mypy
        run: mypy src/

  test:
    name: Test Suite
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macOS-latest]
        python-version: ["3.11", "3.12", "3.13"]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv pip install -e ".[dev]" --system

      - name: Run tests
        run: pytest --cov=src --cov-report=xml --cov-fail-under=90

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.13'
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install uv bandit safety
          uv pip install -e ".[dev]" --system

      - name: Run security checks
        run: |
          bandit -r src/
          safety check --json

      - name: Run CodeQL analysis
        uses: github/codeql-action/analyze@v2
        with:
          languages: python
```

### Package Publishing

```yaml
# .github/workflows/publish.yml
name: Publish Package
on:
  release:
    types: [published]

jobs:
  build:
    name: Build Package
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install build tools
        run: |
          pip install uv
          uv pip install build twine --system

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  publish-pypi:
    name: Publish to PyPI
    needs: build
    runs-on: ubuntu-latest
    environment: release
    permissions:
      id-token: write  # For trusted publishing
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

  publish-github:
    name: Publish to GitHub Packages
    needs: build
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Configure GitHub Package Registry
        run: |
          echo "//npm.pkg.github.com/:_authToken=${{ secrets.GITHUB_TOKEN }}" > .npmrc
          pip config set global.index-url https://pypi.org/simple/
          pip config set global.extra-index-url https://pypi.pkg.github.com/simple/

      - name: Publish to GitHub Packages
        run: |
          pip install twine
          twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.GITHUB_TOKEN }}
```

### Documentation Deployment

```yaml
# .github/workflows/docs.yml
name: Documentation
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    name: Build Documentation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[dev]" --system

      - name: Build documentation
        run: mkdocs build --strict

      - name: Upload documentation artifacts
        uses: actions/upload-artifact@v3
        with:
          name: documentation
          path: site/

  deploy:
    name: Deploy Documentation
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Download documentation artifacts
        uses: actions/download-artifact@v3
        with:
          name: documentation
          path: site/

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload to GitHub Pages
        uses: actions/upload-pages-artifact@v2
        with:
          path: site/

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

## Dependency Management 📦

The template includes automated dependency management using Dependabot and uv.

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "username"
    assignees:
      - "username"
    commit-message:
      prefix: "deps"
      include: "scope"
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "ci"

  # Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "docker"
```

### Automated Dependency Updates

```yaml
# .github/workflows/dependency-updates.yml
name: Dependency Updates
on:
  schedule:
    - cron: "0 9 * * 1"  # Monday 9 AM
  workflow_dispatch:

jobs:
  update:
    name: Update Dependencies
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install uv
        run: pip install uv

      - name: Update dependencies
        run: |
          uv pip compile pyproject.toml --upgrade --output-file requirements.lock
          
      - name: Run tests with updated dependencies
        run: |
          uv pip install -r requirements.lock
          pytest

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: "deps: update Python dependencies"
          title: "Update Python dependencies"
          body: |
            Automated dependency update.
            
            - Updated all dependencies to latest compatible versions
            - All tests pass with updated dependencies
            
            Please review the changes before merging.
          branch: update-dependencies
          delete-branch: true
```

## Container Support 🐳

The template includes comprehensive Docker support for development and deployment.

### Development Dockerfile

```dockerfile
# Dockerfile
FROM python:3.13-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Development stage
FROM base as development

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies
RUN uv pip install -e ".[dev]" --system

# Copy source code
COPY . .

# Set default command
CMD ["pytest"]

# Production stage
FROM base as production

# Copy dependency files
COPY pyproject.toml README.md ./

# Install only production dependencies
RUN uv pip install . --system

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Set default command
CMD ["python", "-m", "my_package"]
```

### Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - pip-cache:/root/.cache/pip
    environment:
      - PYTHONPATH=/app/src
      - DEBUG=true
    ports:
      - "8000:8000"
    command: pytest --watch

  docs:
    build:
      context: .
      target: development
    volumes:
      - .:/app
    ports:
      - "8080:8000"
    command: mkdocs serve --dev-addr 0.0.0.0:8000

  test:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - test-results:/app/test-results
    environment:
      - COVERAGE_FILE=/app/test-results/.coverage
    command: pytest --cov=src --cov-report=html:/app/test-results/htmlcov

volumes:
  pip-cache:
  test-results:
```

### Container Registry Publishing

```yaml
# .github/workflows/docker.yml
name: Docker
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    name: Build and Push
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          target: production
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Release Management 🚀

The template includes automated release management with semantic versioning.

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    if: "!contains(github.event.head_commit.message, 'skip ci')"
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install semantic-release --system

      - name: Run semantic release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: semantic-release publish

      - name: Update changelog
        run: semantic-release changelog

      - name: Commit changelog
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add CHANGELOG.md
          git commit -m "docs: update changelog [skip ci]" || exit 0
          git push
```

### Semantic Release Configuration

```toml
# pyproject.toml
[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
branch = "main"
upload_to_pypi = true
upload_to_release = true
build_command = "uv build"
commit_message = "chore: release {version} [skip ci]"

[tool.semantic_release.commit_parser_options]
allowed_tags = ["build", "chore", "ci", "docs", "feat", "fix", "perf", "style", "refactor", "test"]
minor_tags = ["feat"]
patch_tags = ["fix", "perf"]

[tool.semantic_release.changelog]
template_dir = "templates"
changelog_file = "CHANGELOG.md"
exclude_commit_patterns = [
    "^Merge pull request",
    "^Merge branch",
]
```

## Monitoring and Observability 📊

The template includes tools for monitoring application health and performance.

### Health Checks

```python
# src/my_package/health.py
"""Health check endpoints for monitoring."""

import time
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    """Health check status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    """Health check result."""
    status: HealthStatus
    timestamp: float
    duration_ms: float
    details: Dict[str, Any]

def check_database() -> HealthCheck:
    """Check database connectivity."""
    start_time = time.time()
    try:
        # Database connection check
        duration = (time.time() - start_time) * 1000
        return HealthCheck(
            status=HealthStatus.HEALTHY,
            timestamp=time.time(),
            duration_ms=duration,
            details={"connection": "ok", "query_time_ms": duration}
        )
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        return HealthCheck(
            status=HealthStatus.UNHEALTHY,
            timestamp=time.time(),
            duration_ms=duration,
            details={"error": str(e)}
        )

def check_external_service() -> HealthCheck:
    """Check external service availability."""
    # Implementation here
    pass

def get_system_health() -> Dict[str, HealthCheck]:
    """Get overall system health."""
    return {
        "database": check_database(),
        "external_service": check_external_service(),
    }
```

### Metrics Collection

```python
# src/my_package/metrics.py
"""Application metrics collection."""

import time
import functools
from typing import Dict, Any, Callable
from collections import defaultdict, deque

class MetricsCollector:
    """Simple metrics collector."""
    
    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
    
    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter."""
        self.counters[name] += value
    
    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge value."""
        self.gauges[name] = value
    
    def observe(self, name: str, value: float) -> None:
        """Observe a value for histogram."""
        self.histograms[name].append(value)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        return {
            "counters": dict(self.counters),
            "gauges": self.gauges.copy(),
            "histograms": {
                name: {
                    "count": len(values),
                    "sum": sum(values),
                    "avg": sum(values) / len(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                }
                for name, values in self.histograms.items()
            }
        }

# Global metrics instance
metrics = MetricsCollector()

def timed(metric_name: str) -> Callable:
    """Decorator to time function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                metrics.increment(f"{metric_name}.success")
                return result
            except Exception as e:
                metrics.increment(f"{metric_name}.error")
                raise
            finally:
                duration = time.time() - start_time
                metrics.observe(f"{metric_name}.duration", duration)
        return wrapper
    return decorator
```

## Infrastructure as Code 🏗️

The template supports infrastructure as code for cloud deployments.

### Terraform Configuration

```hcl
# infrastructure/main.tf
terraform {
  required_version = ">=1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Application container
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.app_cpu
  memory                   = var.app_memory
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "app"
      image = "${var.container_image}"
      
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "ENV"
          value = var.environment
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.app.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

# Load balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = var.public_subnet_ids

  enable_deletion_protection = false
}

resource "aws_lb_target_group" "app" {
  name     = "${var.project_name}-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
}
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-package-app
  labels:
    app: my-package
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-package
  template:
    metadata:
      labels:
        app: my-package
    spec:
      containers:
      - name: app
        image: ghcr.io/username/my-package:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: my-package-service
spec:
  selector:
    app: my-package
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Security Best Practices 🔒

The template implements security best practices throughout the DevOps pipeline.

### Security Scanning

```yaml
# .github/workflows/security.yml
name: Security
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM

jobs:
  dependency-check:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install uv safety
          uv pip install -e ".[dev]" --system

      - name: Run safety check
        run: safety check --json --output safety-report.json

      - name: Upload safety report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: safety-report
          path: safety-report.json

  code-scan:
    name: Static Code Analysis
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run bandit security scan
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json

      - name: Upload bandit report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: bandit-report
          path: bandit-report.json

  container-scan:
    name: Container Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t test-image .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'test-image'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Secret Management

```yaml
# Example GitHub secrets configuration
secrets:
  PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

## Performance Monitoring 📈

The template includes performance monitoring and optimization tools.

### Performance Testing

```python
# tests/test_performance.py
"""Performance tests and benchmarks."""

import pytest
import time
from my_package import heavy_computation

class TestPerformance:
    """Performance benchmarks."""
    
    @pytest.mark.performance
    def test_computation_speed(self):
        """Benchmark computation performance."""
        data_sizes = [100, 1000, 10000]
        
        for size in data_sizes:
            start_time = time.time()
            result = heavy_computation(size)
            duration = time.time() - start_time
            
            # Assert performance requirements
            assert duration < size / 1000  # Linear scaling
            assert len(result) == size
            
    @pytest.mark.benchmark
    def test_memory_usage(self):
        """Test memory efficiency."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        
        # Run memory-intensive operation
        large_data = heavy_computation(100000)
        
        memory_after = process.memory_info().rss
        memory_used = memory_after - memory_before
        
        # Assert memory usage is reasonable
        assert memory_used < 100 * 1024 * 1024  # Less than 100MB
```

### Continuous Performance Monitoring

```yaml
# .github/workflows/performance.yml
name: Performance
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  benchmark:
    name: Performance Benchmarks
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install uv pytest-benchmark
          uv pip install -e ".[dev]" --system

      - name: Run benchmarks
        run: pytest tests/test_performance.py --benchmark-json=benchmark.json

      - name: Store benchmark results
        uses: benchmark-action/github-action-benchmark@v1
        with:
          tool: 'pytest'
          output-file-path: benchmark.json
          github-token: ${{ secrets.GITHUB_TOKEN }}
          auto-push: true
```

## Next Steps

Now that you understand DevOps integration:

1. **[Explore development workflows](../development/contributing.md)**
2. **[Learn about template variables](../reference/template-variables.md)**
3. **[Follow best practices](../reference/best-practices.md)**
