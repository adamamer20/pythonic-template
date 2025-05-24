import subprocess, shlex, os, sys, pathlib, json

def run(cmd):
    subprocess.check_call(shlex.split(cmd))

def main():
    run("git init -b main")
    # Ensure pre-commit is installed via uv if not already available
    # This assumes uv is available or installed separately.
    # A more robust solution might involve checking for pre-commit
    # and installing it via pip if uv isn't the primary package manager
    # for the system running cookiecutter. However, the issue implies uv usage.
    try:
        subprocess.check_call(shlex.split("uv tool install pre-commit"))
    except FileNotFoundError:
        print("WARNING: uv command not found. Skipping pre-commit installation via uv.")
        print("Please ensure pre-commit is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install pre-commit using uv: {e}")
        print("Please ensure pre-commit is installed and in your PATH.")

    run("pre-commit install")
    print("✅  Repo initialised. Run `uv pip install -e .[dev]` to enter dev-mode.")

if __name__ == "__main__":
    main()
