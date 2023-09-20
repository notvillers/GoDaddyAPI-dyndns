import json
import os

def daddy_api(file):
    api_list = []
    i = 0
    if os.path.exists(file):
        with open(file, 'r') as json_file:
            api_datas = json.load(json_file)
        for api_data in api_datas:
            api_row = []
            api_row.append(api_data["domain"])
            api_row.append(api_data["type"])
            api_row.append(api_data["name"])
            api_row.append(api_data["api_key"])
            api_row.append(api_data["api_secret"])
            api_list.append(api_row)
            i += 1
    else:
        example_data = [
            {
            "domain" : "example.com",
            "type": "A",
            "name": "@",
            "api_key": "Your_API_key",
            "api_secret": "Your_secret_API_key"
            }
        ]
        with open(file, 'w') as file:
            json.dump(example_data, file)

    return api_list, i