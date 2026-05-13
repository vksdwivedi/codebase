"""Shared domain models for pipeline execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Record = dict[str, Any]


@dataclass(frozen=True)
class RejectedRecord:
    """A record that failed validation and the reason it was rejected."""

    record: Record
    reason: str


@dataclass(frozen=True)
class ValidatedBatch:
    """Accepted and rejected records after silver quality enforcement."""

    accepted: list[Record]
    rejected: list[RejectedRecord]


@dataclass
class PipelineMetrics:
    """Counters emitted after a pipeline run."""

    pipeline_name: str = "local_realtime_lakehouse"
    consumed: int = 0
    bronze_written: int = 0
    silver_written: int = 0
    rejected: int = 0
    gold_written: int = 0
    start_offset: int = 0
    end_offset: int = 0
    aggregate_counts: dict[str, int] = field(default_factory=dict)
    output_tables: dict[str, str] = field(default_factory=dict)
