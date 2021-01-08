from google.cloud import bigquery
import json


def transform_to_json(request):
    result = request.form.to_dict(flat=True)
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


def select_from_json(result, platform):
    if platform == 'workflow':
        selected_result = {
            'id': result.get('id'),
            'name': result.get('name'),
            'since': result.get('since'),
            'last_update': result.get('last_update'),
            'stage_id': result.get('stage_id'),
            'stage_start': result.get('stage_start'),
            'stage_deadline': result.get('deadline'),
            'moves': result.get('moves'),
            'form': result.get('form'),
            'progression': result.get('progression'),
            'on_failed': result.get('on_failed')
        }
    elif platform == 'wework':
        for i in result['form']:
            i.pop('options')
        selected_result = {
            'id': result.get('id'),
            'name': result.get('name'),
            'deadline': result.get('deadline'),
            'stime': result.get('stime'),
            'since': result.get('since'),
            'last_update': result.get('last_update'),
            'form': result.get('form')
        }
    else:
        selected_result = None
    return selected_result


def load(result, table_id):
    bq_client = bigquery.Client()
    #with open(f'{table_id}.json', 'a') as f:
    #    json.dump(result, f, indent=4)
    rows_to_insert = [result]
    errors = bq_client.insert_rows_json(table_id, rows_to_insert)
    return str(errors)


def main(request):
    if request.method == 'GET':
        return 'okay'
    elif request.method == 'POST':
        result = request.form.to_dict(flat=True)
        if 'workflow' in result.get('gen_link'):
            row = transform_to_json(request)
            row = select_from_json(row, 'workflow')
            return load(row, 'Basevn.workflow')
        elif 'wework' in result.get('gen_link'):
            row = transform_to_json(request)
            row = select_from_json(row, 'wework')
            return load(row, 'Basevn.wework')
