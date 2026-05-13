"""Gold-layer aggregate builders."""

from __future__ import annotations

from collections import defaultdict

from realtime_lakehouse.config import PipelineConfig
from realtime_lakehouse.models import Record


class GoldAggregateBuilder:
    """Builds serving-friendly aggregates from silver records."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config

    def by_event_type(self, records: list[Record]) -> list[Record]:
        summary: dict[str, dict[str, float | int | str]] = defaultdict(
            lambda: {"event_count": 0, "total_amount": 0.0}
        )
        for record in records:
            event_type = str(record[self.config.event_type_field])
            row = summary[event_type]
            row[self.config.event_type_field] = event_type
            row["event_count"] = int(row["event_count"]) + 1
            row["total_amount"] = round(float(row["total_amount"]) + float(record[self.config.amount_field]), 2)

        return [_finalize_amount(row) for _, row in sorted(summary.items())]

    def by_customer(self, records: list[Record]) -> list[Record]:
        summary: dict[str, dict[str, float | int | str]] = defaultdict(
            lambda: {"event_count": 0, "total_amount": 0.0}
        )
        event_types_by_customer: dict[str, set[str]] = defaultdict(set)

        for record in records:
            customer_id = str(record[self.config.customer_id_field])
            event_type = str(record[self.config.event_type_field])
            row = summary[customer_id]
            row[self.config.customer_id_field] = customer_id
            row["event_count"] = int(row["event_count"]) + 1
            row["total_amount"] = round(float(row["total_amount"]) + float(record[self.config.amount_field]), 2)
            event_types_by_customer[customer_id].add(event_type)

        rows: list[Record] = []
        for customer_id, row in sorted(summary.items()):
            finalized = _finalize_amount(row)
            finalized["event_types"] = sorted(event_types_by_customer[customer_id])
            rows.append(finalized)
        return rows


def _finalize_amount(row: dict[str, float | int | str]) -> Record:
    finalized = dict(row)
    finalized["total_amount"] = round(float(finalized["total_amount"]), 2)
    return finalized
