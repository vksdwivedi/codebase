"""Gold-layer aggregate builders."""

from __future__ import annotations

from collections import Counter

from realtime_lakehouse.models import Record


class EventTypeAggregator:
    """Builds serving-friendly counts by event type."""

    def build(self, records: list[Record]) -> list[Record]:
        counts = Counter(str(record["event_type"]) for record in records)
        return [
            {"event_type": event_type, "event_count": count}
            for event_type, count in sorted(counts.items())
        ]
