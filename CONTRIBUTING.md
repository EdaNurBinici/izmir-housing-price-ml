# Contributing to Izmir Housing Price ML

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

## Code Quality Standards

This project maintains high code quality standards:

### Formatting
- **Black** for code formatting (line length: 100)
- **isort** for import sorting

Run formatters:
```bash
make format
# or
black .
isort .
```

### Linting
- **Ruff** for fast, comprehensive linting

Run linter:
```bash
make lint
# or
ruff check .
```

### Testing
- **pytest** for unit tests
- Aim for >80% code coverage

Run tests:
```bash
make test
# or
pytest tests/ -v
```

## Pre-commit Hooks

Pre-commit hooks automatically run before each commit:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML validation
- Black formatting
- isort import sorting
- Ruff linting

Install hooks:
```bash
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

## Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following code standards

3. Run quality checks:
   ```bash
   make format
   make lint
   make test
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Test results

## Commit Message Convention

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Build process or auxiliary tool changes

Example:
```
feat: add district-based price prediction
fix: correct luxury score calculation
docs: update installation instructions
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Questions?

Feel free to open an issue for any questions or concerns.
