from utils.action import GenericAction


class Jump(GenericAction):
    def handle(self, action_data, context):
        pipeline_context = {"next_flow": self.action_data.get("next_flow")}
        return context, pipeline_context
