"""Client-side request pacing."""

from __future__ import annotations

import threading
import time
from collections import deque


class RateLimiter:
    """Sliding-window limiter used internally by the client."""

    def __init__(self, max_requests: int = 90, period_seconds: float = 60.0) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be >= 1")
        if period_seconds <= 0:
            raise ValueError("period_seconds must be > 0")
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a request slot is available, then consume it."""
        while True:
            with self._lock:
                now = time.monotonic()
                cutoff = now - self.period_seconds
                while self._timestamps and self._timestamps[0] <= cutoff:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.max_requests:
                    self._timestamps.append(now)
                    return

                wait = self._timestamps[0] + self.period_seconds - now

            if wait > 0:
                time.sleep(wait)
