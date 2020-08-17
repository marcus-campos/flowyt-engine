import re
import os

from dotmap import DotMap
from .settings import WORKSPACE_STORAGE_MODE
from engine.eval import contexted_run


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

        if WORKSPACE_STORAGE_MODE == "local":
            self.integrations = self.__execute_contextered(self.integrations)
            self.env = self.__execute_contextered(self.env)

        self.safe_mode = self.workspace_settings.get("safe_mode", True)
        self.development_language = self.workspace_settings.get("development_language", "python")

    def __execute_contextered(self, data):
        context = DotMap(
            {"public": {"env": lambda env_var, default_env_var="": os.environ.get(env_var, default_env_var)}}
        )

        for key in data:
            elements = {}

            if type(data[key]) == dict:
                data[key] = self.__execute_contextered(data[key])

            if type(data[key]) == str:
                elements = re.findall("\$\{.*?\}", data[key])

            if len(elements) > 0:
                for element in elements:
                    result = contexted_run(context=context, source=element, language="python")
                    data[key] = data[key].replace(element, str(result))

        return data
