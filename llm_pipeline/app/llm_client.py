import json

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings
from app.schemas import ClassificationOut, TicketIn

SYSTEM_PROMPT = (
    "You are a strict support ticket classifier. "
    "Return ONLY valid JSON with keys: category, confidence, rationale. "
    "category must be one of billing|technical|cancellation|other. "
    "confidence must be between 0 and 1. rationale must be short."
)


class LLMClassifier:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self._client = OpenAI(api_key=settings.openai_api_key, timeout=settings.llm_timeout_seconds)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    def classify(self, ticket: TicketIn) -> ClassificationOut:
        user_prompt = (
            f"Ticket ID: {ticket.ticket_id}\n"
            f"Subject: {ticket.subject}\n"
            f"Body: {ticket.body}\n"
            f"Customer tier: {ticket.customer_tier}"
        )

        response = self._client.chat.completions.create(
            model=settings.model_name,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        raw = response.choices[0].message.content or "{}"
        parsed = json.loads(raw)
        return ClassificationOut(**parsed)
