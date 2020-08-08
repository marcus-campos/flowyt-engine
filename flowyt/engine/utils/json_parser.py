import json

from engine.settings import ENGINE_PATH


def parse_json_file(path):
    full_path = ENGINE_PATH + path
    with open(full_path, "r") as f:
        parsed_json = json.load(f)
    return parsed_json
