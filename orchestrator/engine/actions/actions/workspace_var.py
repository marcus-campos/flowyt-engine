from engine.actions.action import GenericAction


class WorkspaceVar(GenericAction):
    def handle(self, action_data, context):
        context.public.workspace = {**action_data}
        return context, None
