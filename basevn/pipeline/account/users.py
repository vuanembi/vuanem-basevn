from basevn.pipeline.interface import Resource
from basevn.repo import ACCOUNT, get_single

pipeline = Resource(
    name="Account_Users",
    get=get_single(
        ACCOUNT,
        "users",
        lambda res: res["users"],
    ),
    transform=lambda rows: [
        {
            "id": row.get("id"),
            "uid": row.get("uid"),
            "hid": row.get("hid"),
            "token": row.get("token"),
            "metatype": row.get("metatype"),
            "first_name": row.get("first_name"),
            "last_name": row.get("last_name"),
            "name": row.get("name"),
            "email": row.get("email"),
            "username": row.get("username"),
            "manager": [i for i in row["manager"]] if row.get("manager") else [],
            "title": row.get("title"),
            "phone": row.get("phone"),
            "address": row.get("address"),
            "role": row.get("role"),
            "status": row.get("status"),
            "since": row.get("since"),
            "keywords": row.get("keywords"),
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "uid", "type": "STRING"},
        {"name": "hid", "type": "STRING"},
        {"name": "token", "type": "STRING"},
        {"name": "metatype", "type": "STRING"},
        {"name": "first_name", "type": "STRING"},
        {"name": "last_name", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "email", "type": "STRING"},
        {"name": "username", "type": "STRING"},
        {"name": "manager", "type": "STRING", "mode": "repeated"},
        {"name": "title", "type": "STRING"},
        {"name": "phone", "type": "STRING"},
        {"name": "address", "type": "STRING"},
        {"name": "role", "type": "STRING"},
        {"name": "status", "type": "STRING"},
        {"name": "since", "type": "STRING"},
        {"name": "keywords", "type": "STRING"},
    ],
)
