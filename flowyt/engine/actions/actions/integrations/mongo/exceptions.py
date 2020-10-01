from engine.exceptions.base import FlowytException

class MongoConnectionErrorException:
    def __init__(self, action_name=None):
        self.message = "Something went wrong when establishing the connection with Mongo"
        super().__init__(self.message)