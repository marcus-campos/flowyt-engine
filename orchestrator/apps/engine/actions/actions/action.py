from apps.engine.actions.action import GenericAction


class Action(GenericAction):
    def handle(self, action_data, context):
        context.public.response = {"data": action_data}
        return context, None
