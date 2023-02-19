import json


def read_config(path):
    with open(path, 'r') as cfg:
        return json.load(cfg)
