"""Tests for SevenShiftsStream HTTP retry and pacing hooks."""

from unittest.mock import MagicMock, patch

import requests

from tap_7shifts.client import _REQUEST_RATE_LIMITER
from tap_7shifts.streams import CompaniesStream


def test_backoff_max_tries():
    """429 retries should outlast the default SDK attempt count."""
    stream = CompaniesStream(tap=MagicMock())
    assert stream.backoff_max_tries() == 8


def test_request_waits_on_shared_rate_limiter():
    """Each HTTP attempt should pass through the process-wide limiter."""
    stream = CompaniesStream(tap=MagicMock())
    prepared = requests.Request("GET", "https://example.com").prepare()
    sentinel = MagicMock(status_code=200)
    with patch.object(_REQUEST_RATE_LIMITER, "wait_turn") as wait_turn:
        with patch(
            "hotglue_singer_sdk.streams.rest.RESTStream._request",
            return_value=sentinel,
        ) as parent_request:
            result = stream._request(prepared, None)
    wait_turn.assert_called_once()
    parent_request.assert_called_once()
    assert result is sentinel
