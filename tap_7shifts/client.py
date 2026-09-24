"""REST client handling, including SevenShiftsStream base class."""

from __future__ import annotations

from typing import Any, Callable, Dict, Generator, Optional

import backoff
import requests
from hotglue_singer_sdk.helpers._network import giveup_oserror_not_transient_network
from hotglue_singer_sdk.streams import RESTStream
from memoization import cached

from tap_7shifts.auth import SevenShiftsAuthenticator
from tap_7shifts.rate_limit import PerSecondRateLimiter

# Shared by every stream in the tap process (parallel child sync uses one token).
_REQUEST_RATE_LIMITER = PerSecondRateLimiter()


class SevenShiftsStream(RESTStream):
    """Base stream with tap-wide request pacing and 429 retry policy."""

    url_base = "https://api.7shifts.com/v2/"
    primary_keys = ["id"]
    replication_key = "modified"
    replication_format = "%Y-%m-%d"
    records_jsonpath = "$.data[*]"
    next_page_token_jsonpath = "$.meta.cursor.next"
    limit = 500

    @property
    @cached
    def authenticator(self) -> SevenShiftsAuthenticator:
        """Return a new authenticator object."""
        return SevenShiftsAuthenticator.create_for_stream(self)

    @property
    @cached
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = super().http_headers
        headers["x-company-guid"] = self.config["guid"]
        return headers

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["cursor"] = next_page_token
        if self.limit:
            params["limit"] = self.limit
        if self.replication_key and context is not None:
            start_date = self.get_starting_time(context, is_inclusive=True)
            if start_date:
                params["modified_since"] = start_date.strftime(self.replication_format)
        return params

    def _request(
        self, prepared_request: requests.PreparedRequest, context: Optional[dict]
    ) -> requests.Response:
        """Gate each HTTP attempt (including backoff retries) on the shared per-second limiter."""
        _REQUEST_RATE_LIMITER.wait_turn()
        return super()._request(prepared_request, context)

    def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
        """Wait long enough to clear 7shifts' documented one-minute throttle on 429."""
        return backoff.expo(factor=5, max_value=60)  # type: ignore[return-value]

    def backoff_max_tries(self) -> int:
        """Allow retries to span the one-minute block after sustained 429s."""
        return 8

    def request_decorator(self, func: Callable) -> Callable:
        """Retry with deterministic waits so jitter does not under-shoot the throttle window."""
        return backoff.on_exception(
            self.backoff_wait_generator,
            self.backoff_exceptions(),
            max_tries=self.backoff_max_tries,
            on_backoff=self.backoff_handler,
            giveup=giveup_oserror_not_transient_network,
            jitter=None,
        )(func)
