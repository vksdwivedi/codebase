from queue import Queue

from app.schemas import TicketIn

job_queue: Queue[TicketIn] = Queue()
