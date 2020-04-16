from engine.actions.action import GenericAction
import redis as red
from redis.exceptions import DataError


class MongoDB(GenericAction):
    def handle(self, action_data, action_context, pipeline_context):
        #TODO
        return action_context, pipeline_context
