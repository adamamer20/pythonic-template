"""
Basic tests for {{ cookiecutter.package_name }}.
"""

import pytest

import {{ cookiecutter.package_name }}


def test_package_version():
    """Test that the package has a version."""
    assert hasattr({{ cookiecutter.package_name }}, "__version__")
    assert isinstance({{ cookiecutter.package_name }}.__version__, str)
    assert len({{ cookiecutter.package_name }}.__version__) > 0


def test_package_import():
    """Test that the package can be imported."""
    assert {{ cookiecutter.package_name }}.__name__ == "{{ cookiecutter.package_name }}"


@pytest.mark.unit
def test_example_function():
    """Example unit test - replace with your actual tests."""
    # This is a placeholder test - replace with your actual test logic
    assert True


@pytest.mark.integration 
def test_example_integration():
    """Example integration test - replace with your actual tests."""
    # This is a placeholder test - replace with your actual test logic
    assert True


@pytest.mark.slow
def test_example_slow():
    """Example slow test - can be skipped with -m 'not slow'."""
    import time
    time.sleep(0.1)  # Simulate slow operation
    assert True
