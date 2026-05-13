"""Configuration objects for the realtime lakehouse pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    """Runtime settings for a local lakehouse pipeline."""

    source_path: Path
    lakehouse_root: Path
    checkpoint_path: Path
    required_fields: tuple[str, ...]
    batch_size: int = 100

    @classmethod
    def from_json(cls, path: str | Path) -> "PipelineConfig":
        """Load a pipeline configuration from a JSON file."""
        config_path = Path(path)
        data = json.loads(config_path.read_text(encoding="utf-8"))
        base_dir = config_path.parent.parent
        return cls(
            source_path=_resolve(base_dir, data["source_path"]),
            lakehouse_root=_resolve(base_dir, data["lakehouse_root"]),
            checkpoint_path=_resolve(base_dir, data["checkpoint_path"]),
            required_fields=tuple(data.get("required_fields", ())),
            batch_size=int(data.get("batch_size", 100)),
        )


def _resolve(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else base_dir / path
