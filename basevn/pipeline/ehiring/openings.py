from basevn.pipeline.interface import Resource
from basevn.utils import parse_unix_ts
from basevn.repo import EHIRING, get_single

pipeline = Resource(
    name="EHiring_Openings",
    get=get_single(
        EHIRING,
        "opening/list",
        lambda res: res["openings"] if "openings" in res else [],
        lambda page: {"page": page},
    ),
    transform=lambda rows: [
        {
            "id": row.get("id"),
            "name": row.get("name"),
            "codename": row.get("codename"),
            "starred": row.get("starred"),
            "dept_id": row.get("dept_id"),
            "salary": row.get("salary"),
            "period": row.get("period"),
            "status": row.get("status"),
            "metatype": row.get("metatype"),
            "num_positions": row.get("num_positions"),
            "company_name": row.get("company_name"),
            "office_name": row.get("office_name"),
            "offices": [i for i in row["offices"]] if row.get("offices") else [],
            "deadline": row.get("deadline"),
            "stime": parse_unix_ts(row.get("stime")),
            "etime": parse_unix_ts(row.get("etime")),
            "talent_pool_id": row.get("talent_pool_id"),
            "since": parse_unix_ts(row.get("since")),
            "last_update": parse_unix_ts(row.get("last_update")),
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "codename", "type": "STRING"},
        {"name": "starred", "type": "STRING"},
        {"name": "dept_id", "type": "STRING"},
        {"name": "salary", "type": "STRING"},
        {"name": "period", "type": "STRING"},
        {"name": "status", "type": "STRING"},
        {"name": "metatype", "type": "STRING"},
        {"name": "num_positions", "type": "STRING"},
        {"name": "company_name", "type": "STRING"},
        {"name": "office_name", "type": "STRING"},
        {"name": "offices", "type": "STRING", "mode": "repeated"},
        {"name": "deadline", "type": "STRING"},
        {"name": "stime", "type": "TIMESTAMP"},
        {"name": "etime", "type": "TIMESTAMP"},
        {"name": "talent_pool_id", "type": "STRING"},
        {"name": "since", "type": "TIMESTAMP"},
        {"name": "last_update", "type": "TIMESTAMP"},
    ],
)
