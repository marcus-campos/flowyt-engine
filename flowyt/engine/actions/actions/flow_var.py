from engine.actions.action import GenericAction


class FlowVar(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        execution_context.public.flow = {**execution_context.public.flow, **action_data}
        return execution_context, pipeline_context
