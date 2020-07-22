from engine.actions.action import GenericAction


class Jump(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        pipeline_context = {"next_flow": self.action_data.get("next_flow")}
        return execution_context, pipeline_context
