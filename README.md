# Team-9-Technology-Template-Repository
# Python Project Template with UV

## Description
A modern Python project template featuring comprehensive test coverage, continuous integration with CircleCI, and dependency management using UV. This template includes configurations for static type checking, code formatting, and automated testing.

## Prerequisites
* Any package installer like curl
* Git
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
source .venv/bin/activate
```
Note on windows:
use
```bash
uv venv .venv
.venv\bin\activate
```

4. Install dependencies:
```bash
uv pip install ".[dev]"
```

## Development Tools

### Static Analysis
Run type checking and code linting:
```bash
mypy src tests
ruff check .
```

### Testing
The project includes unit, integration, and end-to-end tests:

```bash
# Run unit tests with coverage
pytest src/calculator/test src/logger/test src/notifier/test --cov=src --cov-report=html

# Run integration tests
pytest tests/integration

# Run end-to-end tests
pytest tests/e2e

# Run all tests
pytest
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

2. Make your changes and ensure all tests pass:
```bash
pytest
```

3. Push your changes and create a pull request:
```bash
git push origin feature-name
```

## License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Additional Resources
- [UV Documentation](https://github.com/astral-sh/uv)
- [CircleCI Documentation](https://circleci.com/docs/)
- [pytest Documentation](https://docs.pytest.org/)