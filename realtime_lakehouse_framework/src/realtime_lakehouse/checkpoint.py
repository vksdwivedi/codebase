"""File-based offset checkpoint management."""

from __future__ import annotations

from pathlib import Path


class FileCheckpointStore:
    """Persists a single monotonically increasing source offset."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> int:
        """Return the last committed offset, or zero for a new stream."""
        if not self.path.exists():
            return 0
        value = self.path.read_text(encoding="utf-8").strip()
        return int(value or "0")

    def commit(self, offset: int) -> None:
        """Persist an offset atomically enough for local development."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(str(offset), encoding="utf-8")
