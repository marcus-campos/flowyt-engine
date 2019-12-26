import re

from utils.action import GenericAction
from utils.http import HttpRequest


class Request(GenericAction):
    def handle(self, action_data, context):
        request = HttpRequest(action_data.get("url"))
        request_data = {
            "data": action_data.get("data"),
            "headers": action_data.get("headers"),
        }

        response = {}

        if action_data.get("method") == "get":
            request_data["params"] = request_data["data"]
            del request_data["data"]
            request.get(**request_data)

        if action_data.get("method") == "post":
            request.post(**request_data)

        if action_data.get("method") == "put":
            request.put(**request_data)

        if action_data.get("method") == "path":
            request.path(**request_data)

        if action_data.get("method") == "delete":
            del request_data["data"]
            request.delete(**request_data)

        context.public.response = response

        return context
