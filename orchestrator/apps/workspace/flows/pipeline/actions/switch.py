import re

from utils.action import GenericAction


class Switch(GenericAction):
    def handle(self, action_data, context):
        # print(context.public.response)
        return context
