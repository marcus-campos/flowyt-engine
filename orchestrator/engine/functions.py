import os
import importlib.util
from pathlib import Path
from engine.settings import WORKSPACES_PATH


class Functions:
    def __init__(self, workspace):
        self.workspace_functions = {}
        self.workspace = workspace
        self.__load_functions(self.workspace)

    def __load_functions(self, workspace):
        functions_path = WORKSPACES_PATH + "/{0}/functions".format(workspace)

        for module in os.listdir(functions_path):
            module_path = Path(module)
            if self.__skip_module(module_path):
                continue

            spec = importlib.util.spec_from_file_location(
                "module.name", functions_path + "/{0}".format(module)
            )
            module_loaded = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_loaded)
            self.workspace_functions[module_path.stem] = module_loaded

    def __skip_module(self, module_path):
        return module_path.name == "__init__.py" or not module_path.suffix == ".py"
