from utils.json_parser import parse_json_file
from .actions import Actions


class Flow:
    def __init__(self, workspace, flow):
        self.vars = {}
        self.__load_flow(workspace, flow)

    def __load_flow(self, workspace, flow):
        flow_settings = parse_json_file("/{0}/flows/{1}.json".format(workspace, flow))

        self.id = flow_settings.get("id")
        self.name = flow_settings.get("name")
        self.pipeline = Actions(flow_settings.get("pipeline", {}))
