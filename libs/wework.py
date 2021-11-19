import os

import requests

BASE_URL = "https://wework.base.vn/extapi/v3/"


def get_projects(session: requests.Session, page: int = 0) -> list[dict]:
    with session.post(
        f"{BASE_URL}/project/list",
        data={
            "access_token": os.getenv("WEWORK_TOKEN"),
            "page": page,
        },
    ) as r:
        res = r.json()
    data = res["projects"]
    return data + get_projects(session, page + 1) if data else []


def get_project_details(session: requests.Session, id: str) -> dict:
    with session.post(
        f"{BASE_URL}/project/get.full",
        data={
            "access_token": os.getenv("WEWORK_TOKEN"),
            "id": id,
        },
    ) as r:
        return r.json()


def get_projects_details(session: requests.Session):
    project_details = [
        get_project_details(session, project["id"]) for project in get_projects(session)
    ]
    return [
        {
            "project": project["project"],
            "tasklists": project["tasklists"],
            "tasks": project["tasks"],
            "subtasks": project["subtasks"],
            "milestones": project["milestones"],
        }
        for project in project_details
    ]
