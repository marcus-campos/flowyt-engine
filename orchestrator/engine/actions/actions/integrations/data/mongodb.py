from engine.actions.action import GenericAction
import redis as red
from redis.exceptions import DataError


class MongoDB(GenericAction):
    def handle(self, action_data, context):
        response = None
        key = action_data.get("key")
        data = action_data.get("data", None)

        config = context.private.integrations.redis
        redis = self.__connect(config)

        try:
            if action_data.get("action_type") == "get":
                response = redis.get(key)
            elif action_data.get("action_type") == "set":
                redis.set(key, data)
            elif action_data.get("action_type") == "publish":
                redis.publish(key, data)
        except DataError:
            raise "We were unable to perform this action, please make sure you are entering the data correctly"
        except:
            raise "Something went wrong and it was not possible to perform this action"

        context.public.response = {"data": response}
        return context, None

    def __connect(self, config):
        try:
            conn = red.Redis(
                host=config["HOST"], port=config["PORT"], password=config["PASSWORD"], db=config["DB"]
            )
        except:
            raise "Could not connect to the informed host"

        return conn
