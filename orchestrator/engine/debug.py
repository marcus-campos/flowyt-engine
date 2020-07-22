import copy


class PipelineDebug:
    def __init__(self):
        self.__load_models()

    def __load_models(self):
        self.WORKSPACE_LOGS = {
            "workspace": {
                "id": None,
                "name": None,
                "elapsed_time": None,
                "flows": [],
            }
        }

        self.CURRENT_FLOW = None

        self.FLOW_LOGS = {
            "id": None,
            "name": None,
            "elapsed_time": None,
            "actions": [],
        }

        self.ACTION_LOGS = {
            "id": None,
            "name": None,
            "data": None,
            "time_spent": None,
        }

    def workspace(self, workspace_id, workspace_name, workspace_elapsed_time):
        self.WORKSPACE_LOGS["workspace"]["id"] = workspace_id
        self.WORKSPACE_LOGS["workspace"]["name"] = workspace_name
        self.WORKSPACE_LOGS["workspace"]["elapsed_time"] = workspace_elapsed_time

    def flow(self, flow_id, flow_name, flow_elapsed_time):
        logs = copy.deepcopy(self.FLOW_LOGS)
        logs["id"] = flow_id
        logs["name"] = flow_name
        logs["elapsed_time"] = flow_elapsed_time
        self.CURRENT_FLOW = logs

    def action(self, action_id, action_name, action_data, action_time_spent):
        logs = copy.deepcopy(self.ACTION_LOGS)
        logs["id"] = action_id
        logs["name"] = action_name
        logs["data"] = action_data
        logs["time_spent"] = action_time_spent
        self.CURRENT_FLOW["actions"].append(logs)

    def append(self):
        self.WORKSPACE_LOGS["workspace"]["flows"].append(
            copy.deepcopy(self.CURRENT_FLOW))
        self.CURRENT_FLOW = None

    def get(self):
        workspace_logs = copy.deepcopy(self.WORKSPACE_LOGS)
        self.__load_models()
        return workspace_logs
