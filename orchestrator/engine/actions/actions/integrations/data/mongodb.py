from engine.actions.action import GenericAction
from pymongo import MongoClient


class MongoDB(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        config = execution_context.private.integrations.mongodb
        collection = self.__collection(config, execution_context["collection"])

        return execution_context, pipeline_context

    def __collection(self, config, collection):
        client = MongoClient(
            "mongodb://{0}:{1}@{2}:{3}".format(
                config.user, config.password, config.host, config.port
            )
        )
        db = client[config.database]
        collection = db[collection]
        return collection

    def perform_action(self, collection, action):
        if action == "insert_one":
            pass

    def insert_one(self, collection, data):
        result = collection.insert_one(data)
        return result