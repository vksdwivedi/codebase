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


@dataclass
class PipelineMetrics:
    """Counters emitted after a pipeline run."""

    consumed: int = 0
    bronze_written: int = 0
    silver_written: int = 0
    rejected: int = 0
    gold_written: int = 0
    aggregate_counts: dict[str, int] = field(default_factory=dict)
