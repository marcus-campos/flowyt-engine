from engine.actions.action import GenericAction


class Run(GenericAction):
    def handle(self, action_data, context):
        context.public.response = {"data": action_data}
        return context, None
