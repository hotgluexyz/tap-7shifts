"""Thread-safe request pacing for the 7shifts API token limit."""

from __future__ import annotations

import threading
import time
from collections import deque

# 7shifts documents 10 requests/second per access token; stay under for headroom
DEFAULT_MAX_REQUESTS_PER_SECOND = 9
_WINDOW_SECONDS = 1.0


class PerSecondRateLimiter:
    """Block until another request may start within a rolling one-second window."""

    def __init__(self, max_requests_per_second: int = DEFAULT_MAX_REQUESTS_PER_SECOND) -> None:
        self._max_requests = max_requests_per_second
        self._lock = threading.Lock()
        # Monotonic timestamps of recent request starts (shared across tap threads)
        self._starts: deque[float] = deque()

    def wait_turn(self) -> None:
        """Wait until starting a new request stays under the per-second cap."""
        with self._lock:
            while True:
                now = time.monotonic()

                # Compute the time before which request starts are no longer valid
                cutoff = now - _WINDOW_SECONDS

                # Drop request start times that fell outside the rolling 1s window
                while self._starts and self._starts[0] <= cutoff:
                    self._starts.popleft()
                
                # If there's room for another request, mark the start time and return
                if len(self._starts) < self._max_requests:
                    self._starts.append(now)
                    return
                
                # Otherwise, compute how long to sleep to make room for the next request
                sleep_for = self._starts[0] + _WINDOW_SECONDS - now
                if sleep_for > 0:
                    time.sleep(sleep_for)
