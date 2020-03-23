from .pipeline import Pipeline
from .settings import WORKSPACE_STORAGE_MODE
from .functions import FunctionLoader

class Engine:
    def start(self, workspace_data, request_data, workspace, flow):
        # Load functions
        workspace_data = self.__load_functions(workspace, workspace_data)
        return Pipeline(workspace_data, flow).start(request_data)

    def __load_functions(self, workspace, workspace_data):
        function_loader = FunctionLoader()

        if WORKSPACE_STORAGE_MODE == "redis":
            workspace_data["functions"] = function_loader.load_string(workspace_data["functions"], "python")
        else:
            workspace_data["functions"] = function_loader.load_local(workspace)

        return workspace_data

