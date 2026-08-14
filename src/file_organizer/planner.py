from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from file_organizer.config import category_for_suffix


@dataclass(frozen=True, slots=True)
class MoveOperation:
    source: Path
    destination: Path

    def as_dict(self) -> dict[str, str]:
        return {
            "source": str(self.source),
            "destination": str(self.destination),
        }


def _unique_destination(destination: Path, reserved: set[Path]) -> Path:
    if destination not in reserved and not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = destination.with_name(f"{stem} ({counter}){suffix}")
        if candidate not in reserved and not candidate.exists():
            return candidate
        counter += 1


def build_plan(directory: Path) -> list[MoveOperation]:
    root = directory.expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    operations: list[MoveOperation] = []
    reserved: set[Path] = set()

    for source in sorted(root.iterdir(), key=lambda path: path.name.lower()):
        if not source.is_file() or source.name.startswith("."):
            continue

        category = category_for_suffix(source.suffix)
        destination = root / category / source.name
        destination = _unique_destination(destination, reserved)
        reserved.add(destination)
        operations.append(MoveOperation(source=source, destination=destination))

    return operations
