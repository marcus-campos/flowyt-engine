from engine.actions.action import GenericAction
import redis as red
from redis.exceptions import DataError


class MongoDB(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        # TODO
        return execution_context, pipeline_context
