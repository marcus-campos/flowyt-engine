import copy
import json
import os

from orchestrator.settings import WORKSPACE_STORAGE_MODE, WORKSPACES_PATH

from utils.json_parser import parse_json_file
from utils.redis import Redis


class WorkspaceLoad:
    base_model = {"config": {}, "flows": {}, "functions": {}, "routes": []}

    def load(self, workspace, subdomain):
        if WORKSPACE_STORAGE_MODE == "local":
            return self.__load_local(workspace)

        return self.__load_redis(workspace, subdomain)

    def __load_redis(self, worksace, subdomain):
        redis = Redis().workspace
        raw_data = redis.get("{0}.{1}".format(subdomain, worksace))

        if not raw_data:
            return None

        return json.loads(raw_data)

    def __load_local(self, workspace):
        model = copy.deepcopy(self.base_model)
        workspace_path = "{0}/{1}".format(WORKSPACES_PATH, workspace)

        # Config
        model["config"]["settings"] = parse_json_file("{0}/config/settings.json".format(workspace_path))

        # Routes
        model["routes"] = parse_json_file("{0}/routes.json".format(workspace_path))

        # Flows
        flows_path = "{0}/flows".format(workspace_path)
        flows = {}

        for flow in os.listdir(flows_path):
            flow_name = flow[:-5]
            flows[flow_name] = parse_json_file("{0}/{1}".format(flows_path, flow))

        return model
