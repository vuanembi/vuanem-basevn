import os

import requests

BASE_URL = "https://workflow.base.vn/extapi/v1/"
TOKEN = os.getenv("WORKFLOW_TOKEN")
DATE_FORMAT = "%d/%m/%Y"


def get_workflows(session: requests.Session):
    def _get(page: int = 0) -> list[dict]:
        with session.post(
            f"{BASE_URL}/workflows/get",
            data={
                "access_token": TOKEN,
                "page_id": page,
            },
        ) as r:
            res = r.json()
        data = res["workflows"]
        return data + _get(page + 1) if data else []

    return _get


def get_jobs(session: requests.Session):
    def _get():
        def _get_jobs_by_workflow(id: str, page: int = 0) -> list[dict]:
            with session.post(
                f"{BASE_URL}/jobs/get",
                data={
                    "access_token": TOKEN,
                    "workflow_id": id,
                    "page_id": page,
                },
            ) as r:
                res = r.json()
            data = res["jobs"]
            return data + _get_jobs_by_workflow(id, page + 1) if data else []

        return [
            i
            for j in [
                _get_jobs_by_workflow(workflow["id"])
                for workflow in get_workflows(session)()
            ]
            for i in j
        ]

    return _get
