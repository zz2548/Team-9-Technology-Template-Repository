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
source .venv/bin/activate
```
Note : If on on windows do
```bash
uv venv .venv
.venv\Scripts\activate
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
ruff check . --config pyproject.toml
```

### Testing
The project includes unit, integration, and end-to-end tests:

```bash
# Running a single unit test
nose2 -v -s src/calculator/test/
nose2 -v -s src/logger/test/
nose2 -v -s src/notifier/test/

# Running all unit tests with coverage
```bash
nose2 -v -s src/calculator/test/ --with-coverage --coverage=src.calculator

COVERAGE_FILE=.coverage.logger nose2 -v -s src/logger/test/ --with-coverage --coverage=src.logger

COVERAGE_FILE=.coverage.notifier nose2 -v -s src/notifier/test/ --with-coverage --coverage=src.notifier

coverage combine .coverage .coverage.logger .coverage.notifier

coverage report --fail-under=70
coverage xml -o unit-coverage.xml 
coverage html -d unit-htmlcov
```
Note : The above command works in bash environment, you might need to change the command slightly depending on your terminal.


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

2. Make your changes and ensure all tests pass:
```bash
nose2
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
- [nose2 Documentation](https://docs.nose2.io/en/latest/)