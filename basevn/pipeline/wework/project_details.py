from basevn.pipeline.interface import Resource
from basevn.utils import safe_string
from basevn.repo import WEWORK, get_multiple, get_single

pipeline = Resource(
    name="Wework_ProjectDetails",
    get=get_multiple(
        get_listing_fn=get_single(
            WEWORK,
            "project/list",
            lambda res: res["projects"] if "projects" in res else [],
            lambda page: {"page": page},
        ),
        get_one_fn=get_single(
            WEWORK,
            "project/get.full",
            res_fn=lambda x: [x],
        ),
        id_fn=lambda project: project["id"],
        body_fn=lambda id: {"id": id},
        res_fn=lambda project_details: [
            {
                "project": project["project"],
                "tasklists": project["tasklists"],
                "tasks": project["tasks"],
                "subtasks": project["subtasks"],
                "milestones": project["milestones"],
            }
            for project in project_details
        ],
    ),
    transform=lambda rows: [
        {
            "project": {
                "id": row["project"].get("id"),
                "name": row["project"].get("name"),
                "owners": [
                    {
                        "username": owner.get("username"),
                    }
                    for owner in row["project"]["owners"]
                ]
                if row["project"].get("owners", [])
                else [],
                "followers": [
                    {
                        "username": follower.get("username"),
                    }
                    for follower in row["project"]["followers"]
                ]
                if row["project"].get("followers", [])
                else [],
                "stime": safe_string(row["project"].get("stime")),
                "etime": safe_string(row["project"].get("etime")),
                "since": row["project"].get("since"),
                "last_update": row["project"].get("last_update"),
                "status": row["project"].get("status"),
                "status_obj": {
                    "stage": row["project"]["status_obj"].get("stage"),
                    "status": row["project"]["status_obj"].get("status"),
                    "color": row["project"]["status_obj"].get("color"),
                    "note": row["project"]["status_obj"].get("note"),
                }
                if row["project"].get("status_obj", {})
                else {},
                "stats": {
                    "total": row["project"]["stats"].get("total"),
                    "complete": row["project"]["stats"].get("complete"),
                    "active": row["project"]["stats"].get("active"),
                    "overdue": row["project"]["stats"].get("overdue"),
                }
                if row["project"].get("stats", {})
                else {},
            }
            if row.get("project", {})
            else {},
            "tasklists": [
                {
                    "id": tasklist.get("id"),
                    "name": tasklist.get("name"),
                    "complete": tasklist.get("complete"),
                    "percent": tasklist.get("percent"),
                    "stats": {
                        "total": tasklist["stats"].get("total"),
                        "total_display": tasklist["stats"].get("total_display"),
                        "done": tasklist["stats"].get("done"),
                        "failed": tasklist["stats"].get("failed"),
                        "active": tasklist["stats"].get("active"),
                    }
                    if tasklist.get("stats", {})
                    else {},
                    "order": tasklist.get("order"),
                    "since": tasklist.get("since"),
                    "has_deadline": tasklist.get("has_deadline"),
                    "deadline": tasklist.get("deadline"),
                    "stime": safe_string(tasklist.get("stime")),
                    "etime": safe_string(tasklist.get("etime")),
                }
                for tasklist in row["tasklists"]
            ]
            if row.get("tasklists", [])
            else [],
            "tasks": [
                {
                    "id": task.get("id"),
                    "name": task.get("name"),
                    "user_id": task.get("user_id"),
                    "username": task.get("username"),
                    "creator_id": task.get("creator_id"),
                    "creator_username": task.get("creator_username"),
                    "has_deadline": task.get("has_deadline"),
                    "deadline": task.get("deadline"),
                    "deadline_has_time": task.get("deadline_has_time"),
                    "start_time": task.get("start_time"),
                    "stime": safe_string(task.get("stime")),
                    "etime": safe_string(task.get("etime")),
                    "overdue": task.get("overdue"),
                    "urgent": task.get("urgent"),
                    "important": task.get("important"),
                    "started": task.get("started"),
                    "completed_time": task.get("completed_time"),
                    "starred": task.get("starred"),
                    "complete": task.get("complete"),
                    "score": task.get("score"),
                    "tags": task.get("tags"),
                    "status": task.get("status"),
                    "review": task.get("review"),
                    "owners": [
                        {
                            "username": owner.get("username"),
                        }
                        for owner in task["owners"]
                    ]
                    if task.get("owners", [])
                    else [],
                    "followers": [
                        {
                            "username": follower.get("username"),
                        }
                        for follower in task["followers"]
                    ]
                    if task.get("followers", [])
                    else [],
                    "since": task.get("since"),
                    "last_update": task.get("last_update"),
                    "tasklist_id": task.get("tasklist_id"),
                    "project_id": task.get("project_id"),
                    "milestone_id": task.get("milestone_id"),
                    "real_order": task.get("real_order"),
                }
                for task in row["tasks"]
            ]
            if row.get("tasks", [])
            else [],
            "milestones":[
                {
                    "id": milestones.get("id"),
                    "user_id": milestones.get("user_id"),
                    "username": milestones.get("username"),
                    "creator_id": milestones.get("creator_id"),
                    "name": milestones.get("name"),
                    "content": milestones.get("content"),
                    "time": milestones.get("time"),
                    "color": milestones.get("color"),
                    "dept_id": milestones.get("dept_id"),
                    "project_id": milestones.get("project_id"),
                    "since": milestones.get("since"),
                    "system_id": milestones.get("system_id"),
                    "done": milestones.get("done"),
                    "total": milestones.get("total"),
                    "complete": milestones.get("complete"),
                }
                for milestones in row["milestones"]
            ]
            if row.get("milestones", [])
            else [],
        }
        for row in rows
    ],
    schema=[
        {
            "name": "project",
            "type": "record",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {
                    "name": "owners",
                    "type": "record",
                    "mode": "repeated",
                    "fields": [{"name": "username", "type": "STRING"}],
                },
                {
                    "name": "followers",
                    "type": "record",
                    "mode": "repeated",
                    "fields": [{"name": "username", "type": "STRING"}],
                },
                {"name": "stime", "type": "STRING"},
                {"name": "etime", "type": "STRING"},
                {"name": "since", "type": "STRING"},
                {"name": "last_update", "type": "STRING"},
                {"name": "status", "type": "STRING"},
                {
                    "name": "status_obj",
                    "type": "record",
                    "fields": [
                        {"name": "stage", "type": "STRING"},
                        {"name": "status", "type": "STRING"},
                        {"name": "color", "type": "STRING"},
                        {"name": "note", "type": "STRING"},
                    ],
                },
                {
                    "name": "stats",
                    "type": "record",
                    "fields": [
                        {"name": "total", "type": "INTEGER"},
                        {"name": "complete", "type": "INTEGER"},
                        {"name": "active", "type": "INTEGER"},
                        {"name": "overdue", "type": "INTEGER"},
                    ],
                },
            ],
        },
        {
            "name": "tasklists",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "complete", "type": "INTEGER"},
                {"name": "percent", "type": "INTEGER"},
                {
                    "name": "stats",
                    "type": "record",
                    "fields": [
                        {"name": "total", "type": "INTEGER"},
                        {"name": "total_display", "type": "INTEGER"},
                        {"name": "done", "type": "INTEGER"},
                        {"name": "failed", "type": "INTEGER"},
                        {"name": "active", "type": "INTEGER"},
                    ],
                },
                {"name": "order", "type": "INTEGER"},
                {"name": "since", "type": "STRING"},
                {"name": "has_deadline", "type": "STRING"},
                {"name": "deadline", "type": "STRING"},
                {"name": "stime", "type": "STRING"},
                {"name": "etime", "type": "INTEGER"},
            ],
        },
        {
            "name": "tasks",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "user_id", "type": "STRING"},
                {"name": "username", "type": "STRING"},
                {"name": "creator_id", "type": "STRING"},
                {"name": "creator_username", "type": "STRING"},
                {"name": "has_deadline", "type": "STRING"},
                {"name": "deadline", "type": "STRING"},
                {"name": "deadline_has_time", "type": "INTEGER"},
                {"name": "start_time", "type": "STRING"},
                {"name": "stime", "type": "STRING"},
                {"name": "etime", "type": "STRING"},
                {"name": "overdue", "type": "INTEGER"},
                {"name": "urgent", "type": "STRING"},
                {"name": "important", "type": "STRING"},
                {"name": "started", "type": "INTEGER"},
                {"name": "completed_time", "type": "INTEGER"},
                {"name": "starred", "type": "STRING"},
                {"name": "complete", "type": "STRING"},
                {"name": "score", "type": "INTEGER"},
                {"name": "tags", "type": "STRING", "mode": "repeated"},
                {"name": "status", "type": "STRING"},
                {"name": "review", "type": "STRING"},
                {
                    "name": "owners",
                    "type": "record",
                    "mode": "repeated",
                    "fields": [{"name": "username", "type": "STRING"}],
                },
                {
                    "name": "followers",
                    "type": "record",
                    "mode": "repeated",
                    "fields": [{"name": "username", "type": "STRING"}],
                },
                {"name": "since", "type": "STRING"},
                {"name": "last_update", "type": "STRING"},
                {"name": "tasklist_id", "type": "STRING"},
                {"name": "project_id", "type": "STRING"},
                {"name": "milestone_id", "type": "STRING"},
                {"name": "real_order", "type": "STRING"},
            ],
        },
        {
            "name": "milestones",
            "type": "record",
            "mode": "repeated",
            "fields": [
                {"name": "id", "type": "STRING"},
                {"name": "user_id", "type": "STRING"},
                {"name": "username", "type": "STRING"},
                {"name": "creator_id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "content", "type": "STRING"},
                {"name": "time", "type": "STRING"},
                {"name": "color", "type": "STRING"},
                {"name": "dept_id", "type": "STRING"},
                {"name": "project_id", "type": "STRING"},
                {"name": "since", "type": "STRING"},
                {"name": "system_id", "type": "STRING"},
                {"name": "done", "type": "INTEGER"},
                {"name": "total", "type": "INTEGER"},
                {"name": "complete", "type": "INTEGER"}
            ]
        },
    ],
)
