from utils.action import GenericAction
from dotmap import DotMap


class FlowVar(GenericAction):
    def handle(self, action_data, context):
        context.public.flow = {**context.public.flow, **action_data}
        return context