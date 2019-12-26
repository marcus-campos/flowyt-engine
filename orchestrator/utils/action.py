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
        return self.next_action(context)