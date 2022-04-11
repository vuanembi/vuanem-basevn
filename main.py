from typing import Any

from basevn.basevn_controller import basevn_controller
from tasks.tasks_service import tasks_service


def main(request) -> dict[str, Any]:
    data = request.get_json()
    print(data)

    if "tasks" in data:
        fn = tasks_service
    elif "table" in data:
        fn = basevn_controller # type: ignore
    else:
        raise ValueError(data)

    response = fn(data)
    print(response)
    return response
