"""7shifts Authentication."""

import requests

from hotglue_singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from hotglue_singer_sdk.helpers._util import utc_now


# Default scopes for 7shifts API; scope format: "v1_access {ADDITIONAL_SCOPES}"
DEFAULT_OAUTH_SCOPES = "v1_access companies:read locations:read"


class SevenShiftsAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator for 7shifts OAuth2 client_credentials."""

    @property
    def oauth_request_body(self) -> dict:
        """Form body for token request."""
        return {
            "grant_type": "client_credentials",
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "scope": self.oauth_scopes or DEFAULT_OAUTH_SCOPES,
        }

    def update_access_token(self) -> None:
        """Fetch a new access token and keep it in memory only (do not persist to config)."""
        request_time = utc_now()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(
            self.auth_endpoint, data=auth_request_payload, auth=self.request_auth()
        )
        try:
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
        except Exception as ex:
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            )
        token_json = token_response.json()
        self.access_token = token_json["access_token"]
        self.expires_in = token_json.get("expires_in", self._default_expiration) + int(request_time.timestamp())
        self.last_refreshed = request_time

    @classmethod
    def create_for_stream(cls, stream) -> "SevenShiftsAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="https://app.7shifts.com/oauth2/token",
            oauth_scopes=DEFAULT_OAUTH_SCOPES,
        )
