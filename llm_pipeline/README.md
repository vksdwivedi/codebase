# LLM Pipeline (FastAPI + Background Worker)

This project implements a **complete LLM data pipeline** for one practical use case:
**support ticket classification** into `billing`, `technical`, `cancellation`, or `other`.

## Architecture

`Ingest API -> In-memory Queue -> Background Worker -> LLM -> Schema Validation -> Result/Review Store`

- API endpoint queues incoming tickets.
- Worker pulls tickets, calls the LLM, validates strict JSON output, and routes:
  - high confidence => results
  - low confidence or errors => human review queue

## Setup

```bash
cd llm_pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

## API endpoints

- `GET /health`
- `POST /ingest`
- `GET /results`
- `GET /review`

### Example request

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id":"T-1001",
    "subject":"I was charged twice",
    "body":"My card was charged twice for the same order.",
    "customer_tier":"premium"
  }'
```

## Testing

```bash
PYTHONPATH=. pytest -q
```

## Production hardening checklist

1. Replace in-memory queue with Redis + Celery/RQ.
2. Replace in-memory stores with Postgres.
3. Add metrics (latency, failures, JSON parse errors, cost).
4. Add PII redaction before LLM calls.
5. Add offline evaluation dataset and CI gate.
