"""Streaming source and lakehouse sink implementations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from realtime_lakehouse.models import Record


class JsonLinesSource:
    """Reads JSON Lines records from an offset for local micro-batch testing."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def read_batch(self, offset: int, limit: int) -> tuple[list[Record], int]:
        records: list[Record] = []
        next_offset = offset
        with self.path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream):
                if line_number < offset:
                    continue
                if len(records) >= limit:
                    break
                records.append(json.loads(line))
                next_offset = line_number + 1
        return records, next_offset


class JsonLinesSink:
    """Writes records to medallion-layer JSON Lines files."""

    def __init__(self, lakehouse_root: Path) -> None:
        self.lakehouse_root = lakehouse_root

    def append(self, layer: str, table: str, records: Iterable[Record]) -> int:
        """Append records to a table and return the number written."""
        return self._write(layer=layer, table=table, records=records, mode="a")

    def replace(self, layer: str, table: str, records: Iterable[Record]) -> int:
        """Replace a table snapshot and return the number written."""
        return self._write(layer=layer, table=table, records=records, mode="w")

    def path_for(self, layer: str, table: str) -> Path:
        """Return the file path for a logical layer/table pair."""
        return self.lakehouse_root / layer / f"{table}.jsonl"

    def _write(self, layer: str, table: str, records: Iterable[Record], mode: str) -> int:
        materialized = list(records)
        target_file = self.path_for(layer, table)
        if not materialized and mode == "a":
            return 0

        target_file.parent.mkdir(parents=True, exist_ok=True)
        with target_file.open(mode, encoding="utf-8") as stream:
            for record in materialized:
                stream.write(json.dumps(record, sort_keys=True) + "\n")
        return len(materialized)
