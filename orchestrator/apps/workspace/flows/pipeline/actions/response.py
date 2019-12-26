import re

from utils.action import GenericAction


class Response(GenericAction):
    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        context = self.handle(self.action_data, context)

        pipeline_context = {"response": self.action_data}

        return self.next_action(context, pipeline_context)
