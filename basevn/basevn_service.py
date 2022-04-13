from typing import Union

import requests
from compose import compose

from db.bigquery import load
from basevn.pipeline.interface import Resource
from basevn.pipeline.workflow import workflows, jobs
from basevn.pipeline.wework import project_details
from basevn.pipeline.account import users
from basevn.pipeline.ehiring import openings

Response = dict[str, Union[str, int]]

pipelines = {
    i.name: i
    for i in [
        workflows.pipeline,
        jobs.pipeline,
        project_details.pipeline,
        users.pipeline,
        openings.pipeline,
    ]
}


def pipeline_service(resource: Resource) -> dict[str, Union[str, int]]:
    with requests.Session() as session:
        return compose(
            lambda x: {
                "table": resource.name,
                "num_processed": x,
            },
            load(resource.name, resource.schema),
            resource.transform,
            resource.get(session),
        )()
