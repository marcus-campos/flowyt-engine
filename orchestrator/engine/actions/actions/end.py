import re
from engine.actions.action import GenericAction


class End(GenericAction):
    def handle(self, action_data, context):
        pipeline_context = {"end": True}
        return context, pipeline_context
