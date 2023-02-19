import json


def read_level(base_path, name):
    with open(f'{base_path}/levels/{name}.json', 'r') as f:
        return json.load(f)
