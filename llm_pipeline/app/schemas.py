from typing import Literal, Optional

from pydantic import BaseModel, Field


class TicketIn(BaseModel):
    ticket_id: str
    subject: str
    body: str
    customer_tier: Optional[str] = "standard"


class ClassificationOut(BaseModel):
    category: Literal["billing", "technical", "cancellation", "other"]
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=1, max_length=200)


class IngestResponse(BaseModel):
    status: Literal["queued"]
    ticket_id: str
