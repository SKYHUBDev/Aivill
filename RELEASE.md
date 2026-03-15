# AiVill Release Guide

This guide explains how to publish AiVill to PyPI.

## Prerequisites

1. Python 3.8+
2. pip installed
3. PyPI account (testpypi and production)

## Step 1: Build the Package

```bash
# Install build if needed
pip install build

# Build the package
python -m build
```

This creates:
- `dist/aivill-0.1.0.tar.gz` (source distribution)
- `dist/aivill-0.1.0-py3-none-any.whl` (wheel)

## Step 2: Upload to Test PyPI (Optional but Recommended)

```bash
# Install twine if needed
pip install twine

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ aivill
```

## Step 3: Upload to Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

## Step 4: Verify Installation

```bash
# Install from PyPI
pip install aivill

# Verify import
python -c "from aivill import VillainEngine; print('Success!')"
```

## Version Bumping

To release a new version:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Update version in `aivill/__init__.py`:
   ```python
   __version__ = "0.2.0"
   ```

3. Rebuild:
   ```bash
   python -m build
   ```

4. Upload:
   ```bash
   twine upload dist/*
   ```

## Troubleshooting

### "File already exists" error
- Increment the version number

### Authentication error
- Make sure you're logged in to PyPI
- Use `twine login` to store credentials

### Package not found
- Wait a few minutes for PyPI to index
- Check the package name is correct on PyPI

## Quick Reference

```bash
# Full release workflow
python -m build
twine upload dist/*
```

## Links

- PyPI: https://pypi.org/project/aivill/
- GitHub: https://github.com/aivill/aivill
- Documentation: https://aivill.readthedocs.io
