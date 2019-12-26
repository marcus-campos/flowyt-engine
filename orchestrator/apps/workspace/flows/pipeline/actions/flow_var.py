from utils.action import GenericAction
from dotmap import DotMap

class FlowVar(GenericAction):
    def handle(self, context):
        context.public.flow = {**context.public.flow, **self.action_data}
        return context