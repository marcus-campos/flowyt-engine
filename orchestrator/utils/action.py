import re
from utils.eval import contexted_run

class GenericAction():
    def __init__(self, action_data = None):
        self.action_data = action_data

    def next_action(self, context, params=None):
        if params:
            context["pipeline_context"] = {
                "next_flow": params.get("next_flow", None),
                "next_action": params.get("next_action", None)
            }
        return context

    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        print(self.action_data)
        self.handle(context)
        return self.next_action(context)


    def handle(self, context):
        return context

    def load_action_data(self, action_data,context):
        for key in action_data:
            if isinstance(action_data[key], dict):
                self.load_action_data(action_data[key], context)

            if type(action_data[key]) is list:
                for item in action_data[key]:
                    self.load_action_data(item, context)

            elements = []
            if type(action_data[key]) is str:
                elements = re.findall('\$\{.*?\}', action_data[key])
            for element in elements:
                result = contexted_run(context=context, source=element)
                action_data[key] = action_data[key].replace(element, str(result))

        return action_data