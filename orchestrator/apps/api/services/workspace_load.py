import copy
import importlib.util
import os
from pathlib import Path

from orchestrator.settings import WORKSPACE_STORAGE_MODE, WORKSPACES_PATH

from utils.json_parser import parse_json_file


class WorkspaceLoad():
    base_model = {
        "config": {},
        "flows": {},
        "functions": {},
        "routes": []
    }

    def load(self, workspace, subdomain):
        if WORKSPACE_STORAGE_MODE == "local":
            return self.__load_local(workspace)

        return self.__load_redis()

    def __load_redis(self):
        pass

    def __load_local(self, workspace):
        model = copy.deepcopy(self.base_model)
        workspace_path = "{0}/{1}".format(WORKSPACES_PATH, workspace)

        # Config
        model["config"]["settings"] = parse_json_file(
            "{0}/config/settings.json".format(workspace_path)
        )
        
        # Routes
        model["routes"] = parse_json_file("{0}/routes.json".format(workspace_path))

        # Flows
        flows_path = "{0}/flows".format(workspace_path)
        flows = {}

        for flow in os.listdir(flows_path):
            flow_name = flow[:-5]
            flows[flow_name] = parse_json_file("{0}/{1}".format(flows_path, flow))

        # Functions
        functions_path = "{0}/functions".format(workspace_path)
        functions = {}

        for module in os.listdir(functions_path):
            module_path = Path(module)

            if module_path.name == "__init__.py" or not module_path.suffix == ".py":
                continue

            spec = importlib.util.spec_from_file_location(
                "module.name", functions_path + "/{0}".format(module)
            )
            module_loaded = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_loaded)
            functions[module_path.stem] = module_loaded

        model["functions"] = functions

        return model

        
