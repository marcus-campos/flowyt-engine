import json


def parse_json_file(path):
    print(path)
    with open(path, "r") as f:
        parsed_json = json.load(f)
    return parsed_json
