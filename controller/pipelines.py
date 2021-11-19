import importlib

import requests
from google.cloud import bigquery

from libs.bigquery import load
from models.base import Basevn


def factory(resource: str, table: str) -> Basevn:
    try:
        module = importlib.import_module(f"models.{resource}.{table}")
        return getattr(module, table)
    except (ImportError, AttributeError):
        raise ValueError(table)


def run(
    session: requests.Session,
    client: bigquery.Client,
    dataset: str,
    model: Basevn,
) -> dict:
    data = model["get"](session)
    response = {
        "table": model["name"],
        "num_processed": len(data),
    }
    if len(data) > 0:
        response["output_rows"] = load(client, dataset, model, data)
    return response
