import re

from engine.actions.action import GenericAction


class Response(GenericAction):
    def handle(self, action_data, execution_context, pipeline):
        pipeline["response"] = {
            **self.action_data.get("data", {}),
        }

        return execution_context, pipeline

    def __get_headers(self, headers):
        default_headers = {"Content-Type": "application/json"}
        return {**default_headers, **headers}

class ResponseHttp(Response):
    def handle(self, action_data, execution_context, pipeline):
        execution_context, pipeline = super().handle(action_data, execution_context, pipeline)
        
        pipeline["response"] = {
            "data": pipeline["response"],
            "status": self.action_data.get("status", 200),
            "headers": self.__get_headers(self.action_data.get("headers", {})),
        }

        return execution_context, pipeline

    def __get_headers(self, headers):
        default_headers = {"Content-Type": "application/json"}
        return {**default_headers, **headers}