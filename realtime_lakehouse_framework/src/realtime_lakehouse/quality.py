"""Data quality rules used when promoting bronze records into silver."""

from __future__ import annotations

from realtime_lakehouse.models import Record, RejectedRecord


class QualityRuleSet:
    """Applies required-field validation and simple normalization."""

    def __init__(self, required_fields: tuple[str, ...]) -> None:
        self.required_fields = required_fields

    def validate(self, records: list[Record]) -> tuple[list[Record], list[RejectedRecord]]:
        accepted: list[Record] = []
        rejected: list[RejectedRecord] = []

        for record in records:
            missing = [field for field in self.required_fields if field not in record]
            if missing:
                rejected.append(RejectedRecord(record=record, reason=f"missing fields: {', '.join(missing)}"))
                continue

            normalized = dict(record)
            normalized["event_type"] = str(normalized["event_type"]).lower()
            normalized["customer_id"] = str(normalized["customer_id"])
            normalized["amount"] = float(normalized["amount"])
            accepted.append(normalized)

        return accepted, rejected
