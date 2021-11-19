import os
import json

import requests
from google.cloud import bigquery

from controller.pipelines import factory, run

BQ_CLIENT = bigquery.Client()
SESSION = requests.Session()
DATASET = "IP_Basevn"


def main(request) -> dict:
    data = request.get_json()
    print(data)

    if "table" in data:
        response = {
            "pipelines": "Basevn",
            "results": run(
                SESSION,
                BQ_CLIENT,
                DATASET,
                factory(data["resouce"], data["table"]),
            ),
        }
        print(response)
        SESSION.post(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
            json={
                "chat_id": "-465061044",
                "text": json.dumps(response, indent=4),
            },
        )
        return response
    else:
        raise ValueError(data)
