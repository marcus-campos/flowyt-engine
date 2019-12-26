import re

from utils.action import GenericAction
from utils.http import HttpRequest


class Request(GenericAction):
    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        context = self.handle(self.action_data, context)

        status_code = context.public.response.get("status_code")
        pipeline_context = {}

        if status_code < 200 or status_code > 299:
            pipeline_context["next_action"] = self.action_data.get("next_action_fail")
        else:
            pipeline_context["next_action"] = self.action_data.get("next_action_success")

        return self.next_action(context, pipeline_context)

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
            response = request.get(**request_data)

        if action_data.get("method") == "post":
            response = request.post(**request_data)

        if action_data.get("method") == "put":
            response = request.put(**request_data)

        if action_data.get("method") == "path":
            response = request.path(**request_data)

        if action_data.get("method") == "delete":
            del request_data["data"]
            response = request.delete(**request_data)

        context.public.response = {
            "status_code": response.status_code,
            "data": response.json() if len(response.text) > 0 else {},
            "headers": response.headers,
        }

        return context
