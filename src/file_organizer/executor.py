from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from file_organizer.planner import MoveOperation

MANIFEST_VERSION = 1


def write_manifest(
    operations: Iterable[MoveOperation],
    manifest_path: Path,
) -> Path:
    manifest_path = manifest_path.expanduser().resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "version": MANIFEST_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operations": [operation.as_dict() for operation in operations],
    }
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return manifest_path


def apply_plan(
    operations: list[MoveOperation],
    manifest_path: Path,
) -> Path:
    completed: list[MoveOperation] = []

    try:
        for operation in operations:
            operation.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(operation.source), str(operation.destination))
            completed.append(operation)
    except Exception:
        for operation in reversed(completed):
            if operation.destination.exists() and not operation.source.exists():
                operation.source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(operation.destination), str(operation.source))
        raise

    return write_manifest(completed, manifest_path)


def rollback(manifest_path: Path) -> int:
    manifest_path = manifest_path.expanduser().resolve()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    if payload.get("version") != MANIFEST_VERSION:
        raise ValueError("Unsupported manifest version")

    operations = payload.get("operations")
    if not isinstance(operations, list):
        raise ValueError("Manifest operations must be a list")

    restored = 0

    for item in reversed(operations):
        if not isinstance(item, dict):
            raise ValueError("Invalid manifest operation")

        source = Path(str(item["source"]))
        destination = Path(str(item["destination"]))

        if not destination.exists():
            continue
        if source.exists():
            raise FileExistsError(
                f"Cannot restore {source.name}: original path already exists"
            )

        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(destination), str(source))
        restored += 1

    return restored
