import copy

from engine.actions.action import GenericAction
from pymongo import MongoClient


class MongoDB(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        config = execution_context.private.integrations.mongodb
        
        conn_name = action_data.get("conn_name")
        collection = self.__collection(config.get(conn_name), action_data["collection"])
        
        result = self.perform_action(collection, action_data["action"], action_data["args"])
        execution_context.public.response = result
        return execution_context, pipeline_context

    def __collection(self, config, collection):
        try:
            client = MongoClient(
                "mongodb://{0}:{1}@{2}:{3}".format(config.user, config.password, config.host, config.port)
            )
            db = client[config.database]
            collection = db[collection]
        except Exception as e:
            raise "Something went wrong when establishing the connection with Mongo"

        return collection

    def perform_action(self, collection, action, args):
        result = None
        result = getattr(collection, action)(**args)
        return result
