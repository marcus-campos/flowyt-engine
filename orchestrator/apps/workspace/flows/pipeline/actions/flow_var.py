from utils.action import GenericAction

class FlowVar(GenericAction):
    def start(self, context):
        action_data = self.action_data
        public_vars = context.get("public", {})
        
        for key in action_data:
            action_data[key] = action_data[key].format(**public_vars)

        print(action_data)

        return self.next_action(context)

