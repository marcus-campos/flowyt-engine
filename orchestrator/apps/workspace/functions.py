import os
import importlib.util

from orchestrator.settings import BASE_DIR, WORKSPACES_DIR

class Functions():
    def __init__(self, workspace):
        self.workspace_functions = {}
        self.workspace = workspace
        self.__load_functions(self.workspace)

    def __load_functions(self, workspace):
        functions_path = BASE_DIR + WORKSPACES_DIR + "/{0}/functions".format(workspace)
        
        for module in os.listdir(functions_path):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
           
            spec = importlib.util.spec_from_file_location("module.name", functions_path + "/{0}".format(module))
            module_loaded = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_loaded)
            self.workspace_functions[module[:-3]] = module_loaded