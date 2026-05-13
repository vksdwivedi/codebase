from __future__ import annotations

import json
from pathlib import Path

from realtime_lakehouse.config import PipelineConfig
from realtime_lakehouse.pipeline import LakehousePipeline


def test_pipeline_promotes_records_through_medallion_layers(tmp_path: Path) -> None:
    source = tmp_path / "events.jsonl"
    source.write_text(
        "\n".join(
            [
                json.dumps({"event_id": "1", "event_type": "Order_Created", "event_time": "now", "customer_id": 10, "amount": "4.5"}),
                json.dumps({"event_id": "2", "event_type": "Order_Created", "event_time": "now", "customer_id": 11, "amount": 5}),
                json.dumps({"event_id": "bad", "event_type": "Order_Created"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    config = PipelineConfig(
        source_path=source,
        lakehouse_root=tmp_path / "lakehouse",
        checkpoint_path=tmp_path / "checkpoints" / "offset",
        required_fields=("event_id", "event_type", "event_time", "customer_id", "amount"),
        batch_size=10,
    )

    metrics = LakehousePipeline(config).run_once()

    assert metrics.consumed == 3
    assert metrics.bronze_written == 3
    assert metrics.silver_written == 2
    assert metrics.rejected == 1
    assert metrics.gold_written == 1
    assert metrics.aggregate_counts == {"order_created": 2}
    assert config.checkpoint_path.read_text(encoding="utf-8") == "3"

    clean_rows = (config.lakehouse_root / "silver" / "events_clean.jsonl").read_text(encoding="utf-8").splitlines()
    assert json.loads(clean_rows[0])["customer_id"] == "10"
    assert json.loads(clean_rows[0])["amount"] == 4.5
