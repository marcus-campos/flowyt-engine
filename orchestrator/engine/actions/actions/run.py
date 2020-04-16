from engine.actions.action import GenericAction


class Run(GenericAction):
    def handle(self, action_data, action_context, pipeline_context):
        action_context.public.response = {"data": action_data}
        return action_context, pipeline_context
