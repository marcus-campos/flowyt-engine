from engine.actions.action import GenericAction


class WorkspaceVar(GenericAction):
    def handle(self, action_data, action_context, pipeline_context):
        action_context.public.workspace = {**action_data}
        return action_context, pipeline_context
