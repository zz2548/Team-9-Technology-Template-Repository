import platform
import subprocess
import sys


def main() -> None:
    # Detect operating system
    os_name = platform.system()

    # Set up environment activation and dependency installation
    if os_name == "Windows":
        # First install dependencies
        install_cmd = [
            "powershell",
            "-Command",
            ".venv\\Scripts\\Activate.ps1; uv pip install '.[dev]'",
        ]

        # Then run tests
        test_cmd = [
            "powershell",
            "-Command",
            ".venv\\Scripts\\Activate.ps1; "
            "python -m nose2 -v -s src/calculator/test/; "
            "python -m nose2 -v -s src/logger/test/; "
            "python -m nose2 -v -s src/notifier/test/",
        ]
    else:  # Linux or macOS
        # First install dependencies
        install_cmd = [
            "bash",
            "-c",
            "source .venv/bin/activate && uv pip install '.[dev]'",
        ]

        # Then run tests
        test_cmd = [
            "bash",
            "-c",
            "source .venv/bin/activate && "
            "python -m nose2 -v -s src/calculator/test/ && "
            "python -m nose2 -v -s src/logger/test/ && "
            "python -m nose2 -v -s src/notifier/test/",
        ]

    # Run the installation command
    print("Installing dependencies...")
    install_result = subprocess.run(install_cmd, shell=False, check=False)  # noqa: S603
    if install_result.returncode != 0:
        print("Failed to install dependencies")
        sys.exit(install_result.returncode)

    # Run the test command
    print("Running tests...")
    test_result = subprocess.run(test_cmd, shell=False, check=False)  # noqa: S603
    sys.exit(test_result.returncode)


if __name__ == "__main__":
    main()
