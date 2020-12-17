import re

from engine.actions.action import GenericAction


class End(GenericAction):
    def handle(self, action_data, execution_context, pipeline):
        pipeline = {"end": True}
        return execution_context, pipeline
