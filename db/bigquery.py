from typing import Any

from google.cloud import bigquery

DATASET = "IP_Basevn"

client = bigquery.Client()


def load(table: str, schema=list[dict[str, Any]]):
    def _load(rows: list[dict[str, Any]]) -> int:
        return (
            client.load_table_from_json(
                rows,
                f"{DATASET}.{table}",
                job_config=bigquery.LoadJobConfig(
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_TRUNCATE",
                    schema=schema,
                ),
            )
            .result()
            .output_rows
        )

    return _load
