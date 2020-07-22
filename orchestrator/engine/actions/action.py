import ast
import copy
import re

from dotmap import DotMap
from engine.eval import contexted_run
from engine.utils.http import HttpRequest
from engine.utils.json_parser import parse_json_file


class GenericAction:
    def __init__(self, action_data=None):
        self.action_data = action_data
        self.context = None

    """
        Action life cycle: 
        _load_action_data -> before_handle -> handle -> after_handle -> _next_action
    """

    def start(self, context):
        self.action_data = self._load_action_data(self.action_data, context)

        self.action_data, context, pipeline_context = self.before_handle(self.action_data, context)
        context, pipeline_context = self.handle(self.action_data, context, pipeline_context)
        context, pipeline_context = self.after_handle(self.action_data, context, pipeline_context)

        return self._next_action(context, pipeline_context)

    def before_handle(self, action_data, execution_context):
        return action_data, execution_context, {}

    def after_handle(self, action_data, execution_context, pipeline_context):
        return execution_context, pipeline_context

    def handle(self, action_data, execution_context, pipeline_context):
        return execution_context, pipeline_context

    def _next_action(self, context, pipeline_context=None):
        context.pipeline_context = {}
        if pipeline_context:
            context.pipeline_context = {
                "response": pipeline_context.get("response", None),
                "next_flow": pipeline_context.get("next_flow", None),
                "next_action": pipeline_context.get("next_action", None),
            }

        return context

    def _load_action_data(self, action_data, context):
        for key in action_data:
            if isinstance(action_data[key], dict):
                self._load_action_data(action_data[key], context)

            if type(action_data[key]) is list:
                for item in action_data[key]:
                    self._load_action_data(item, context)

            elements = []
            language = context.private.development_language
            if type(action_data[key]) is str:
                elements = re.findall("\$\{.*?\}", action_data[key])
                if not elements:
                    language = "python"
                    elements = re.findall("\$\(py\)\{.*?\}", action_data[key])
                    if not elements:
                        language = "javascript"
                        elements = re.findall("\$\(js\)\{.*?\}", action_data[key])

            for element in elements:
                result = contexted_run(context=context, source=element, language=language)

                if type(result) is str:
                    action_data[key] = action_data[key].replace(element, str(result))
                elif type(result) is list:
                    for index in range(len(result)):
                        item = result[index]
                        if type(item) is DotMap:
                            result[index] = item.toDict()
                    action_data[key] = result
                elif type(result) is DotMap:
                    action_data[key] = result.toDict()
                else:
                    action_data[key] = result

        return action_data


class HttpAction(GenericAction):
    HTTP_STATUS_OK_200 = 200
    HTTP_STATUS_MULTIPLE_CHOICES_300 = 300
    SCHEMA = None
    ACTION_CONTEXT = None

    def before_handle(self, action_data, execution_context):
        if not self.SCHEMA:
            return execution_context, {}

        action_context = copy.deepcopy(execution_context)
        action_context.public = {**action_context.public.toDict(), **self.ACTION_CONTEXT, **{"p": action_data.get("path_params", {"teste": "123"})}}
        action_context = DotMap(action_context)

        schema = self._load_scheme()
        schema = self._load_action_data(schema, action_context)

        endpoint_schema = schema["endpoints"][action_data["method"]].get([action_data["path"]], None)
        
        if not endpoint_schema:
            return execution_context, {}
        
        action_data["url"] = "{0}{1}".format(schema["base_url"], action_data["path"])
        action_data["headers"] = {**schema["base_headers"], **endpoint_schema["headers"], **action_data["headers"]}
        action_data["data"] = {**schema["base_data"], **endpoint_schema["data"], **action_data["data"]}
        action_data["params"] = {**schema["base_params"], **endpoint_schema["params"], **action_data["params"]}
        del action_data["path"]
        # url, method, headers, params, data, next_action_success, next_action_fail

        return action_data, execution_context, {}

    def handle(self, action_data, execution_context, pipeline_context):
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

        execution_context.public.response = {
            "status": response.status_code,
            "data": response_data,
            "headers": dict(response.headers),
            "elapsed": {"total_seconds": response.elapsed.total_seconds()},
        }

        status_code = execution_context.public.response.get("status")

        if status_code < self.HTTP_STATUS_OK_200 or status_code >= self.HTTP_STATUS_MULTIPLE_CHOICES_300:
            pipeline_context["next_action"] = self.action_data.get("next_action_fail")
        else:
            pipeline_context["next_action"] = self.action_data.get("next_action_success")

        return execution_context, pipeline_context

    def _load_scheme(self):
        schema_path = "actions/schemas/{0}.json".format(self.SCHEMA)
        schema = parse_json_file(schema_path)
        return schema

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
