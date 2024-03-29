from basevn.pipeline.interface import Resource
from basevn.utils import parse_unix_ts
from basevn.pipeline.ehiring import openings
from basevn.repo import EHIRING, get_multiple, get_single

pipeline = Resource(
    name="EHiring_Candidates",
    get=get_multiple(
        get_listing_fn=openings.pipeline.get,
        get_one_fn=get_single(
            EHIRING,
            "candidate/list",
            lambda res: res["candidates"] if "candidates" in res else [],
            lambda page: {"page": page},
            1,
        ),
        id_fn=lambda opening: opening["id"],
        body_fn=lambda id: {"opening_id": id},
    ),
    transform=lambda rows: [
        {
            "id": row.get("id"),
            "first_name": row.get("first_name"),
            "last_name": row.get("last_name"),
            "email": row.get("email"),
            "name": row.get("name"),
            "status": row.get("status"),
            "disp_name": row.get("disp_name"),
            "prefix": row.get("prefix"),
            "title": row.get("title"),
            "display_title": row.get("display_title"),
            "phone": row.get("phone"),
            "dob_day": row.get("dob_day"),
            "dob_month": row.get("dob_month"),
            "dob_year": row.get("dob_year"),
            "gender": row.get("gender"),
            "ssn": row.get("ssn"),
            "address": row.get("address"),
            "opening_id": row.get("opening_id"),
            "stage_id": row.get("stage_id"),
            "stage_name": row.get("stage_name"),
            "last_time_stage": row.get("last_time_stage"),
            "source": row.get("source"),
            "campaign": row.get("campaign"),
            "since": parse_unix_ts(row.get("since")),
            "last_update": parse_unix_ts(row.get("last_update")),
            "metatype": row.get("metatype"),
            "assign_username": row.get("assign_username"),
            "interview_count": row.get("interview_count"),
            "last_interview": row.get("last_interview"),
            "last_stage_before_failed": row.get("last_stage_before_failed"),
            "reason": row.get("reason"),
            "time_apply": parse_unix_ts(row.get("time_apply")),
            "time_offered": parse_unix_ts(row.get("time_offered")),
            "time_hired": parse_unix_ts(row.get("time_hired")),
            "time_rejected": parse_unix_ts(row.get("time_rejected")),
            "time_campaign_qualified": parse_unix_ts(
                row.get("time_campaign_qualified")
            ),
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "first_name", "type": "STRING"},
        {"name": "last_name", "type": "STRING"},
        {"name": "email", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "status", "type": "STRING"},
        {"name": "disp_name", "type": "STRING"},
        {"name": "prefix", "type": "STRING"},
        {"name": "title", "type": "STRING"},
        {"name": "display_title", "type": "STRING"},
        {"name": "phone", "type": "STRING"},
        {"name": "dob_day", "type": "STRING"},
        {"name": "dob_month", "type": "STRING"},
        {"name": "dob_year", "type": "STRING"},
        {"name": "gender", "type": "STRING"},
        {"name": "ssn", "type": "STRING"},
        {"name": "address", "type": "STRING"},
        {"name": "opening_id", "type": "STRING"},
        {"name": "stage_id", "type": "STRING"},
        {"name": "stage_name", "type": "STRING"},
        {"name": "last_time_stage", "type": "STRING"},
        {"name": "source", "type": "STRING"},
        {"name": "campaign", "type": "STRING"},
        {"name": "since", "type": "TIMESTAMP"},
        {"name": "last_update", "type": "TIMESTAMP"},
        {"name": "metatype", "type": "STRING"},
        {"name": "assign_username", "type": "STRING"},
        {"name": "interview_count", "type": "INTEGER"},
        {"name": "last_interview", "type": "INTEGER"},
        {"name": "last_stage_before_failed", "type": "STRING"},
        {"name": "reason", "type": "STRING"},
        {"name": "time_apply", "type": "TIMESTAMP"},
        {"name": "time_offered", "type": "TIMESTAMP"},
        {"name": "time_hired", "type": "TIMESTAMP"},
        {"name": "time_rejected", "type": "TIMESTAMP"},
        {"name": "time_campaign_qualified", "type": "TIMESTAMP"},
    ],
)
