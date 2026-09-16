## What changed?

Describe the behavior or safety issue this PR changes and the approach you took.

## Why this approach?

Explain any planning, collision handling, filesystem mutation, manifest, rollback, CLI, or compatibility trade-offs introduced by the change.

## Validation

- [ ] `python -m ruff check src tests`
- [ ] `python -m compileall -q src tests`
- [ ] `python -m pytest`
- [ ] Tested with temporary/sample files rather than important personal data
- [ ] No personal files, secrets, generated manifests, or local environment files were committed

## Risk / rollback

Describe any chance of destructive file behavior, overwrite risk, path handling changes, or rollback impact.

## Documentation

- [ ] README/docs updated when behavior changed
- [ ] No documentation change needed
