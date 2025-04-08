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
mypy src
ruff check . --config pyproject.toml
```

### Testing
The project includes unit, integration, and end-to-end tests:

#### Running Individual Test Suites
```bash
# Run calculator unit tests with pytest
pytest src/calculator/test/ --cov=src.calculator

# Run logger unit tests with pytest
pytest src/logger/test/ --cov=src.logger

# Run notifier unit tests with pytest
pytest src/notifier/test/ --cov=src.notifier

# Specific nose2 test for calculator
nose2 -v src.calculator.test.test_calculator_nose2 --with-coverage --coverage=src.calculator
```

#### Running Integration and E2E Tests
```bash
# Run integration tests with pytest
pytest tests/integration/ --cov=src

# Run end-to-end tests with pytest
pytest tests/e2e/ --cov=src
```

#### Running All Tests
```bash
# Run all tests
pytest

# Generate HTML report for detailed coverage visualization
pytest --cov=src --cov-report=html
```

#### Running Sample Nose2 Test
```bash
# Run the nose2 calculator test
nose2 -v src.calculator.test.test_calculator_nose2 --with-coverage --coverage=src.calculator
```

> **Note**: The above commands work in a bash environment. You might need to adjust commands for your specific terminal.



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