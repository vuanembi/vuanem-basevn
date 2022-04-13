from basevn.pipeline.interface import Resource
from basevn.utils import safe_string
from basevn.repo import WORKFLOW, get_single

pipeline = Resource(
    name="Workflow_Workflows",
    get=get_single(
        WORKFLOW,
        "workflows/get",
        lambda res: res["workflows"] if 'workflows' in res else [],
        lambda page: {"page_id": page},
    ),
    transform=lambda rows: [
        {
            "id": row.get("id"),
            "name": row.get("name"),
            "owners": row.get("owners"),
            "followers": row.get("followers"),
            "viewable_teams": row.get("viewable_teams"),
            "creatable_teams": row.get("creatable_teams"),
            "stages": [
                {
                    "id": stage.get("id"),
                    "name": stage.get("name"),
                    "metatype": stage.get("metatype"),
                    "owners": stage.get("owners"),
                    "followers": stage.get("followers"),
                }
                for stage in row["stages"]
            ]
            if row.get("stages", [])
            else [],
            "failed_reasons": [
                {
                    "key": failed_reason.get("key"),
                    "value": failed_reason.get("value"),
                }
                for failed_reason in row["failed_reasons"]
            ]
            if row.get("failed_reasons", [])
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
                    "stage_id": safe_string(form.get("stage_id")),
                }
                for form in row["form"]
            ]
            if row.get("form", [])
            else [],
            "stats": {
                "done": row["stats"].get("done"),
                "failed": row["stats"].get("failed"),
                "active": row["stats"].get("active"),
            }
            if row.get("stats", {})
            else {},
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "owners", "type": "STRING", "mode": "repeated"},
        {"name": "followers", "type": "STRING", "mode": "repeated"},
        {"name": "viewable_teams", "type": "STRING", "mode": "repeated"},
        {"name": "creatable_teams", "type": "STRING", "mode": "repeated"},
        {
            "name": "stages",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "metatype", "type": "STRING"},
                {"name": "owners", "type": "STRING", "mode": "repeated"},
                {"name": "followers", "type": "STRING", "mode": "repeated"},
            ],
        },
        {
            "name": "failed_reasons",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "key", "type": "STRING"},
                {"name": "value", "type": "STRING"},
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
            ],
        },
        {
            "name": "stats",
            "type": "record",
            "fields": [
                {"name": "done", "type": "INTEGER"},
                {"name": "failed", "type": "INTEGER"},
                {"name": "active", "type": "INTEGER"},
            ],
        },
    ],
)
