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


def send_telegram(text):
    token = os.environ.get('TELEGRAM_TOKEN')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': '-465061044',
        'text': text
    }
    return requests.post(url=url, data=payload)


class Basevn:
    client = bigquery.Client()
    now = int(datetime.now().timestamp())

    def __init__(self):
        return None

    def transform_json_type(self, result):
        for key, value in result.items():
            try:
                result[key] = json.loads(value)
            except:
                pass
            if type(result[key]) == list:
                for i in result[key]:
                    if type(i) == dict:
                        for key2, value2 in i.items():
                            try:
                                i[key2] = json.loads(value2)
                            except:
                                pass
            elif type(result[key]) == dict:
                for key2, value2 in result[key].items():
                    try:
                        result[key][key2] = json.loads(value2)
                    except:
                        pass
        return result

    def transform_forms_dates(self, job):
        forms = job.get('form')
        for form in forms:
            if form.get('type') == 'date':
                form['value'] = datetime.strftime(datetime.strptime(
                    form.get('value'), '%d/%m/%Y'), '%m/%d/%Y')
        return job

    def add_batched_at(self, result):
        result['_batched_at'] = self.now
        return result


class Workflow(Basevn):
    def __init__(self):
        self.token = os.environ.get('WORKFLOW_TOKEN')

    def get_workflows(self):
        url = 'https://workflow.base.vn/extapi/v1/workflows/get'
        payload = {
            'access_token': self.token
        }
        with requests.post(url, data=payload) as r:
            result = r.json()
        self.get_workflow_stages_dim(result)
        return [i.get('id') for i in result.get('workflows')]

    def get_workflow_stages_dim(self, result):
        stages = [i.get('stages') for i in result.get('workflows')]
        stages = list(itertools.chain(*stages))
        stages = [self.transform_json_type(stage) for stage in stages]
        stages = [self.add_batched_at(stage) for stage in stages]
        errors_workflow_stages = self.client.insert_rows_json(
            'Basevn.dim_workflow_stages',
            stages
        )
        return errors_workflow_stages

    async def get_workflow_jobs(self, ids):
        url = 'https://workflow.base.vn/extapi/v1/workflow/jobs'
        async with aiohttp.ClientSession() as session:
            for id in ids:
                jobs_done = False
                page_id = 0
                while jobs_done == False:
                    payload = {
                        'access_token': self.token,
                        'id': id,
                        'page_id': page_id,
                        'limit': 500
                    }
                    async with session.post(url, data=payload) as r:
                        results = await r.json()
                        jobs = results.get('jobs')
                    if len(jobs) > 0:
                        jobs = [self.transform_json_type(job) for job in jobs]
                        jobs = [self.transform_forms_dates(
                            job) for job in jobs]
                        jobs = [self.add_batched_at(job) for job in jobs]
                        errors = self.client.insert_rows_json(
                            'Basevn.workflow',
                            jobs,
                            ignore_unknown_values=True
                        )
                        page_id = page_id + 1
                    elif len(jobs) == 0:
                        jobs_done = True

    async def run(self):
        await self.get_workflow_jobs(self.get_workflows())
        send_telegram('Workflow Done')


class WeWork(Basevn):
    def __init__(self):
        self.token = os.environ.get('WEWORK_TOKEN')

    async def get_wework_projects(self):
        url = 'https://wework.base.vn/extapi/v2/project/list'
        page_id = 0
        async with aiohttp.ClientSession() as session:
            is_remain = True
            projects_ids = []
            while is_remain == True:
                payload = {
                    'access_token': self.token,
                    'id': page_id
                }
                async with session.post(url, data=payload) as r:
                    results = await r.json()
                    results = self.transform_json_type(results)
                    is_remain = results.get('is_remain')
                    for i in results.get('projects'):
                        if i.get('metatype') == 'project':
                            i = self.add_batched_at(i)
                            projects_ids.append(i.get('id'))
                            if len(i) > 0:
                                errors_projects = self.client.insert_rows_json(
                                    'Basevn.wework_projects',
                                    [i],
                                    ignore_unknown_values=True
                                )
        return projects_ids

    async def get_wework_projects_details(self):
        url = 'https://wework.base.vn/extapi/v2/project/get.full'
        async with aiohttp.ClientSession() as session:
            for project in await self.get_wework_projects():
                payload = {
                    'access_token': self.token,
                    'id': project
                }
                async with session.post(url, data=payload) as r:
                    results = await r.json()
                    tasklists = results.get('tasklists')
                    tasklists = [self.transform_json_type(
                        tasklist) for tasklist in tasklists]
                    tasklists = [self.add_batched_at(
                        tasklist) for tasklist in tasklists]
                    tasks = results.get('tasks')
                    tasks = [self.transform_json_type(task) for task in tasks]
                    tasks = [self.add_batched_at(task) for task in tasks]
                    if len(tasklists) > 0:
                        errors_tasklists = self.client.insert_rows_json(
                            'Basevn.wework_tasklists',
                            tasklists,
                            ignore_unknown_values=True
                        )
                    if len(tasks) > 0:
                        errors_tasklists = self.client.insert_rows_json(
                            'Basevn.wework_tasks',
                            tasks,
                            ignore_unknown_values=True
                        )

    async def run(self):
        await self.get_wework_projects_details()
        send_telegram('Wework Done')


async def run():
    await asyncio.gather(
        Workflow().run(),
        WeWork().run()
    )


def main(request=''):
    send_telegram('Basevn >>>')
    start = time.time()
    asyncio.run(run())
    end = time.time()
    send_telegram('Basevn ran for ' + str(round(end - start, 2)))
    return 'ok'