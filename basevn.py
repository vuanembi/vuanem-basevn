from google.cloud import bigquery
from datetime import datetime
import json
from flask import jsonify

def main(request):
    gbq_client = bigquery.Client()
    new_dict = request.form.to_dict(flat=True)
    for key, value in new_dict.items():
        try:
            new_dict[key] = json.loads(value)
        except:
            pass
        if type(new_dict[key]) == list:
            for i in new_dict[key]:
                if type(i) == dict:
                    for key2, value2 in i.items():
                        try:
                            i[key2] = json.loads(value2)
                        except:
                            pass
        elif type(new_dict[key]) == dict:
            for key2, value2 in new_dict[key].items():
                try:
                    new_dict[key][key2] = json.loads(value2)
                except:
                    pass
        print(key, value)
        
    with open('sss.json', 'w') as f:
        json.dump(new_dict, f, indent=4)
    #table_id = "Basevn.basevn_workflow"
    #rows_to_insert = [
    #    new_dict
    #]
    #errors = gbq_client.insert_rows_json(table_id, rows_to_insert)
    #print(errors)
    #print(y)
    return "ok"