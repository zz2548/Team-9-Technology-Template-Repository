# Team-9-Technology-Template-Repository
# Python Project Template with UV

## Description
A modern Python project template featuring comprehensive test coverage, continuous integration with CircleCI, and dependency management using UV. This template includes configurations for static type checking, code formatting, and automated testing.

## Prerequisites
* Python 3.10 or higher
* UV for Python dependency management

## Project Setup

1. Clone the repository:
    ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install UV:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create a virtual environment:
   ```bash
   uv venv .venv
   ```
   
   Activate the virtual environment:
   - On Unix/Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. Install dependencies and pre-commit hooks:
    ```bash
    uv pip install ".[dev]"
    pre-commit install
    ```
## Development Tools

### Static Analysis
Run type checking and code linting:
```bash
mypy src tests
ruff check . --config pyproject.toml
```

### Testing
The project includes unit, integration, and end-to-end tests:

#### Running Individual Test Suites
```bash
# Run calculator unit tests
nose2 -v -s src/calculator/test/

# Run logger unit tests
nose2 -v -s src/logger/test/

# Run notifier unit tests
nose2 -v -s src/notifier/test/
```

#### Running Tests with Coverage
```bash
# Running all unit tests with coverage
nose2 -v -s src/calculator/test/ --with-coverage --coverage=src.calculator

COVERAGE_FILE=.coverage.logger nose2 -v -s src/logger/test/ --with-coverage --coverage=src.logger

COVERAGE_FILE=.coverage.notifier nose2 -v -s src/notifier/test/ --with-coverage --coverage=src.notifier

coverage combine .coverage .coverage.logger .coverage.notifier

coverage report --fail-under=70
coverage xml -o unit-coverage.xml
coverage html -d unit-htmlcov
```
> **Note**: The above commands work in a bash environment. You might need to adjust commands for your specific terminal.

#### Other Test Types
```bash
# Run integration tests
nose2 -v -s tests/integration

# Run end-to-end tests
nose2 -v -s tests/e2e

# Run all tests
nose2
```

### Coverage Reports
Test coverage reports are generated in HTML format. View them by opening `htmlcov/index.html` in your browser.

## Continuous Integration
This project uses CircleCI for continuous integration, which:
- Runs static analysis (mypy and ruff)
- Executes all test suites
- Generates and stores test reports
- Enforces minimum test coverage requirements

## Contributing

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```

2. Install pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

   The pre-commit hooks will automatically:
   - Format your code using ruff-format
   - Check for linting issues with ruff
   - Verify type annotations with mypy
   - Run unit tests to ensure all tests pass

4. Push your changes and create a pull request:
   ```bash
   git push origin feature-name
   ```

If pre-commit identifies any issues, it will prevent the commit and display what needs to be fixed. Address the issues and try committing again.

## License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Additional Resources
- [UV Documentation](https://github.com/astral-sh/uv)
- [CircleCI Documentation](https://circleci.com/docs/)
- [nose2 Documentation](https://docs.nose2.io/en/latest/)