"""Command-line entrypoint for the realtime lakehouse framework."""

from __future__ import annotations

import argparse
import json

from realtime_lakehouse.config import PipelineConfig
from realtime_lakehouse.pipeline import LakehousePipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a realtime lakehouse micro-batch pipeline.")
    parser.add_argument("--config", required=True, help="Path to a pipeline JSON configuration file.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pipeline = LakehousePipeline(PipelineConfig.from_json(args.config))
    metrics = pipeline.run_once()
    print(json.dumps(metrics.__dict__, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
