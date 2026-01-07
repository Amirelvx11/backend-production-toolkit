import time
import uuid
from contextlib import AbstractContextManager
from backend_toolkit.logger import get_logger

logger = get_logger("backend toolkit monitoring - run tracker")


class RunTracker(AbstractContextManager):
    def __init__(self, name: str):
        self.name = name
        self.run_id = str(uuid.uuid4())
        self._start: float | None = None

    def __enter__(self):
        self._start = time.time()
        logger.info(
            f"run-started: {self.name}",
            extra={"run_id": self.run_id},
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        duration = round(time.time() - self._start, 4)

        if exc:
            logger.error(
                f"run-failed: {self.name}",
                extra={"run_id": self.run_id},
                exc_info=True,
            )
        else:
            logger.info(
                f"run-finished: {self.name} duration={duration}s",
                extra={"run_id": self.run_id},
            )
        return False
