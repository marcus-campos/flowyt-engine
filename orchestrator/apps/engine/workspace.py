from orchestrator.settings import WORKSPACES_PATH

from utils.json_parser import parse_json_file


class Workspace:
    def __init__(self, workspace):
        self.vars = {}
        self.__load_workspace(workspace)

    def __load_workspace(self, workspace):
        workspace_settings = parse_json_file(
            "{0}/{1}/config/settings.json".format(WORKSPACES_PATH, workspace)
        )

        self.id = workspace_settings.get("id")
        self.name = workspace_settings.get("name")
        self.debug = workspace_settings.get("debug")
        self.release = workspace_settings.get("release", {})
        self.integrations = workspace_settings.get("integrations", {})
        self.env = workspace_settings.get("env", {})
        self.safe_mode = workspace_settings.get("safe_mode", True)
