# Lakehouse Design Notes

## Design goals

- Support near real-time ingestion with checkpointed micro-batches.
- Preserve raw data for replay, audit, and backfills.
- Promote records through explicit bronze, silver, and gold contracts.
- Keep quality failures queryable instead of silently dropping them.
- Keep the local implementation dependency-free while leaving clear adapter seams for production systems.

## Runtime flow

1. `JsonLinesSource` reads a bounded batch from the last committed offset.
2. `JsonLinesSink` appends raw records to the bronze table.
3. `QualityRuleSet` checks required fields, normalizes event/customer identifiers, coerces amounts, and stamps processing metadata.
4. Rejected records are written to a dedicated silver rejection table with reasons.
5. `GoldAggregateBuilder` creates replaceable serving snapshots for event types and customers.
6. `FileCheckpointStore` commits the new source offset only after writes complete.

## Layer contracts

| Layer | Contract | Example storage |
| --- | --- | --- |
| Bronze | Immutable raw events exactly as received | Object storage JSONL/Parquet |
| Silver | Validated, typed, normalized records plus rejected-record quarantine | Delta/Iceberg/Hudi tables |
| Gold | Business-ready aggregate snapshots for analytics and serving | Warehouse tables, marts, or feature store |

## Gold marts

### Event type summary

Each row contains:

- `event_type`
- `event_count`
- `total_amount`

### Customer summary

Each row contains:

- `customer_id`
- `event_count`
- `total_amount`
- `event_types`

## Production adapter checklist

- Streaming source: Kafka, Kinesis, Pub/Sub, Event Hubs, CDC logs, or managed stream processors.
- Transactional sink: Delta Lake, Apache Iceberg, Apache Hudi, warehouse tables, or object storage with compaction.
- Schema and contracts: schema registry validation, compatibility checks, and dead-letter routing by failure category.
- Observability: publish `PipelineMetrics`, data quality rates, lag, and freshness to monitoring systems.
- Reliability: durable checkpoint storage, retries, idempotent writes, and backfill/replay tooling.
