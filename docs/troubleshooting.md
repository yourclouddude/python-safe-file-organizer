# Troubleshooting

## `file-organizer: command not found`

Install the project in editable mode from the repository root:

```bash
pip install -e .
```

Then reopen the shell if your environment does not refresh console scripts automatically.

You can also run:

```bash
python -m file_organizer.cli plan .
```

## Nothing is being organized

The tool scans only files directly inside the target directory.

It intentionally ignores:

- subdirectories
- hidden files beginning with `.`

Recursive behavior is not enabled in this version.

## A file was renamed with `(1)`

That means a file with the same name already existed in the destination category.

The organizer preserves both files rather than overwriting one.

## `apply` prints the plan but moves nothing

That is the safety behavior. Add explicit confirmation:

```bash
file-organizer apply PATH --yes
```

Always run `plan` first.

## Rollback says the original path already exists

The organizer refuses to overwrite a file created after the original move.

Inspect both files manually and decide which one should remain before retrying rollback.

## The manifest is missing

The default manifest is created inside the organized directory as:

```text
.file-organizer-manifest.json
```

Because it begins with `.`, the organizer itself ignores it during later scans.

## Permission denied

The current user must have permission to read, create directories, and move files in the target path.

Do not solve permission problems by running unknown automation with unnecessarily elevated privileges. Use a test directory you own while learning.

## Windows path issues

Use quoted paths when directories contain spaces:

```powershell
file-organizer plan "C:\Users\you\My Files"
```

The project uses `pathlib` so path handling remains platform-aware.
