"""Stream type classes for tap-7shifts."""

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
