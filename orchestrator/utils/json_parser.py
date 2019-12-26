import json

from orchestrator.settings import (BASE_DIR, WORKSPACES_DIR)


def parse_json_file(path):
    settings_path = BASE_DIR + WORKSPACES_DIR + "{0}".format(path)
    with open(settings_path, 'r') as f:
        parsed_json = json.load(f)
    return parsed_json