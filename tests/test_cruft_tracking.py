#!/usr/bin/env python3
"""Test for cruft tracking functionality."""

import json
import shutil
import re
import subprocess
import tempfile
from pathlib import Path


def test_cruft_commit_is_valid_sha():
    """Test that generated projects have a valid 40-character SHA in .cruft.json."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Compute template path relative to repo root
        ROOT = Path(__file__).resolve().parent.parent
        template_path = ROOT

        # Generate a test project
        uv = shutil.which("uv")
        cmd = [
            *( ["uv", "run"] if uv else [] ),
            "cookiecutter",
            str(template_path),
            "--no-input",
            "--overwrite-if-exists",
            "project_name=Test Project",
            "repo_name=test-project",
            "-o", str(temp_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        assert result.returncode == 0, f"cookiecutter failed:\nSTDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

        # Check .cruft.json
        cruft_file = temp_path / "test-project" / ".cruft.json"
        assert cruft_file.exists(), ".cruft.json file not found"

        # Parse and validate
        data = json.loads(cruft_file.read_text())
        commit = data.get("commit")
        assert commit is not None, "commit field is missing or null"

        # Validate it's a 40-character hex string (full SHA)
        assert re.fullmatch(r"[0-9a-f]{40}", commit), f"Invalid commit SHA format: {commit}"
