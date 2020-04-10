import ast
import re
from dotmap import DotMap

from engine.eval import contexted_run


class GenericAction:
    def __init__(self, action_data=None):
        self.action_data = action_data
        self.context = None

    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        context, pipeline_context = self.handle(self.action_data, context)
        return self.next_action(context, pipeline_context)

    def handle(self, action_data, context):
        return context, None

    def next_action(self, context, pipeline_context=None):
        context.pipeline_context = {}
        if pipeline_context:
            context.pipeline_context = {
                "response": pipeline_context.get("response", None),
                "next_flow": pipeline_context.get("next_flow", None),
                "next_action": pipeline_context.get("next_action", None),
            }

        return context

    def load_action_data(self, action_data, context):
        for key in action_data:
            if isinstance(action_data[key], dict):
                self.load_action_data(action_data[key], context)

            if type(action_data[key]) is list:
                for item in action_data[key]:
                    self.load_action_data(item, context)

            elements = []
            language = context.private.development_language
            if type(action_data[key]) is str:
                elements = re.findall("\$\{.*?\}", action_data[key])
                if not elements:
                    language = "python"
                    elements = re.findall("\$\(py\)\{.*?\}", action_data[key])
                    if not elements:
                        language = "javascript"
                        elements = re.findall("\$\(js\)\{.*?\}", action_data[key])

            for element in elements:
                result = contexted_run(context=context, source=element, language=language)

                if type(result) is str:
                    action_data[key] = action_data[key].replace(element, str(result))
                elif type(result) is list:
                    for index in range(len(result)):
                        item = result[index]
                        if type(item) is DotMap:
                            result[index] = item.toDict()
                    action_data[key] = result
                elif type(result) is DotMap:
                    action_data[key] = result.toDict()
                else:
                    action_data[key] = result

        return action_data