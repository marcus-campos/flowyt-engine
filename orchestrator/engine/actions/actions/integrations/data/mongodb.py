import copy

from engine.actions.action import GenericAction
from pymongo import MongoClient


class MongoDB(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        config = execution_context.private.integrations.mongodb
        collection = self.__collection(config, action_data["collection"])
        result = self.perform_action(collection, action_data["action"], action_data["data"])
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

    def perform_action(self, collection, action, data):
        result = None

        if action == "insert_one":
            result = {"id": self.insert_one(collection, data)}
        elif action == "insert_many":
            ids = self.insert_many(collection, data)
            result = {"ids": ids}
        elif action == "find":
            result = {"id": self.insert_one(collection, data)}
        elif action == "update":
            result = {"id": self.update(collection, data)}
        elif action == "findAndModify":
            result = {"id": self.findAndModify(collection, data)}

        return result

    def insert_one(self, collection, data):
        data = copy.deepcopy(data)
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def insert_many(self, collection, data):
        data = copy.deepcopy(data)
        result = collection.insert_many(data)
        return [str(id) for id in result]

    def find(self, collection, data):
        data = copy.deepcopy(data)
        query = data.get("query")
        include = data.get("include")
        result = collection.find(query, include)
        return result

    def update(self, collection, data):
        data = copy.deepcopy(data)
        query = data.get("query")
        values = data.get("values")
        result = collection.update(query, values)
        return result

    def findAndModify(self, collection, data):
        data = copy.deepcopy(data)
        query = data.get("query")
        values = data.get("values")
        sort = data.get("sort")
        result = collection.find_and_modify(query=query, update=values, sort=sort)
        return result
