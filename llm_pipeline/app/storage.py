from datetime import datetime, timezone
from threading import Lock
from typing import Any

RESULTS: list[dict[str, Any]] = []
REVIEW: list[dict[str, Any]] = []
_lock = Lock()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_result(ticket_id: str, result: dict[str, Any]) -> None:
    with _lock:
        RESULTS.append({"ts": _utc_now(), "ticket_id": ticket_id, **result})


def save_for_review(ticket_id: str, payload: dict[str, Any] | None = None, error: str | None = None) -> None:
    with _lock:
        REVIEW.append({"ts": _utc_now(), "ticket_id": ticket_id, "payload": payload, "error": error})


def fetch_results(limit: int = 50) -> list[dict[str, Any]]:
    with _lock:
        return RESULTS[-limit:]


def fetch_review(limit: int = 50) -> list[dict[str, Any]]:
    with _lock:
        return REVIEW[-limit:]
