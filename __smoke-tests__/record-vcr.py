from hotglue_smoke_test.vcr.tap import VCRTapTestRunner


class ConnectorTapTestRunner(VCRTapTestRunner):
    # 7shifts sends the company GUID in this header.
    FILTER_HEADERS = [*VCRTapTestRunner.FILTER_HEADERS, "x-company-guid"]
    # Scrub the GUID in config; the base already covers client credentials.
    TOKEN_KEYS = [*VCRTapTestRunner.TOKEN_KEYS, "guid"]
    PRESERVE_KEYS = {"id", "user_id", "modified", "next", "expires_in"}

    def module(self) -> str:
        return "tap_7shifts.tap"

    def launch(self):
        from tap_7shifts.tap import Tap7Shifts

        Tap7Shifts.cli()


if __name__ == "__main__":
    ConnectorTapTestRunner.main()
