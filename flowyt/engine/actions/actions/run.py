from engine.actions.action import GenericAction


class Run(GenericAction):
    def handle(self, action_data, execution_context, pipeline):
        execution_context.public.response = {"data": action_data}
        return execution_context, pipeline
