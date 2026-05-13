"""Configuration objects for the realtime lakehouse pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TableNames:
    """Logical table names used by the medallion writers."""

    bronze_events: str = "events_raw"
    silver_events: str = "events_clean"
    silver_rejections: str = "events_rejected"
    gold_event_summary: str = "event_type_summary"
    gold_customer_summary: str = "customer_summary"


@dataclass(frozen=True)
class PipelineConfig:
    """Runtime settings for a local lakehouse pipeline."""

    source_path: Path
    lakehouse_root: Path
    checkpoint_path: Path
    required_fields: tuple[str, ...]
    batch_size: int = 100
    pipeline_name: str = "local_realtime_lakehouse"
    event_type_field: str = "event_type"
    event_time_field: str = "event_time"
    customer_id_field: str = "customer_id"
    amount_field: str = "amount"
    tables: TableNames = TableNames()

    @classmethod
    def from_json(cls, path: str | Path) -> "PipelineConfig":
        """Load a pipeline configuration from a JSON file."""
        config_path = Path(path)
        data = json.loads(config_path.read_text(encoding="utf-8"))
        base_dir = config_path.parent.parent
        table_data = data.get("tables", {})
        return cls(
            source_path=_resolve(base_dir, data["source_path"]),
            lakehouse_root=_resolve(base_dir, data["lakehouse_root"]),
            checkpoint_path=_resolve(base_dir, data["checkpoint_path"]),
            required_fields=tuple(data.get("required_fields", ())),
            batch_size=int(data.get("batch_size", 100)),
            pipeline_name=str(data.get("pipeline_name", "local_realtime_lakehouse")),
            event_type_field=str(data.get("event_type_field", "event_type")),
            event_time_field=str(data.get("event_time_field", "event_time")),
            customer_id_field=str(data.get("customer_id_field", "customer_id")),
            amount_field=str(data.get("amount_field", "amount")),
            tables=TableNames(**_known_table_names(table_data)),
        )


def _known_table_names(data: dict[str, Any]) -> dict[str, str]:
    allowed = set(TableNames.__dataclass_fields__)
    return {key: str(value) for key, value in data.items() if key in allowed}


def _resolve(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else base_dir / path
