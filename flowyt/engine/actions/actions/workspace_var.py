from engine.actions.action import GenericAction


class WorkspaceVar(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        execution_context.public.workspace = {**execution_context.public.workspace, **action_data}
        return execution_context, pipeline_context
