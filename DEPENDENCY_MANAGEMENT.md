# Dependency Management Guide

This project uses a two-tier dependency management system for reproducibility and flexibility.

## File Structure

- **`requirements.in`** - High-level dependencies with minimum versions (>=)
- **`requirements.txt`** - Pinned exact versions (==) for reproducible builds
- **`requirements-dev.txt`** - Development tools with pinned versions

## Philosophy

### Production Dependencies
- `requirements.in` specifies what we need (flexible)
- `requirements.txt` specifies exact versions (reproducible)
- This ensures consistent builds across environments

### Development Dependencies
- `requirements-dev.txt` includes production deps + dev tools
- All versions are pinned for consistency

## Updating Dependencies

### Option 1: Manual Update (Current Method)

1. Update `requirements.in` with new minimum versions
2. Install and test locally:
   ```bash
   pip install -r requirements.in
   ```
3. Freeze current versions to `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```
4. Clean up `requirements.txt` to only include direct dependencies

### Option 2: Using pip-tools (Recommended for Future)

Install pip-tools:
```bash
pip install pip-tools
```

Compile pinned versions:
```bash
pip-compile requirements.in
```

Upgrade all dependencies:
```bash
pip-compile --upgrade requirements.in
```

Upgrade specific package:
```bash
pip-compile --upgrade-package pandas requirements.in
```

## Current Versions (Last Updated: 2026-02-17)

### Production
- streamlit==1.52.2
- pandas==2.2.3
- numpy==2.1.3
- scikit-learn==1.6.0
- matplotlib==3.9.3
- seaborn==0.13.2
- joblib==1.4.2
- pyyaml==6.0.3
- pytest==7.4.3

### Development
- black==26.1.0
- isort==7.0.0
- ruff==0.15.1
- pre-commit==4.0.1
- mypy==1.13.0

## Testing After Updates

Always test after updating dependencies:

```bash
# Install updated dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run linters
ruff check .
black --check .
isort --check-only .

# Train model to ensure compatibility
python model_egitim.py

# Test application
streamlit run app.py
```

## CI/CD Integration

Our GitHub Actions workflow automatically:
1. Caches dependencies for faster builds
2. Tests against multiple Python versions (3.8-3.11)
3. Runs linting and formatting checks
4. Ensures reproducible builds with pinned versions

## Best Practices

1. **Always pin versions in production** - Use `==` in `requirements.txt`
2. **Use minimum versions in .in files** - Use `>=` in `requirements.in`
3. **Test before committing** - Run full test suite after updates
4. **Document breaking changes** - Note any API changes in commit messages
5. **Update regularly** - Check for security updates monthly

## Troubleshooting

### Dependency Conflicts

If you encounter conflicts:
```bash
pip install --upgrade pip
pip install -r requirements.in --upgrade
pip freeze > requirements.txt
```

### Version Incompatibilities

Check compatibility:
```bash
pip check
```

### Clean Install

Start fresh:
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## Security

Check for known vulnerabilities:
```bash
pip install safety
safety check -r requirements.txt
```

Or use GitHub's Dependabot (already configured in this repo).
