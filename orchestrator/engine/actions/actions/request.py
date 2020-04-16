import xmltodict
from engine.actions.action import GenericAction
from engine.utils.http import HttpRequest


HTTP_STATUS_OK_200 = 200
HTTP_STATUS_MULTIPLE_CHOICES_300 = 300


class Request(GenericAction):
    def handle(self, action_data, action_context, pipeline_context):
        response_data = {}
        request = HttpRequest(action_data.get("url"))
        request_data = {
            "data": action_data.get("data"),
            "headers": action_data.get("headers"),
            # "files": action_data.get("files"),
        }

        handler = getattr(self, action_data.get("method").lower())
        response = handler(request, request_data)

        try:
            response_data = response.json() if len(response.text) > 0 else {}
        except:
            try:
                response_data = xmltodict.parse(response.content)
            except:
                response_data = {}

        action_context.public.response = {
            "status": response.status_code,
            "data": response_data,
            "headers": dict(response.headers),
            "elapsed": {"total_seconds": response.elapsed.total_seconds()},
        }

        status_code = action_context.public.response.get("status")

        if status_code < HTTP_STATUS_OK_200 or status_code >= HTTP_STATUS_MULTIPLE_CHOICES_300:
            pipeline_context["next_action"] = self.action_data.get("next_action_fail")
        else:
            pipeline_context["next_action"] = self.action_data.get("next_action_success")

        return action_context, pipeline_context

    def get(self, request, request_data):
        del request_data["data"]
        return request.get(**request_data)

    def post(self, request, request_data):
        return request.post(**request_data)

    def patch(self, request, request_data):
        return request.patch(**request_data)

    def put(self, request, request_data):
        return request.put(**request_data)

    def delete(self, request, request_data):
        return request.delete(**request_data)
