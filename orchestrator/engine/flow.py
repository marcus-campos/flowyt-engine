from engine.settings import WORKSPACES_PATH
from utils.json_parser import parse_json_file

from .action import Actions


class Flow:
    def __init__(self, workspace, flow):
        self.vars = {}
        self.__load_flow(workspace, flow)

    def __load_flow(self, workspace, flow):
        flow_settings = parse_json_file("{0}/{1}/flows/{2}.json".format(WORKSPACES_PATH, workspace, flow))

        self.id = flow_settings.get("id")
        self.name = flow_settings.get("name")
        self.pipeline = Actions(flow_settings.get("pipeline", {}))
