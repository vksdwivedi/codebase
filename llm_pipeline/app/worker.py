import logging
import threading
from queue import Empty

from app.config import settings
from app.llm_client import LLMClassifier
from app.queue import job_queue
from app.storage import save_for_review, save_result

logger = logging.getLogger(__name__)


class TicketWorker:
    def __init__(self) -> None:
        self._classifier = LLMClassifier()
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True, name="ticket-worker")
        self._thread.start()
        logger.info("Ticket worker started")

    def stop(self) -> None:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        logger.info("Ticket worker stopped")

    def _loop(self) -> None:
        while self._running:
            try:
                ticket = job_queue.get(timeout=1)
            except Empty:
                continue

            try:
                result = self._classifier.classify(ticket)
                payload = result.model_dump()
                if result.confidence < settings.low_confidence_threshold:
                    save_for_review(ticket.ticket_id, payload=payload)
                else:
                    save_result(ticket.ticket_id, result=payload)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Worker failed for ticket_id=%s", ticket.ticket_id)
                save_for_review(ticket.ticket_id, error=str(exc))
            finally:
                job_queue.task_done()
