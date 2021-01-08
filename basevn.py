import aiohttp
import asyncio
import requests
from datetime import datetime
import time
import os
from tqdm.asyncio import tqdm, trange
from google.cloud import bigquery
import json
import itertools

token = os.environ.get('WORKFLOW_TOKEN')
client = bigquery.Client()


def transform_json_type(result):
    for item in result:
        for key, value in item.items():
            try:
                item[key] = json.loads(value)
            except:
                pass
            if type(item[key]) == list:
                for i in item[key]:
                    if type(i) == dict:
                        for key2, value2 in i.items():
                            try:
                                i[key2] = json.loads(value2)
                            except:
                                pass
            elif type(item[key]) == dict:
                for key2, value2 in item[key].items():
                    try:
                        item[key][key2] = json.loads(value2)
                    except:
                        pass
    return result


def get_workflows():
    url = 'https://workflow.base.vn/extapi/v1/workflows/get'
    payload = {
        'access_token': token
    }
    with requests.post(url, data=payload) as r:
        result = r.json()
    get_workflow_stages_dim(result)
    return [i.get('id') for i in result.get('workflows')]


def get_workflow_stages_dim(result):
    stages = [i.get('stages') for i in result.get('workflows')]
    stages = list(itertools.chain(*stages))
    stages = transform_json_type(stages)
    errors = client.insert_rows_json(
        'Basevn.dim_workflow_stages',
        stages
    )
    return errors


def transform_forms_dates(job):
    forms = job.get('form')
    for form in forms:
        if form.get('type') == 'date':
            form['value'] = datetime.strftime(datetime.strptime(
                form.get('value'), '%d/%m/%Y'), '%m/%d/%Y')
    return job


async def get_workflow_jobs(ids):
    url = 'https://workflow.base.vn/extapi/v1/workflow/jobs'
    async with aiohttp.ClientSession() as session:
        for id in tqdm(ids):
            jobs_done = False
            page_id = 0
            while jobs_done == False:
                payload = {
                    'access_token': token,
                    'id': id,
                    'page_id': page_id,
                    'limit': 500
                }
                async with session.post(url, data=payload) as r:
                    results = await r.json()
                    jobs = results.get('jobs')
                if len(jobs) > 0:
                    jobs = transform_json_type(jobs)
                    jobs = [transform_forms_dates(job) for job in jobs]
                    errors = client.insert_rows_json(
                        'Basevn.workflow',
                        jobs,
                        ignore_unknown_values=True
                    )
                    page_id = page_id + 1
                elif len(jobs) == 0:
                    jobs_done = True


def truncate_table():
    tables = ['Basevn.workflow', 'Basevn.dim_workflow_stages']
    for i in tables:
        client.query(f'''
                     TRUNCATE TABLE `voltaic-country-280607.{i}`
                     ''')


def send_telegram(text):
    url = f'https://api.telegram.org/bot1259711927:AAHwBvjQfAVPH04z_OSXS4eDAs1GdvPiRcM/sendMessage'
    payload = {
        'chat_id': '-465061044',
        'text': text
    }
    return requests.post(url=url, data=payload)


async def run():
    send_telegram('basevn >>>')
    truncate_table()
    for i in trange(125):
        time.sleep(1)
    send_telegram('basevn done sleep')
    await get_workflow_jobs(get_workflows())
    send_telegram('basevn done')


def main(request):
    asyncio.run(run())
    return 'ok'