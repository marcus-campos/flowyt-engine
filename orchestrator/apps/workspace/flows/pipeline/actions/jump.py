from utils.action import GenericAction


class Jump(GenericAction):
    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        pipeline_context = {"next_flow": self.action_data.get("next_flow")}
        return self.next_action(context, pipeline_context)
