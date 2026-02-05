"""Stream type classes for tap-7shifts."""

from typing import Optional

from hotglue_singer_sdk import typing as th

from tap_7shifts.client import SevenShiftsStream


class CompaniesStream(SevenShiftsStream):
    """Companies stream - list of companies from 7shifts API."""

    name = "companies"
    path = "companies"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("uuid", th.StringType),
        th.Property("country", th.StringType),
        th.Property("photo", th.StringType),
        th.Property("trial", th.BooleanType),
        th.Property("plan_id", th.StringType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property("expires", th.DateTimeType),
        th.Property("days_to_expire", th.IntegerType),
        th.Property("converted", th.StringType),
        th.Property("pos", th.StringType),
        th.Property("status", th.StringType),
        th.Property("start_week_on", th.IntegerType),
        th.Property(
            "meta",
            th.ObjectType(
                th.Property("onboarding_complete", th.BooleanType),
                th.Property("buy_now", th.BooleanType),
                th.Property("employee_count_range", th.StringType),
                th.Property("signup_utm_source", th.StringType),
                th.Property("signup_form_type", th.StringType),
                th.Property("utm_medium", th.StringType),
                th.Property("utm_source", th.StringType),
                th.Property("signup_content_source", th.StringType),
                th.Property("icp_segment", th.StringType),
                th.Property("ai_importer_invoked", th.BooleanType),
                th.Property("declared_number_of_locations", th.IntegerType),
                th.Property("marketing_site_visitor_uuid", th.StringType),
                th.Property("pricing_test_aggregate_id", th.StringType),
                th.Property("trial_checklist_stored_locally", th.BooleanType),
            ),
        ),
        th.Property("active", th.BooleanType),
        th.Property("coupon", th.StringType),
    ).to_dict()


class LocationsStream(SevenShiftsStream):
    """Locations stream - list of locations for the company (company_id from config)."""

    name = "locations"
    path = "company/{company_id}/locations"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("company_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("country", th.StringType),
        th.Property("state", th.StringType),
        th.Property("city", th.StringType),
        th.Property("formatted_address", th.StringType),
        th.Property("lat", th.NumberType),
        th.Property("lng", th.NumberType),
        th.Property("place_id", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("timezone_updated", th.BooleanType),
        th.Property("hash", th.StringType),
        th.Property("mapping_id", th.StringType),
        th.Property("department_based_budget", th.BooleanType),
        th.Property("holiday_pay", th.BooleanType),
        th.Property("auto_send_log_book_time", th.StringType),
        th.Property("mon_hours_close", th.StringType),
        th.Property("tue_hours_close", th.StringType),
        th.Property("wed_hours_close", th.StringType),
        th.Property("thu_hours_close", th.StringType),
        th.Property("fri_hours_close", th.StringType),
        th.Property("sat_hours_close", th.StringType),
        th.Property("sun_hours_close", th.StringType),
        th.Property("mon_hours_open", th.StringType),
        th.Property("tue_hours_open", th.StringType),
        th.Property("wed_hours_open", th.StringType),
        th.Property("thu_hours_open", th.StringType),
        th.Property("fri_hours_open", th.StringType),
        th.Property("sat_hours_open", th.StringType),
        th.Property("sun_hours_open", th.StringType),
        th.Property("mon_is_closed", th.BooleanType),
        th.Property("tue_is_closed", th.BooleanType),
        th.Property("wed_is_closed", th.BooleanType),
        th.Property("thu_is_closed", th.BooleanType),
        th.Property("fri_is_closed", th.BooleanType),
        th.Property("sat_is_closed", th.BooleanType),
        th.Property("sun_is_closed", th.BooleanType),
        th.Property("shift_feedback", th.BooleanType),
        th.Property("message", th.StringType),
        th.Property("deleted", th.BooleanType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()


class DepartmentsStream(SevenShiftsStream):
    """Departments stream - list of departments for the company (company_id from config)."""

    name = "departments"
    path = "company/{company_id}/departments"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("company_id", th.IntegerType),
        th.Property("location_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("default", th.BooleanType),
        th.Property("deleted", th.BooleanType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()


class ShiftsStream(SevenShiftsStream):
    """Shifts stream - list of shifts for the company (company_id from config)."""

    name = "shifts"
    path = "company/{company_id}/shifts"
    replication_format = "%Y-%m-%dT%H:%M:%SZ"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("department_id", th.IntegerType),
        th.Property("location_id", th.IntegerType),
        th.Property("company_id", th.IntegerType),
        th.Property("role_id", th.IntegerType),
        th.Property("station", th.IntegerType),
        th.Property("station_name", th.StringType),
        th.Property("station_id", th.IntegerType),
        th.Property("start", th.DateTimeType),
        th.Property("end", th.DateTimeType),
        th.Property("close", th.BooleanType),
        th.Property("business_decline", th.BooleanType),
        th.Property("hourly_wage", th.IntegerType),
        th.Property("notes", th.StringType),
        th.Property("draft", th.BooleanType),
        th.Property("notified", th.BooleanType),
        th.Property("open", th.BooleanType),
        th.Property("unassigned", th.BooleanType),
        th.Property("unassigned_skill_level", th.IntegerType),
        th.Property("open_offer_type", th.StringType),
        th.Property("publish_status", th.StringType),
        th.Property("attendance_status", th.StringType),
        th.Property("late_minutes", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property("soft_deleted", th.StringType),
        th.Property("deleted", th.BooleanType),
        th.Property(
            "breaks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("shift_id", th.IntegerType),
                    th.Property("start", th.DateTimeType),
                    th.Property("end", th.DateTimeType),
                    th.Property("name", th.StringType),
                    th.Property("length", th.IntegerType),
                    th.Property("break_type_id", th.IntegerType),
                    th.Property("type", th.StringType),
                )
            ),
        ),
    ).to_dict()


class UsersStream(SevenShiftsStream):
    """Users stream - list of users for the company (company_id from config)."""

    name = "users"
    path = "company/{company_id}/users"

    def get_child_context(self, record: dict, context: Optional[dict] = None) -> dict:
        """Provide user_id for child streams (e.g. UserWagesStream)."""
        return {"user_id": record["id"]}

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("identity_id", th.IntegerType),
        th.Property("company_id", th.IntegerType),
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("preferred_first_name", th.StringType),
        th.Property("preferred_last_name", th.StringType),
        th.Property("pronouns", th.StringType),
        th.Property("email", th.StringType),
        th.Property("mobile_number", th.StringType),
        th.Property("home_number", th.StringType),
        th.Property("address", th.StringType),
        th.Property("postal_zip", th.StringType),
        th.Property("city", th.StringType),
        th.Property("prov_state", th.StringType),
        th.Property("invite_status", th.StringType),
        th.Property("last_login", th.DateTimeType),
        th.Property("active", th.BooleanType),
        th.Property("photo", th.StringType),
        th.Property("notes", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("type", th.StringType),
        th.Property("punch_id", th.StringType),
        th.Property("employee_id", th.StringType),
        th.Property("max_weekly_hours", th.StringType),
        th.Property("invited", th.DateTimeType),
        th.Property("invite_accepted", th.DateTimeType),
        th.Property("is_new", th.BooleanType),
        th.Property("birth_date", th.StringType),
        th.Property("language", th.StringType),
        th.Property("appear_as_employee", th.BooleanType),
        th.Property("subscribe_to_updates", th.BooleanType),
        th.Property("skill_level", th.IntegerType),
        th.Property("hourly_wage", th.IntegerType),
        th.Property("wage_type", th.StringType),
        th.Property("sms_me_schedules", th.BooleanType),
        th.Property("notify_ot_risk", th.BooleanType),
        th.Property("push", th.BooleanType),
        th.Property("permissions_template_id", th.IntegerType),
        th.Property("onboarding_required", th.BooleanType),
        th.Property("reactivation_status", th.StringType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()


class UserWagesStream(SevenShiftsStream):
    """User wages stream - one record per user with current_wages and upcoming_wages as arrays (matches API shape)."""

    name = "user_wages"
    path = "company/{company_id}/users/{user_id}/wages"
    parent_stream_type = UsersStream
    primary_keys = ["user_id"]
    replication_key = None
    parallelization_limit = 10
    records_jsonpath = "$.data"
    state_partitioning_keys = ["user_id"]
    ignore_parent_replication_key = True

    def get_context_state(self, context: Optional[dict]) -> dict:
        """Use a single stream state (no partitions) so we don't list every user_id in state."""
        return self.stream_state

    _wage_object = th.ObjectType(
        th.Property("id", th.IntegerType),
        th.Property("effective_date", th.StringType),
        th.Property("role_id", th.IntegerType),
        th.Property("wage_type", th.StringType),
        th.Property("wage_cents", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
    )

    schema = th.PropertiesList(
        th.Property("user_id", th.IntegerType),
        th.Property("current_wages", th.ArrayType(_wage_object)),
        th.Property("upcoming_wages", th.ArrayType(_wage_object)),
        th.Property("wage_type", th.StringType),
    ).to_dict()


class UserAssignmentsStream(SevenShiftsStream):
    """User assignments stream - one record per user with locations, departments, and roles as arrays (matches API shape)."""

    name = "user_assignments"
    path = "company/{company_id}/users/{user_id}/assignments"
    parent_stream_type = UsersStream
    primary_keys = ["user_id"]
    replication_key = None
    parallelization_limit = 10
    records_jsonpath = "$.data"
    state_partitioning_keys = ["user_id"]
    ignore_parent_replication_key = True

    def get_context_state(self, context: Optional[dict]) -> dict:
        """Use a single stream state (no partitions) so we don't list every user_id in state."""
        return self.stream_state

    schema = th.PropertiesList(
        th.Property("user_id", th.IntegerType),
        th.Property(
            "locations",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("company_id", th.IntegerType),
                    th.Property("timezone", th.StringType),
                    th.Property("hash", th.StringType),
                    th.Property("formatted_address", th.StringType),
                    th.Property("lat", th.NumberType),
                    th.Property("lng", th.NumberType),
                    th.Property("country", th.StringType),
                    th.Property("city", th.StringType),
                    th.Property("state", th.StringType),
                )
            ),
        ),
        th.Property(
            "departments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("company_id", th.IntegerType),
                    th.Property("location_id", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("appear_on_schedule", th.BooleanType),
                )
            ),
        ),
        th.Property(
            "roles",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("company_id", th.IntegerType),
                    th.Property("location_id", th.IntegerType),
                    th.Property("department_id", th.IntegerType),
                    th.Property("name", th.StringType),
                    th.Property("is_primary", th.BooleanType),
                    th.Property("skill_level", th.IntegerType),
                    th.Property("sort", th.IntegerType),
                )
            ),
        ),
    ).to_dict()
