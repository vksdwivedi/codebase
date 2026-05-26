from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.queue import job_queue
from app.schemas import IngestResponse, TicketIn
from app.storage import fetch_results, fetch_review
from app.worker import TicketWorker

worker = TicketWorker()


@asynccontextmanager
async def lifespan(_: FastAPI):
    worker.start()
    yield
    worker.stop()


app = FastAPI(title="LLM Ticket Classification Pipeline", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(ticket: TicketIn) -> IngestResponse:
    job_queue.put(ticket)
    return IngestResponse(status="queued", ticket_id=ticket.ticket_id)


@app.get("/results")
def results(limit: int = 50) -> dict[str, object]:
    items = fetch_results(limit=limit)
    return {"count": len(items), "items": items}


@app.get("/review")
def review(limit: int = 50) -> dict[str, object]:
    items = fetch_review(limit=limit)
    return {"count": len(items), "items": items}
