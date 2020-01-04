import re
from utils.eval import contexted_run


class GenericAction:
    def __init__(self, action_data=None):
        self.action_data = action_data

    def next_action(self, context, pipeline_context=None):
        context.pipeline_context = {}
        if pipeline_context:
            context.pipeline_context = {
                "response": pipeline_context.get("response", None),
                "next_flow": pipeline_context.get("next_flow", None),
                "next_action": pipeline_context.get("next_action", None),
            }

        return context

    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        context = self.handle(self.action_data, context)
        return self.next_action(context)

    def handle(self, action_data, context):
        return context

    def load_action_data(self, action_data, context):
        for key in action_data:
            if isinstance(action_data[key], dict):
                self.load_action_data(action_data[key], context)

            if type(action_data[key]) is list:
                for item in action_data[key]:
                    self.load_action_data(item, context)

            elements = []
            if type(action_data[key]) is str:
                elements = re.findall("\$\{.*?\}", action_data[key])

            for element in elements:
                result = contexted_run(context=context, source=element)
                action_data[key] = action_data[key].replace(element, str(result))

        return action_data
