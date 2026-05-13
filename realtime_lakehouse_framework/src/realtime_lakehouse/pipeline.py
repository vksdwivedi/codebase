"""Pipeline orchestration for local realtime lakehouse processing."""

from __future__ import annotations

from dataclasses import asdict

from realtime_lakehouse.checkpoint import FileCheckpointStore
from realtime_lakehouse.config import PipelineConfig
from realtime_lakehouse.gold import EventTypeAggregator
from realtime_lakehouse.io import JsonLinesSink, JsonLinesSource
from realtime_lakehouse.models import PipelineMetrics
from realtime_lakehouse.quality import QualityRuleSet


class LakehousePipeline:
    """Runs one micro-batch through bronze, silver, and gold layers."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.source = JsonLinesSource(config.source_path)
        self.sink = JsonLinesSink(config.lakehouse_root)
        self.checkpoints = FileCheckpointStore(config.checkpoint_path)
        self.quality_rules = QualityRuleSet(config.required_fields)
        self.aggregator = EventTypeAggregator()

    def run_once(self) -> PipelineMetrics:
        """Process a single micro-batch and commit the source offset."""
        offset = self.checkpoints.load()
        records, next_offset = self.source.read_batch(offset=offset, limit=self.config.batch_size)

        metrics = PipelineMetrics(consumed=len(records))
        if not records:
            return metrics

        metrics.bronze_written = self.sink.append("bronze", "events_raw", records)
        accepted, rejected = self.quality_rules.validate(records)
        metrics.silver_written = self.sink.append("silver", "events_clean", accepted)
        metrics.rejected = self.sink.append(
            "silver",
            "events_rejected",
            [asdict(item) for item in rejected],
        )

        gold_records = self.aggregator.build(accepted)
        metrics.gold_written = self.sink.append("gold", "event_type_counts", gold_records)
        metrics.aggregate_counts = {
            str(record["event_type"]): int(record["event_count"])
            for record in gold_records
        }
        self.checkpoints.commit(next_offset)
        return metrics
