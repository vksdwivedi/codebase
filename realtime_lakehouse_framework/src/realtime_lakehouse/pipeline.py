"""Pipeline orchestration for local realtime lakehouse processing."""

from __future__ import annotations

from dataclasses import asdict

from realtime_lakehouse.checkpoint import FileCheckpointStore
from realtime_lakehouse.config import PipelineConfig
from realtime_lakehouse.gold import GoldAggregateBuilder
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
        self.quality_rules = QualityRuleSet(config)
        self.aggregates = GoldAggregateBuilder(config)

    def run_once(self) -> PipelineMetrics:
        """Process a single micro-batch and commit the source offset."""
        start_offset = self.checkpoints.load()
        records, end_offset = self.source.read_batch(offset=start_offset, limit=self.config.batch_size)
        metrics = PipelineMetrics(
            pipeline_name=self.config.pipeline_name,
            consumed=len(records),
            start_offset=start_offset,
            end_offset=end_offset,
            output_tables=self._output_tables(),
        )
        if not records:
            return metrics

        tables = self.config.tables
        metrics.bronze_written = self.sink.append("bronze", tables.bronze_events, records)

        validated = self.quality_rules.validate(records)
        metrics.silver_written = self.sink.append("silver", tables.silver_events, validated.accepted)
        metrics.rejected = self.sink.append(
            "silver",
            tables.silver_rejections,
            [asdict(item) for item in validated.rejected],
        )

        event_type_summary = self.aggregates.by_event_type(validated.accepted)
        customer_summary = self.aggregates.by_customer(validated.accepted)
        metrics.gold_written = self.sink.replace("gold", tables.gold_event_summary, event_type_summary)
        metrics.gold_written += self.sink.replace("gold", tables.gold_customer_summary, customer_summary)
        metrics.aggregate_counts = {
            str(record[self.config.event_type_field]): int(record["event_count"])
            for record in event_type_summary
        }

        self.checkpoints.commit(end_offset)
        return metrics

    def _output_tables(self) -> dict[str, str]:
        tables = self.config.tables
        layer_tables = {
            "bronze_events": ("bronze", tables.bronze_events),
            "silver_events": ("silver", tables.silver_events),
            "silver_rejections": ("silver", tables.silver_rejections),
            "gold_event_summary": ("gold", tables.gold_event_summary),
            "gold_customer_summary": ("gold", tables.gold_customer_summary),
        }
        return {name: str(self.sink.path_for(layer, table)) for name, (layer, table) in layer_tables.items()}
