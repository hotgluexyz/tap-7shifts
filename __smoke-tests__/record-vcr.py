import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import vcr
from hotglue_smoke_test.vcr.tap import VCRTapTestRunner


class Runner(VCRTapTestRunner):
    PRESERVE_KEYS = {
        "cursor",
        "id",
        "user_id",
        "company_id",
        "location_id",
        "department_id",
        "role_id",
        "shift_id",
    }

    def module(self) -> str:
        return "tap_7shifts.tap"

    def launch(self):
        from tap_7shifts.tap import Tap7Shifts
        from tap_7shifts.streams import UserAssignmentsStream, UserWagesStream

        UserAssignmentsStream.parallelization_limit = 1
        UserWagesStream.parallelization_limit = 1

        Tap7Shifts.cli()

    def scrub_uri(self, uri: str) -> str:
        parts = urlsplit(uri)
        path = re.sub(r"/company/[^/]+/", "/company/1/", parts.path)
        path = re.sub(
            r"/users/([^/]+)/",
            lambda match: f"/users/{self._scrub_identifier(match.group(1))}/",
            path,
        )
        query = urlencode(
            [(key, "<scrubbed-cursor>" if key == "cursor" else value)
             for key, value in parse_qsl(parts.query, keep_blank_values=True)]
        )
        return urlunsplit((parts.scheme, parts.netloc, path, query, parts.fragment))

    def _scrub_identifier(self, identifier: str) -> str:
        mapping = getattr(self, "_identifier_map", {})
        self._identifier_map = mapping
        return mapping.setdefault(identifier, str(1000 + len(mapping)))

    def scrub_response_body(self, body, faker, cache):
        def scrub_cursor(match):
            value = match.group(2)
            mapping = getattr(self, "_cursor_map", {})
            self._cursor_map = mapping
            replacement = mapping.setdefault(value, f"scrubbed-cursor-{len(mapping) + 1}")
            return f'{match.group(1)}"{replacement}"'

        scrubbed = super().scrub_response_body(body, faker, cache)
        scrubbed = re.sub(r'("(?:current|prev|next)"\s*:\s*)"([^"]+)"', scrub_cursor, scrubbed)
        scrubbed = re.sub(r'("company_id"\s*:\s*)\d+', r"\g<1>1", scrubbed)
        scrubbed = re.sub(
            r'("(?:id|user_id|location_id|department_id|role_id|shift_id)"\s*:\s*)(\d+)',
            lambda match: match.group(1) + self._scrub_identifier(match.group(2)),
            scrubbed,
        )
        return scrubbed

    def vcr_use_cassette(self, filter_query_parameters):
        """Match child requests after normalizing scrubbed user IDs."""
        vcr.default_vcr.register_matcher(
            "normalized_path",
            lambda left, right: re.sub(r"/users/[^/]+/", "/users/1/", urlsplit(left.uri).path)
            == re.sub(r"/users/[^/]+/", "/users/1/", urlsplit(right.uri).path),
        )
        vcr.default_vcr.register_matcher(
            "normalized_query",
            lambda left, right: sorted((k, v) for k, v in parse_qsl(urlsplit(left.uri).query) if k != "cursor")
            == sorted((k, v) for k, v in parse_qsl(urlsplit(right.uri).query) if k != "cursor"),
        )
        return vcr.use_cassette(
            self.vcr_cassette_path,
            decode_compressed_response=True,
            filter_headers=list(self.FILTER_HEADERS),
            filter_post_data_parameters=list(self.TOKEN_KEYS),
            filter_query_parameters=filter_query_parameters,
            before_record_response=self.before_record_response,
            match_on=["method", "scheme", "host", "port", "normalized_path", "normalized_query"],
        )


if __name__ == "__main__":
    Runner.main()
