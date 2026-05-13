"""Data quality rules used when promoting bronze records into silver."""

from __future__ import annotations

from datetime import UTC, datetime

from realtime_lakehouse.config import PipelineConfig
from realtime_lakehouse.models import Record, RejectedRecord, ValidatedBatch


class QualityRuleSet:
    """Applies required-field validation, type coercion, and normalization."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.required_fields = config.required_fields

    def validate(self, records: list[Record]) -> ValidatedBatch:
        accepted: list[Record] = []
        rejected: list[RejectedRecord] = []

        for record in records:
            missing = [field for field in self.required_fields if _is_blank(record.get(field))]
            if missing:
                rejected.append(RejectedRecord(record=record, reason=f"missing required fields: {', '.join(missing)}"))
                continue

            try:
                accepted.append(self._normalize(record))
            except (TypeError, ValueError) as exc:
                rejected.append(RejectedRecord(record=record, reason=f"normalization failed: {exc}"))

        return ValidatedBatch(accepted=accepted, rejected=rejected)

    def _normalize(self, record: Record) -> Record:
        normalized = dict(record)
        normalized[self.config.event_type_field] = str(normalized[self.config.event_type_field]).strip().lower()
        normalized[self.config.customer_id_field] = str(normalized[self.config.customer_id_field]).strip()
        normalized[self.config.amount_field] = round(float(normalized[self.config.amount_field]), 2)
        normalized["_processed_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        normalized["_pipeline"] = self.config.pipeline_name
        return normalized


def _is_blank(value: object) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())
