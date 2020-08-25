from .functions import FunctionLoader
from .pipeline import Pipeline
from .settings import WORKSPACE_STORAGE_MODE


class Engine:
    def start(self, workspace_data={}, request_data={}, input_data=None, workspace="", flow=""):
        # Load functions
        workspace_data = self.__load_functions(workspace, workspace_data)
        return Pipeline(workspace_data, flow).start(request_data, input_data)

    def __load_functions(self, workspace, workspace_data):
        function_loader = FunctionLoader()
        development_language = workspace_data["config"]["settings"].get("development_language", "python")

        if WORKSPACE_STORAGE_MODE == "redis":
            workspace_data["functions"] = function_loader.load_string(
                workspace_data["functions"], development_language
            )
        else:
            workspace_data["functions"] = function_loader.load_local(workspace)

        return workspace_data
