from apps.engine.actions.action import GenericAction


class WorkspaceVar(GenericAction):
    def handle(self, action_data, context):
        context.public.workspace = {**context.public.flow, **action_data}
        return context, None
