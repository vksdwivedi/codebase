from __future__ import annotations

import json
from pathlib import Path

from realtime_lakehouse.config import PipelineConfig, TableNames
from realtime_lakehouse.pipeline import LakehousePipeline


def test_pipeline_promotes_records_through_medallion_layers(tmp_path: Path) -> None:
    source = tmp_path / "events.jsonl"
    source.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "event_id": "1",
                        "event_type": "Order_Created",
                        "event_time": "now",
                        "customer_id": 10,
                        "amount": "4.5",
                    }
                ),
                json.dumps(
                    {
                        "event_id": "2",
                        "event_type": "Order_Created",
                        "event_time": "now",
                        "customer_id": 11,
                        "amount": 5,
                    }
                ),
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
        pipeline_name="orders_test",
    )

    metrics = LakehousePipeline(config).run_once()

    assert metrics.pipeline_name == "orders_test"
    assert metrics.consumed == 3
    assert metrics.bronze_written == 3
    assert metrics.silver_written == 2
    assert metrics.rejected == 1
    assert metrics.gold_written == 3
    assert metrics.start_offset == 0
    assert metrics.end_offset == 3
    assert metrics.aggregate_counts == {"order_created": 2}
    assert config.checkpoint_path.read_text(encoding="utf-8") == "3"

    clean_rows = (config.lakehouse_root / "silver" / "events_clean.jsonl").read_text(encoding="utf-8").splitlines()
    first_clean_row = json.loads(clean_rows[0])
    assert first_clean_row["customer_id"] == "10"
    assert first_clean_row["amount"] == 4.5
    assert first_clean_row["_pipeline"] == "orders_test"
    assert "_processed_at" in first_clean_row

    event_summary_rows = (config.lakehouse_root / "gold" / "event_type_summary.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert json.loads(event_summary_rows[0]) == {
        "event_count": 2,
        "event_type": "order_created",
        "total_amount": 9.5,
    }

    customer_summary_rows = (config.lakehouse_root / "gold" / "customer_summary.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert json.loads(customer_summary_rows[0]) == {
        "customer_id": "10",
        "event_count": 1,
        "event_types": ["order_created"],
        "total_amount": 4.5,
    }


def test_config_supports_named_tables(tmp_path: Path) -> None:
    config_path = tmp_path / "configs" / "local.json"
    config_path.parent.mkdir()
    config_path.write_text(
        json.dumps(
            {
                "pipeline_name": "custom_orders",
                "source_path": "examples/events.jsonl",
                "lakehouse_root": "lakehouse",
                "checkpoint_path": "checkpoints/local.offset",
                "batch_size": 25,
                "required_fields": ["event_id"],
                "tables": {
                    "bronze_events": "raw_orders",
                    "gold_customer_summary": "customer_value",
                    "unknown": "ignored",
                },
            }
        ),
        encoding="utf-8",
    )

    config = PipelineConfig.from_json(config_path)

    assert config.pipeline_name == "custom_orders"
    assert config.batch_size == 25
    assert config.required_fields == ("event_id",)
    assert config.tables == TableNames(bronze_events="raw_orders", gold_customer_summary="customer_value")
    assert config.source_path == tmp_path / "examples" / "events.jsonl"
