from utils.json_parser import parse_json_file


class Workspace():
    def __init__(self, workspace):
        self.vars = {}
        self.__load_workspace(workspace)

    def __load_workspace(self, workspace):
        workspace_settings = parse_json_file("/{0}/config/settings.json".format(workspace))

        self.id = workspace_settings.get('id')
        self.name = workspace_settings.get('name')
        self.release = workspace_settings.get('release', {})
        self.integrations = workspace_settings.get('integrations', {})
        self.env = workspace_settings.get('env', {})