"""7shifts tap class."""

from typing import List

from hotglue_singer_sdk import Stream, Tap
from hotglue_singer_sdk import typing as th

from tap_7shifts.streams import (
    CompaniesStream,
    DepartmentsStream,
    LocationsStream,
    RolesStream,
    ShiftsStream,
    TimePunchesStream,
    UserAssignmentsStream,
    UserWagesStream,
    UsersStream,
)

STREAM_TYPES = [
    CompaniesStream,
    LocationsStream,
    DepartmentsStream,
    RolesStream,
    ShiftsStream,
    TimePunchesStream,
    UsersStream,
    UserWagesStream,
    UserAssignmentsStream,
]


class Tap7Shifts(Tap):
    """7shifts tap class."""

    name = "tap-7shifts"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
        ),
        th.Property(
            "guid",
            th.StringType,
            required=True,
        ),
        th.Property(
            "company_id",
            th.StringType,
            description="7shifts company ID (used for company-scoped endpoints such as locations).",
            required=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    Tap7Shifts.cli()
