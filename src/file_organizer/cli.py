from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from file_organizer.executor import apply_plan, rollback
from file_organizer.planner import MoveOperation, build_plan


def _print_plan(operations: list[MoveOperation]) -> None:
    if not operations:
        print("Nothing to organize.")
        return

    for operation in operations:
        print(
            f"{operation.source.name} -> "
            f"{operation.destination.parent.name}/{operation.destination.name}"
        )


def _default_manifest(directory: Path) -> Path:
    return directory.expanduser().resolve() / ".file-organizer-manifest.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Safely organize files by extension with preview and rollback.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Preview changes without moving files")
    plan_parser.add_argument("directory", type=Path)

    apply_parser = subparsers.add_parser("apply", help="Apply the proposed file moves")
    apply_parser.add_argument("directory", type=Path)
    apply_parser.add_argument(
        "--yes",
        action="store_true",
        help="Required safety switch that confirms file moves",
    )
    apply_parser.add_argument("--manifest", type=Path)

    undo_parser = subparsers.add_parser("undo", help="Restore files from a manifest")
    undo_parser.add_argument("manifest", type=Path)
    undo_parser.add_argument(
        "--yes",
        action="store_true",
        help="Required safety switch that confirms rollback",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "plan":
        operations = build_plan(args.directory)
        _print_plan(operations)
        return 0

    if args.command == "apply":
        operations = build_plan(args.directory)
        _print_plan(operations)

        if not args.yes:
            print("\nNo files moved. Re-run with --yes after reviewing the plan.")
            return 2

        manifest = args.manifest or _default_manifest(args.directory)
        written = apply_plan(operations, manifest)
        print(f"\nMoved {len(operations)} file(s). Manifest: {written}")
        return 0

    if args.command == "undo":
        if not args.yes:
            print("No files restored. Re-run with --yes to confirm rollback.")
            return 2

        restored = rollback(args.manifest)
        print(f"Restored {restored} file(s).")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
