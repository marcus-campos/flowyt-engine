from engine.settings import WORKSPACES_PATH

from .action import Actions


class Flow:
    def __init__(self, workspace_data, flow):
        flow_settings = workspace_data["flows"][flow]
        self.id = flow_settings.get("id")
        self.name = flow_settings.get("name")
        self.pipeline = Actions(flow_settings.get("pipeline", {}))
