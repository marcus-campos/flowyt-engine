import re
from utils.action import GenericAction


class Response(GenericAction):
    def handle(self, action_data, context):
        pipeline_context = {"response": self.action_data}
        return context, pipeline_context
