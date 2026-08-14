from __future__ import annotations

import json
from pathlib import Path

import pytest

from file_organizer.cli import main
from file_organizer.executor import apply_plan, rollback
from file_organizer.planner import build_plan


def test_build_plan_classifies_files(tmp_path: Path) -> None:
    (tmp_path / "resume.pdf").write_text("pdf", encoding="utf-8")
    (tmp_path / "photo.png").write_text("png", encoding="utf-8")
    (tmp_path / "notes.xyz").write_text("other", encoding="utf-8")

    plan = build_plan(tmp_path)

    destinations = {operation.destination.relative_to(tmp_path) for operation in plan}
    assert Path("Documents/resume.pdf") in destinations
    assert Path("Images/photo.png") in destinations
    assert Path("Other/notes.xyz") in destinations


def test_build_plan_ignores_directories_and_hidden_files(tmp_path: Path) -> None:
    (tmp_path / "subdir").mkdir()
    (tmp_path / ".secret.txt").write_text("hidden", encoding="utf-8")
    (tmp_path / "visible.txt").write_text("visible", encoding="utf-8")

    plan = build_plan(tmp_path)

    assert [operation.source.name for operation in plan] == ["visible.txt"]


def test_collision_gets_numbered_destination(tmp_path: Path) -> None:
    (tmp_path / "report.pdf").write_text("new", encoding="utf-8")
    documents = tmp_path / "Documents"
    documents.mkdir()
    (documents / "report.pdf").write_text("existing", encoding="utf-8")

    plan = build_plan(tmp_path)

    assert plan[0].destination.name == "report (1).pdf"


def test_apply_writes_manifest_and_moves_files(tmp_path: Path) -> None:
    source = tmp_path / "data.csv"
    source.write_text("a,b", encoding="utf-8")
    manifest = tmp_path / ".manifest.json"

    plan = build_plan(tmp_path)
    written = apply_plan(plan, manifest)

    assert written == manifest.resolve()
    assert not source.exists()
    assert (tmp_path / "Data" / "data.csv").exists()

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert len(payload["operations"]) == 1


def test_rollback_restores_files(tmp_path: Path) -> None:
    source = tmp_path / "image.jpg"
    source.write_text("image", encoding="utf-8")
    manifest = tmp_path / ".manifest.json"

    plan = build_plan(tmp_path)
    apply_plan(plan, manifest)

    restored = rollback(manifest)

    assert restored == 1
    assert source.exists()
    assert not (tmp_path / "Images" / "image.jpg").exists()


def test_rollback_refuses_to_overwrite_existing_source(tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("original", encoding="utf-8")
    manifest = tmp_path / ".manifest.json"

    plan = build_plan(tmp_path)
    apply_plan(plan, manifest)
    source.write_text("new file", encoding="utf-8")

    with pytest.raises(FileExistsError):
        rollback(manifest)


def test_missing_directory_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        build_plan(tmp_path / "missing")


def test_cli_apply_requires_explicit_confirmation(tmp_path: Path) -> None:
    source = tmp_path / "draft.txt"
    source.write_text("draft", encoding="utf-8")

    exit_code = main(["apply", str(tmp_path)])

    assert exit_code == 2
    assert source.exists()


def test_cli_plan_does_not_modify_files(tmp_path: Path) -> None:
    source = tmp_path / "photo.png"
    source.write_text("image", encoding="utf-8")

    exit_code = main(["plan", str(tmp_path)])

    assert exit_code == 0
    assert source.exists()
    assert not (tmp_path / "Images").exists()
