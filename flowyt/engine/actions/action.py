import ast
import copy
import re

from cerberus import Validator
from engine.utils.dotmap import DotMap
from engine.eval import contexted_run
from engine.utils.http import HttpRequest
from engine.utils.json_parser import parse_json_file
from engine.utils.util import can_cast


class GenericAction:
    initial_action_data = None
    action_data = None
    context = None
    can_execute_async = False
    action_schema = {"type": "dict"}

    def __init__(self, action_data=None):
        if not self.initial_action_data:
            self.initial_action_data = copy.deepcopy(action_data)

        self.action_data = action_data
        self.context = None

    async def start_async(self, context):
        return self.start(context)

    def start(self, context):
        """
        Action life cycle:
        __validate_schema -> __load_action_data -> before_handle -> handle -> after_handle -> _next_action
        """
        initial_action_data = copy.deepcopy(self.initial_action_data)
        # self.__validate_schema(initial_action_data)
        self.action_data = self.__load_action_data(initial_action_data, context)

        self.action_data, context, pipeline = self.before_handle(self.action_data, context)
        context, pipeline = self.handle(self.action_data, context, pipeline)
        context, pipeline = self.after_handle(self.action_data, context, pipeline)

        return self._next_action(context, pipeline)

    def __validate_schema(self, action_data):
        action_schema = {
            "id": {"type": "string"},
            "execute_async": self.can_execute_async,
            "action": {"type": "string"},
            "data": self.action_data,
            "next_action": {"type": "string"},
        }

        validator = Validator(action_schema)
        is_valid = validator.validate(action_data)

        if not is_valid:
            raise Exception("The action scheme is incorrect")

    def before_handle(self, action_data, execution_context):
        return action_data, execution_context, {}

    def handle(self, action_data, execution_context, pipeline):
        return execution_context, pipeline

    def after_handle(self, action_data, execution_context, pipeline):
        return execution_context, pipeline

    def _next_action(self, context, pipeline=None):
        context.pipeline["response"] = None
        context.pipeline["next_flow"] = None
        context.pipeline["next_action"] = None
        context.pipeline["extra"] = None

        if pipeline:
            context.pipeline["response"] = pipeline.get("response", None)
            context.pipeline["next_flow"] = pipeline.get("next_flow", None)
            context.pipeline["next_action"] = pipeline.get("next_action", None)
            context.pipeline["extra"] = pipeline.get("extra", None)

        return context

    def __load_action_data(self, action_data, context):
        for key in action_data:
            if isinstance(action_data[key], dict):
                self.__load_action_data(action_data[key], context)

            if isinstance(action_data[key], list):
                for item in action_data[key]:
                    if isinstance(item, list) or isinstance(item, dict):
                        self.__load_action_data(item, context)

            elements = []
            language = context.private["development_language"]
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

                if type(result) is list:
                    for index in range(len(result)):
                        item = result[index]
                        if type(item) is DotMap:
                            result[index] = item.to_dict()
                    action_data[key] = result
                elif type(result) is DotMap:
                    action_data[key] = result.to_dict()
                elif can_cast(result, str):
                    action_data[key] = action_data[key].replace(element, str(result))
                else:
                    action_data[key] = result

        return action_data


class HttpAction(GenericAction):
    http_status_ok_200 = 200
    http_status_multiple_choices_300 = 300
    integration_schema = None
    action_context = None

    def before_handle(self, action_data, execution_context):
        if not self.integration_schema:
            return action_data, execution_context, {}

        action_context = copy.deepcopy(execution_context)
        action_context.public = {
            **action_context.public.toDict(),
            **self.action_context,
            # **{"p": action_data.get("path_params", {"teste": "123"})},
        }
        action_context = DotMap(action_context)

        integration_schema = self._load_scheme()
        integration_schema = self.__load_action_data(integration_schema, action_context)

        endpoint_schema = integration_schema["endpoints"][action_data["method"]].get(
            [action_data["path"]], None
        )

        if not endpoint_schema:
            return execution_context, {}

        action_data["url"] = "{0}{1}".format(integration_schema["base_url"], action_data["path"])
        action_data["headers"] = {
            **integration_schema["base_headers"],
            **endpoint_schema["headers"],
            **action_data["headers"],
        }
        action_data["data"] = {
            **integration_schema["base_data"],
            **endpoint_schema["data"],
            **action_data["data"],
        }
        action_data["params"] = {
            **integration_schema["base_params"],
            **endpoint_schema["params"],
            **action_data["params"],
        }
        del action_data["path"]
        # url, method, headers, params, data, next_action_success, next_action_fail

        return action_data, execution_context, {}

    def handle(self, action_data, execution_context, pipeline):
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

        if status_code < self.http_status_ok_200 or status_code >= self.http_status_multiple_choices_300:
            pipeline["next_action"] = self.action_data.get("next_action_fail")
        else:
            pipeline["next_action"] = self.action_data.get("next_action_success")

        return execution_context, pipeline

    def _load_scheme(self):
        schema_path = "actions/schemas/{0}.json".format(self.schema)
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
