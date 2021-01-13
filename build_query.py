import json
from google.cloud import bigquery
import os


def transform_date(field):
    return f'IF(UNIX_SECONDS({field}) = 0, NULL, {field}) AS {field}, '


def build_latest_queries(
    fields,
    timestamp_fields,
    other_fields,
    table_id
    ):
    fields_list = ', '.join(fields)
    timestamp_fields_list = ', '.join(timestamp_fields)
    timestamp_fields = '\n '.join([transform_date(field) for field in timestamp_fields])
    other_fields_list = ', '.join(other_fields)
    template = f'''
    WITH cte AS (
        SELECT
            {fields_list},
            ROW_NUMBER() OVER (
                PARTITION BY id
                ORDER BY
                    _batched_at DESC
            ) AS row_number
        FROM
            `voltaic-country-280607.Basevn.{table_id}`
    )
    SELECT
        {other_fields_list},
        {timestamp_fields}
    FROM
        cte
    WHERE
        cte.row_number = 1
    '''
    with open(f'sql2/{table_id}.sql', 'w') as f:
        f.write(template)


for i in os.listdir('schema/'):
    with open('schema/' + i, 'rb') as f:
        schema = json.load(f)
        fields = [field.get('name') for field in schema]
        other_fields = [field.get('name') for field in schema if field.get('type') != 'TIMESTAMP']
        timestamp_fields = [
            field.get('name') for field in schema if field.get('type') == 'TIMESTAMP']
        build_latest_queries(
            fields=fields,
            timestamp_fields=timestamp_fields,
            other_fields=other_fields,
            table_id=i.split('.')[0])
