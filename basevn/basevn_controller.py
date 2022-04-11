from typing import Any

from basevn.basevn_service import Response, pipelines, pipeline_service


def basevn_controller(body: dict[str, Any]) -> Response:
    return pipeline_service(pipelines[body["table"]])
