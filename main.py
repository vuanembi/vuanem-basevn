import requests
from google.cloud import bigquery

from controller.pipelines import factory, run
from controller.tasks import create_tasks

BQ_CLIENT = bigquery.Client()
SESSION = requests.Session()
DATASET = "IP_Basevn"


def main(request) -> dict:
    data = request.get_json()
    print(data)

    if "tasks" in data:
        response = create_tasks()
    elif "table" in data:
        response = {
            "pipelines": "Basevn",
            "results": run(
                SESSION,
                BQ_CLIENT,
                DATASET,
                factory(data["resource"], data["table"]),
            ),
        }
    else:
        raise ValueError(data)
    print(response)
    return response
