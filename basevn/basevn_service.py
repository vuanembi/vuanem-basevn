from typing import Union

import requests
from compose import compose

from db.bigquery import load
from basevn.interface import Resource
from basevn.workflow.pipeline import workflows, jobs
from basevn.wework.pipeline import project_details

Response = dict[str, Union[str, int]]

pipelines = {
    i.name: i
    for i in [
        workflows.pipeline,
        jobs.pipeline,
        project_details.pipeline,
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