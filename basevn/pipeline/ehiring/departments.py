from basevn.pipeline.interface import Resource
from basevn.repo import EHIRING, get_single

pipeline = Resource(
    name="EHiring_Departments",
    get=get_single(
        EHIRING,
        "system/depts",
        lambda res: res["depts"] if "depts" in res else [],
    ),
    transform=lambda rows: [
        {
            "id": row.get("id"),
            "name": row.get("name"),
            "content": row.get("content"),
            "image": row.get("image"),
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "content", "type": "STRING"},
        {"name": "image", "type": "STRING"},
    ],
)
