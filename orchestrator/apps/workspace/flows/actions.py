from apps.workspace.flows.pipeline.actions.actions import get_action
from utils.eval import contexted_run_pipeline
import re


class Actions:
    def __init__(self, pipeline):
        self.actions = {}
        self.__first_action = None
        self.__next_action = None
        self.__current_action = None
        self.__load_actions(pipeline)

    def __load_actions(self, pipeline):
        actions_added = False
        for action in pipeline:
            self.actions[action["id"]] = Action(action)

            if not actions_added:
                self.__first_action = action["id"]
                self.__next_action = action["id"]
                actions_added = True

    def next_action(self, pipeline_context):
        self.__current_action = self.__next_action

        elements = {}
        
        if type(self.__current_action) is str:
            elements = re.findall("\$\{.*?\}", self.__current_action)
       
        if len(elements) > 0:
            for element in elements:
                result = contexted_run_pipeline(context=pipeline_context, source=element)
                self.__current_action = self.__current_action.replace(
                    element, str(result)
                )

        if not self.__current_action:
            return None

        self.__next_action = self.actions[self.__current_action].next_action
        return self.actions.get(self.__current_action)


class Action:
    def __init__(self, action_settings):
        self.settings = action_settings
        self.__load_action(action_settings)

    def __load_action(self, action_settings):
        self.id = action_settings["id"]
        self.data = action_settings.get("data", {})
        self.action = get_action(action_settings["action"])(action_data=self.data)
        self.next_action = action_settings["next_action"]
