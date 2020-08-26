import re

from engine.actions.action import GenericAction


class Response(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        running_mode = execution_context['pipeline_context']['running_mode']
        pipeline_context["response"] = {
            "data": self.action_data.get("data", {}),
        }

        if running_mode == "http":
            pipeline_context["response"] = {
                **pipeline_context["response"],
                "status": self.action_data.get("status", 200),
                "headers": self.__get_headers(self.action_data.get("headers", {})),
            }
        return execution_context, pipeline_context

    def __get_headers(self, headers):
        default_headers = {"Content-Type": "application/json"}
        return {**default_headers, **headers}
