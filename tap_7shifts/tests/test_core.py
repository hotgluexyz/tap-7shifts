"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import json
from unittest.mock import MagicMock, patch

import pytest
from hotglue_singer_sdk.testing import get_standard_tap_tests

from tap_7shifts.tap import Tap7Shifts

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "client_id": "test-client-id",
    "client_secret": "test-client-secret",
    "guid": "test-guid",
    "company_id": "test-company-id",
}


@pytest.mark.parametrize(
    "standard_tap_test",
    [
        test
        for test in get_standard_tap_tests(Tap7Shifts, config=SAMPLE_CONFIG)
        if test.__name__ != "_test_stream_connections"
    ],
)
def test_standard_tap_features(standard_tap_test):
    """Run the SDK checks that do not require a live 7shifts account."""
    standard_tap_test()


def test_access_token_support_fetches_oauth_token(tmp_path):
    """Access-token support uses 7shifts' OAuth token endpoint."""
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(SAMPLE_CONFIG))
    tap = Tap7Shifts(config=config_path)
    token_response = MagicMock()
    token_response.json.return_value = {"access_token": "seven-shifts-access-token"}

    with patch(
        "hotglue_singer_sdk.authenticators.requests.post", return_value=token_response
    ) as request_token:
        assert Tap7Shifts.fetch_access_token(tap) == {
            "access_token": "seven-shifts-access-token"
        }

    request_token.assert_called_once_with(
        "https://app.7shifts.com/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
            "scope": "v1_access companies:read locations:read",
        },
        auth=None,
    )
    assert json.loads(config_path.read_text())["access_token"] == "seven-shifts-access-token"
