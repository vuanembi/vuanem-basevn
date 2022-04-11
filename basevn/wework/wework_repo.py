import os

import requests

BASE_URL = "https://wework.base.vn/extapi/v3/"
TOKEN = os.getenv("WEWORK_TOKEN")


def get_projects(session: requests.Session):
    def _get(page: int = 0) -> list[dict]:
        with session.post(
            f"{BASE_URL}/project/list",
            data={
                "access_token": TOKEN,
                "page": page,
            },
        ) as r:
            res = r.json()
        data = res["projects"]
        return data + _get(page + 1) if data else []

    return _get


def get_projects_details(session: requests.Session):
    def _get():
        def _get_project_details(id: str) -> dict:
            with session.post(
                f"{BASE_URL}/project/get.full",
                data={
                    "access_token": TOKEN,
                    "id": id,
                },
            ) as r:
                return r.json()

        project_details = [
            _get_project_details(project["id"]) for project in get_projects(session)()
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

    return _get
