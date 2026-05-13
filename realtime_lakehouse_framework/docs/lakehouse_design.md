# Lakehouse Design Notes

## Goals

- Support near real-time ingestion with checkpointed micro-batches.
- Preserve raw data for replay, audit, and backfills.
- Promote records through bronze, silver, and gold layers.
- Keep quality failures queryable instead of silently dropping them.

## Layer contracts

| Layer | Purpose | Example storage |
| --- | --- | --- |
| Bronze | Immutable raw events exactly as received | Object storage JSONL/Parquet |
| Silver | Validated, typed, deduplicated records | Delta/Iceberg/Hudi tables |
| Gold | Business-ready aggregates and serving tables | Warehouse tables or feature store |

## Production adapters

The local implementation is intentionally small. Production deployments should add adapters for streaming sources, transactional table formats, schema registry validation, and observability sinks.
