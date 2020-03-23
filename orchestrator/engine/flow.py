from engine.settings import WORKSPACES_PATH
from utils.json_parser import parse_json_file

from .action import Actions


class Flow:
    def __init__(self, workspace_data, flow):
        self.vars = {}
        
        flow_settings = workspace_data["flows"][flow]
        self.id = flow_settings.get("id")
        self.name = flow_settings.get("name")
        self.pipeline = Actions(flow_settings.get("pipeline", {}))
