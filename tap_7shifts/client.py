"""REST client handling, including SevenShiftsStream base class."""

from typing import Any, Dict, Optional

import requests
from hotglue_singer_sdk.streams import RESTStream
from memoization import cached

from tap_7shifts.auth import SevenShiftsAuthenticator


class SevenShiftsStream(RESTStream):
    """7shifts stream class (base)."""

    url_base = "https://api.7shifts.com/v2/"
    primary_keys = ["id"]
    replication_key = "modified"
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
                params["modified_since"] = start_date.strftime("%Y-%m-%d")
        return params
