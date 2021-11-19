from google.cloud import bigquery

from models.base import Basevn


def load(client: bigquery.Client, dataset: str, model: Basevn, rows: list[dict]) -> int:
    return (
        client.load_table_from_json(
            rows,
            f"{dataset}.{model['name']}",
            job_config=bigquery.LoadJobConfig(
                create_disposition="CREATE_IF_NEEDED",
                write_disposition="WRITE_TRUNCATE",
                schema=model["schema"],
            ),
        )
        .result()
        .output_rows
    )
