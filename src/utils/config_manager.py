import json


def load_config(config_filename):
    with open(config_filename, 'r') as f:
        config = json.load(f)
    return config
