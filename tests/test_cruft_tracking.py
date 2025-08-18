#!/usr/bin/env python3
"""Test for cruft tracking functionality."""

import json
import re
import subprocess
import tempfile
from pathlib import Path


def test_cruft_commit_is_valid_sha():
    """Test that generated projects have a valid 40-character SHA in .cruft.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Generate a test project
        result = subprocess.run([
            "cookiecutter", 
            "/home/aamer1/pythonic-template",
            "--no-input",
            "--overwrite-if-exists",
            "project_name=Test Project",
            "repo_name=test-project",
            "-o", str(temp_path)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"cookiecutter failed: {result.stderr}")
            return False
            
        # Check .cruft.json
        cruft_file = temp_path / "test-project" / ".cruft.json"
        if not cruft_file.exists():
            print(".cruft.json file not found")
            return False
            
        # Parse and validate
        data = json.loads(cruft_file.read_text())
        commit = data.get("commit")
        
        if not commit:
            print("commit field is missing or null")
            return False
            
        # Validate it's a 40-character hex string (full SHA)
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            print(f"Invalid commit SHA format: {commit}")
            return False
            
        print(f"✓ Valid commit SHA: {commit[:8]}...")
        return True


if __name__ == "__main__":
    success = test_cruft_commit_is_valid_sha()
    exit(0 if success else 1)