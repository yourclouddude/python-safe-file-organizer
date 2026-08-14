# Contributing

Thanks for improving this YourCloudDude learner project.

## Local setup

```bash
python -m venv .venv
pip install -r requirements-dev.txt
pip install -e .
```

## Before opening a pull request

Run:

```bash
python -m ruff check src tests
python -m compileall -q src tests
python -m pytest
```

## Contribution principles

- keep file operations safe by default
- never add silent overwrite behavior
- add tests for destructive or rollback-related changes
- keep the planner independent from execution where practical
- document new CLI behavior
- avoid adding dependencies when the standard library is sufficient

## Good first contributions

- more classification rules
- clearer error messages
- additional tests
- Windows/macOS documentation
- configurable categories
- structured logging

For larger features such as recursion, duplicate deletion, or scheduling, explain the safety model and failure behavior in the pull request.
