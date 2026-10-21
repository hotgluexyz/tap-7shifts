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


def test_access_token_support_uses_each_connector_credentials(tmp_path):
    """Access-token support uses a connector-bound OAuth authenticator."""
    first_config_path = tmp_path / "first-config.json"
    first_config_path.write_text(json.dumps(SAMPLE_CONFIG))
    second_config_path = tmp_path / "second-config.json"
    second_config = {
        **SAMPLE_CONFIG,
        "client_id": "second-client-id",
        "client_secret": "second-client-secret",
    }
    second_config_path.write_text(json.dumps(second_config))
    first_tap = Tap7Shifts(config=first_config_path)
    second_tap = Tap7Shifts(config=second_config_path)
    first_response = MagicMock()
    first_response.json.return_value = {"access_token": "first-access-token"}
    second_response = MagicMock()
    second_response.json.return_value = {"access_token": "second-access-token"}

    with patch(
        "hotglue_singer_sdk.authenticators.requests.post",
        side_effect=[first_response, second_response],
    ) as request_token:
        assert Tap7Shifts.fetch_access_token(first_tap) == {
            "access_token": "first-access-token"
        }
        assert Tap7Shifts.fetch_access_token(second_tap) == {
            "access_token": "second-access-token"
        }

    assert request_token.call_args_list[0].kwargs["data"]["client_id"] == "test-client-id"
    assert request_token.call_args_list[0].kwargs["data"]["client_secret"] == "test-client-secret"
    assert request_token.call_args_list[1].kwargs["data"]["client_id"] == "second-client-id"
    assert request_token.call_args_list[1].kwargs["data"]["client_secret"] == "second-client-secret"
    assert json.loads(first_config_path.read_text())["access_token"] == "first-access-token"
    assert json.loads(second_config_path.read_text())["access_token"] == "second-access-token"
