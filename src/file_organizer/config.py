from __future__ import annotations

CATEGORY_EXTENSIONS: dict[str, set[str]] = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic"},
    "Data": {".csv", ".json", ".xlsx", ".xls", ".parquet", ".xml"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Code": {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".go",
        ".rs",
        ".html",
        ".css",
        ".sql",
    },
    "Audio": {".mp3", ".wav", ".m4a", ".flac", ".aac"},
    "Video": {".mp4", ".mov", ".mkv", ".avi", ".webm"},
}

DEFAULT_CATEGORY = "Other"


def category_for_suffix(suffix: str) -> str:
    normalized = suffix.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if normalized in extensions:
            return category
    return DEFAULT_CATEGORY
