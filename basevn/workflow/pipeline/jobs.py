from basevn.interface import Resource
from basevn.utils import safe_string
from basevn.workflow.pipeline import workflows
from basevn.repo import WORKFLOW, get_multiple, get_single

pipeline = Resource(
    name="Workflow_Jobs",
    get=get_multiple(
        get_listing_fn=workflows.pipeline.get,
        get_one_fn=get_single(
            WORKFLOW,
            "jobs/get",
            lambda page: {"page_id": page},
            lambda res: res["jobs"],
        ),
        id_fn=lambda workflow: workflow["id"],
        body_fn=lambda id: {"workflow_id": id},
    ),
    transform=lambda rows: [
        {
            "id": row.get("id"),
            "type": row.get("type"),
            "status": row.get("status"),
            "state": row.get("state"),
            "owners": row.get("owners"),
            "followers": row.get("followers"),
            "since": row.get("since"),
            "last_update": row.get("last_update"),
            "finish_at": row.get("finish_at"),
            "stage_id": row.get("stage_id"),
            "stage_export": {
                "id": row["stage_export"]["id"],
                "name": row["stage_export"]["name"],
                "metatype": row["stage_export"]["metatype"],
                "workflow_id": row["stage_export"]["workflow_id"],
                "type": row["stage_export"]["type"],
            }
            if row.get("stage_export", {})
            else {},
            "user_id": safe_string(row.get("user_id")),
            "username": row.get("username"),
            "todos": [
                {
                    "id": todo.get("id"),
                    "name": todo.get("name"),
                    "status": todo.get("status"),
                    "stage_id": todo.get("stage_id"),
                    "deadline": todo.get("deadline"),
                    "username": todo.get("username"),
                    "type": todo.get("type"),
                    "link": todo.get("link"),
                }
                for todo in row["todos"]
            ]
            if row.get("todos", [])
            else [],
            "creator_id": row.get("creator_id"),
            "creator_username": row.get("creator_username"),
            "deadline": row.get("deadline"),
            "stage_deadline": row.get("stage_deadline"),
            "stage_start": row.get("stage_start"),
            "workflow_id": row.get("workflow_id"),
            "workflow_export": {
                "id": row["workflow_export"].get("id"),
                "name": row["workflow_export"].get("name"),
                "type": row["workflow_export"].get("type"),
            }
            if row.get("workflow_export", {})
            else {},
            "moves": [
                {
                    "id": move.get("id"),
                    "user_id": safe_string(move.get("user_id")),
                    "mover_id": move.get("mover_id"),
                    "job_id": move.get("job_id"),
                    "stage_id": move.get("stage_id"),
                    "stage_start": move.get("stage_start"),
                    "stage_deadline": move.get("stage_deadline"),
                    "from_stage_id": move.get("from_stage_id"),
                    "duration": move.get("duration"),
                    "past": move.get("past"),
                    "stage_end": move.get("stage_end"),
                }
                for move in row["moves"]
            ]
            if row.get("moves", [])
            else [],
            "form": [
                {
                    "id": form.get("id"),
                    "name": form.get("name"),
                    "type": form.get("type"),
                    "placeholder": form.get("placeholder"),
                    "enabled": form.get("enabled"),
                    "required": form.get("required"),
                    "options": form.get("options"),
                    "stage_id": form.get("stage_id"),
                    "value": form.get("value"),
                    "display": form.get("display"),
                }
                for form in row["form"]
            ]
            if row.get("form", [])
            else [],
            "on_failed": {
                "stage_id": row["on_failed"].get("stage_id"),
                "failed_reason_id": row["on_failed"].get("failed_reason_id"),
                "failed_name": row["on_failed"].get("failed_name"),
                "note": row["on_failed"].get("note"),
                "since": row["on_failed"].get("since"),
            }
            if row.get("on_failed", {})
            else {},
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "type", "type": "STRING"},
        {"name": "status", "type": "STRING"},
        {"name": "state", "type": "STRING"},
        {"name": "owners", "type": "STRING", "mode": "repeated"},
        {"name": "followers", "type": "STRING", "mode": "repeated"},
        {"name": "since", "type": "STRING"},
        {"name": "last_update", "type": "STRING"},
        {"name": "finish_at", "type": "STRING"},
        {"name": "stage_id", "type": "STRING"},
        {
            "name": "stage_export",
            "type": "record",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "metatype", "type": "STRING"},
                {"name": "workflow_id", "type": "STRING"},
                {"name": "type", "type": "STRING"},
            ],
        },
        {"name": "user_id", "type": "STRING"},
        {"name": "username", "type": "STRING"},
        {
            "name": "todos",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "status", "type": "STRING"},
                {"name": "stage_id", "type": "STRING"},
                {"name": "deadline", "type": "STRING"},
                {"name": "username", "type": "STRING"},
                {"name": "type", "type": "STRING"},
                {"name": "link", "type": "STRING"},
            ],
        },
        {"name": "creator_id", "type": "STRING"},
        {"name": "creator_username", "type": "STRING"},
        {"name": "deadline", "type": "STRING"},
        {"name": "stage_deadline", "type": "STRING"},
        {"name": "stage_start", "type": "STRING"},
        {"name": "workflow_id", "type": "STRING"},
        {
            "name": "workflow_export",
            "type": "record",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "type", "type": "STRING"},
            ],
        },
        {
            "name": "moves",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "user_id", "type": "STRING"},
                {"name": "mover_id", "type": "STRING"},
                {"name": "job_id", "type": "STRING"},
                {"name": "stage_id", "type": "STRING"},
                {"name": "stage_start", "type": "TIMESTAMP"},
                {"name": "stage_deadline", "type": "TIMESTAMP"},
                {"name": "from_stage_id", "type": "STRING"},
                {"name": "duration", "type": "INTEGER"},
                {"name": "past", "type": "INTEGER"},
                {"name": "stage_end", "type": "TIMESTAMP"},
            ],
        },
        {
            "name": "form",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "type", "type": "STRING"},
                {"name": "placeholder", "type": "STRING"},
                {"name": "enabled", "type": "INTEGER"},
                {"name": "required", "type": "INTEGER"},
                {"name": "options", "type": "STRING", "mode": "repeated"},
                {"name": "stage_id", "type": "STRING"},
                {"name": "value", "type": "STRING"},
                {"name": "display", "type": "STRING"},
            ],
        },
        {
            "name": "on_failed",
            "type": "record",
            "fields": [
                {"name": "stage_id", "type": "STRING"},
                {"name": "failed_reason_id", "type": "STRING"},
                {"name": "failed_name", "type": "STRING"},
                {"name": "note", "type": "STRING"},
                {"name": "since", "type": "TIMESTAMP"},
            ],
        },
    ],
)
