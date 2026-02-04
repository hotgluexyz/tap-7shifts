"""7shifts Authentication."""

from hotglue_singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


# Default scopes for 7shifts API; scope format: "v1_access {ADDITIONAL_SCOPES}"
DEFAULT_OAUTH_SCOPES = "v1_access companies:read locations:read"


class SevenShiftsAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator for 7shifts OAuth2 client_credentials.

    7shifts expects a form-encoded POST body (no Basic auth):
    grant_type=client_credentials&client_id=...&client_secret=...&scope=...
    """

    @property
    def oauth_request_body(self) -> dict:
        """Form body for token request (application/x-www-form-urlencoded)."""
        return {
            "grant_type": "client_credentials",
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "scope": self.oauth_scopes or DEFAULT_OAUTH_SCOPES,
        }

    @classmethod
    def create_for_stream(cls, stream) -> "SevenShiftsAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="https://app.7shifts.com/oauth2/token",
            oauth_scopes=DEFAULT_OAUTH_SCOPES,
        )
