import os

import requests

BASE_URL = "https://workflow.base.vn/extapi/v1/"

DATE_FORMAT = "%d/%m/%Y"


def get_workflows(session: requests.Session, page: int = 0) -> list[dict]:
    with session.post(
        f"{BASE_URL}/workflows/get",
        data={
            "access_token": os.getenv("WORKFLOW_TOKEN"),
            "page": page,
        },
    ) as r:
        res = r.json()
    data = res["workflows"]
    return data + get_workflows(session, page + 1) if data else []


def get_jobs_by_workflow(
    session: requests.Session,
    id: str,
    page: int = 0,
) -> list[dict]:
    with session.post(
        f"{BASE_URL}/jobs/get",
        data={
            "access_token": os.getenv("WORKFLOW_TOKEN"),
            "workflow_id": id,
            "page_id": page,
        },
    ) as r:
        res = r.json()
    data = res["jobs"]
    return data + get_jobs_by_workflow(session, id, page + 1) if data else []


def get_jobs(session: requests.Session):
    return [
        i
        for j in [
            get_jobs_by_workflow(session, workflow["id"])
            for workflow in get_workflows(session)
        ]
        for i in j
    ]
