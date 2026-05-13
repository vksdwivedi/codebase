# Realtime Lakehouse Framework

A redesigned, batteries-included Python starter for building a local real-time lakehouse pipeline before connecting production streaming and table services. The framework now has explicit pipeline metadata, configurable table names, stronger silver-layer validation, and two gold serving marts.

## What the framework does

- **Ingests micro-batches** from JSON Lines with checkpointed offsets.
- **Preserves bronze data** as append-only raw events for replay and audit.
- **Promotes silver records** with required-field checks, type coercion, normalized event/customer fields, processing metadata, and queryable rejections.
- **Builds gold marts** for event-type metrics and customer-level value summaries.
- **Emits operational metrics** with offsets, output table paths, write counts, and aggregate counts.

## Redesigned architecture

```text
                ┌──────────────────┐
                │ JSONL event feed │
                └────────┬─────────┘
                         │ offset-aware micro-batch
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ LakehousePipeline                                           │
│  ├─ Bronze: raw append-only events                          │
│  ├─ Silver: validation, normalization, rejected records      │
│  └─ Gold: event-type summary + customer summary snapshots    │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
        lakehouse/{bronze,silver,gold}/*.jsonl + checkpoints
```

## Quick start

```bash
cd realtime_lakehouse_framework
PYTHONPATH=src python -m realtime_lakehouse.cli --config configs/local_pipeline.json
```

The command reads sample events from `examples/events.jsonl`, writes medallion outputs into `./lakehouse`, and stores offsets in `./checkpoints`.

Example metric output:

```json
{
  "aggregate_counts": {
    "order_created": 2,
    "order_cancelled": 1
  },
  "bronze_written": 3,
  "consumed": 3,
  "end_offset": 3,
  "gold_written": 4,
  "pipeline_name": "orders_realtime_lakehouse",
  "rejected": 0,
  "silver_written": 3,
  "start_offset": 0
}
```

## Configuration

`configs/local_pipeline.json` controls source paths, checkpoints, required fields, and logical table names:

```json
{
  "pipeline_name": "orders_realtime_lakehouse",
  "source_path": "examples/events.jsonl",
  "lakehouse_root": "lakehouse",
  "checkpoint_path": "checkpoints/local_pipeline.offset",
  "batch_size": 3,
  "required_fields": ["event_id", "event_type", "event_time", "customer_id", "amount"],
  "tables": {
    "bronze_events": "orders_raw",
    "silver_events": "orders_clean",
    "silver_rejections": "orders_rejected",
    "gold_event_summary": "orders_by_event_type",
    "gold_customer_summary": "orders_by_customer"
  }
}
```

## Output tables

| Layer | Default table | Write mode | Purpose |
| --- | --- | --- | --- |
| Bronze | `events_raw` | Append | Raw source events for replay and audit |
| Silver | `events_clean` | Append | Normalized, typed records with pipeline metadata |
| Silver | `events_rejected` | Append | Failed records with rejection reasons |
| Gold | `event_type_summary` | Replace snapshot | Event counts and amount totals by event type |
| Gold | `customer_summary` | Replace snapshot | Customer counts, total amount, and observed event types |

## Project layout

```text
configs/                  Local pipeline configuration
examples/                 Example streaming input data
docs/                     Design notes and production guidance
src/realtime_lakehouse/   Framework package
tests/                    Unit tests for the pipeline components
```

## Extending for production

1. Replace `JsonLinesSource` with adapters for Kafka, Kinesis, Pub/Sub, CDC logs, or managed streaming services.
2. Replace `JsonLinesSink` with Delta Lake, Apache Iceberg, Apache Hudi, or cloud object storage writers.
3. Add schema registry checks in `QualityRuleSet` for contract enforcement and backwards-compatible evolution.
4. Publish `PipelineMetrics` to observability systems such as Prometheus, OpenTelemetry, Datadog, or CloudWatch.
5. Run the CLI from an orchestrator or container platform with durable checkpoint storage.
