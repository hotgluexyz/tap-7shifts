"""Tests for per-second API pacing."""

import threading
import time

from tap_7shifts.rate_limit import PerSecondRateLimiter


def test_per_second_limiter_blocks_third_start_when_cap_is_two():
    """A rolling 1s cap of 2 should delay a third start until the window moves."""
    limiter = PerSecondRateLimiter(max_requests_per_second=2)
    limiter.wait_turn()
    limiter.wait_turn()
    start = time.monotonic()
    limiter.wait_turn()
    elapsed = time.monotonic() - start
    assert elapsed >= 0.9


def test_per_second_limiter_shared_across_threads():
    """Concurrent callers should share one cap (same as tap-wide limiter)."""
    limiter = PerSecondRateLimiter(max_requests_per_second=3)
    barrier = threading.Barrier(4)

    def burst() -> None:
        barrier.wait()
        limiter.wait_turn()

    start = time.monotonic()
    threads = [threading.Thread(target=burst) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.monotonic() - start
    assert elapsed >= 0.9
