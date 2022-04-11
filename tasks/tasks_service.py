from basevn import basevn_service
from tasks import cloud_tasks


def tasks_service(*args) -> dict[str, int]:
    return {
        "tasks": cloud_tasks.create_tasks(
            [{"table": table} for table in basevn_service.pipelines.keys()],
            lambda x: x["table"],
        )
    }
