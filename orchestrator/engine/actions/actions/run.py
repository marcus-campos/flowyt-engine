from engine.actions.action import GenericAction


class Run(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        execution_context.public.response = {"data": action_data}
        return execution_context, pipeline_context
