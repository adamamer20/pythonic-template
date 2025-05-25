{%- if cookiecutter.use_docker == 'y' %}
FROM python:{{ cookiecutter.python_version }}-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fish \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally
RUN pip install uv

# Create non-root user
RUN useradd --create-home --shell /usr/bin/fish dev
USER dev
WORKDIR /home/dev

# Set fish as default shell for the user
SHELL ["/usr/bin/fish", "-l", "-c"]

# Copy project files
COPY --chown=dev:dev . /workspace
WORKDIR /workspace

# Install Python dependencies
RUN uv pip install --system -e .[dev]

# Install pre-commit hooks
RUN pre-commit install

# Set fish as the default shell
CMD ["/usr/bin/fish", "-l"]
{%- endif %}
