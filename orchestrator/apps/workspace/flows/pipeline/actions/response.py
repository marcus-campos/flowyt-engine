import re
from utils.action import GenericAction


class Response(GenericAction):
    def handle(self, action_data, context):
        pipeline_context = {
            "response": {
                "status": self.action_data.get("status", 200),
                "headers": self.__get_headers(self.action_data.get("headers", {})),
                "data": self.action_data.get("data", {}),
            }
        }
        return context, pipeline_context

    def __get_headers(self, headers):
        default_headers = {"Content-Type": "application/json"}

        return {**default_headers, **headers}
