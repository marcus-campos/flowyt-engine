import re
from engine.actions.action import GenericAction


class Response(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        pipeline_context = {
            "response": {
                "status": self.action_data.get("status", 200),
                "headers": self.__get_headers(self.action_data.get("headers", {})),
                "data": self.action_data.get("data", {}),
            }
        }
        return execution_context, pipeline_context

    def __get_headers(self, headers):
        default_headers = {"Content-Type": "application/json"}
        return {**default_headers, **headers}
