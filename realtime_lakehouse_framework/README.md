# Realtime Lakehouse Framework

A lightweight Python starter framework for real-time data processing on a data lakehouse. It models the common medallion architecture:

- **Bronze**: append-only raw events as they arrive.
- **Silver**: validated and normalized records with bad data separated.
- **Gold**: curated aggregates ready for analytics and serving.

The project intentionally uses the Python standard library so the scaffold can run locally before you connect production services such as Kafka, Flink/Spark, object storage, Delta/Iceberg/Hudi tables, and orchestration tools.

## Architecture

```text
Event Sources -> Stream Reader -> Bronze Sink -> Silver Quality Rules -> Gold Aggregates
      |              |                 |                |                    |
   APIs/CDC       Micro-batch       Raw JSONL       Clean JSONL        JSON metrics
   Kafka/etc.     checkpoints       partitions      dead letters       serving layer
```

## Quick start

```bash
cd realtime_lakehouse_framework
python -m realtime_lakehouse.cli --config configs/local_pipeline.json
```

The command reads sample events from `examples/events.jsonl`, writes medallion outputs into `./lakehouse`, and stores offsets in `./checkpoints`.

## Project layout

```text
configs/                  Local pipeline configuration
examples/                 Example streaming input data
src/realtime_lakehouse/   Framework package
tests/                    Unit tests for the pipeline components
```

## Extending for production

1. Replace `JsonLinesSource` with adapters for Kafka, Kinesis, Pub/Sub, CDC logs, or managed streaming services.
2. Replace `JsonLinesSink` with Delta Lake, Apache Iceberg, Apache Hudi, or cloud object storage writers.
3. Add schema registry checks in `QualityRuleSet` for contract enforcement.
4. Publish `PipelineMetrics` to observability systems such as Prometheus, OpenTelemetry, or CloudWatch.
5. Run the CLI from an orchestrator or container platform with durable checkpoint storage.
