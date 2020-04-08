class Workspace:
    def __init__(self, workspace_settings):
        self.vars = {}
        self.workspace_settings = workspace_settings

        self.id = self.workspace_settings.get("id")
        self.name = self.workspace_settings.get("name")
        self.debug = self.workspace_settings.get("debug")
        self.release = self.workspace_settings.get("release", {})
        self.integrations = self.workspace_settings.get("integrations", {})
        self.env = self.workspace_settings.get("env", {})
        self.safe_mode = self.workspace_settings.get("safe_mode", True)
        self.development_language = self.workspace_settings.get("development_language", "python")
