from apps.api.serializers import StartSerializer
from apps.workspace.flows.pipeline.pipeline import Pipeline
from flask import request, Response
from flask_restful import Resource
import json


class StartFlow(Resource):

    serializer_class = StartSerializer()

    def __init__(self, workspace, flow, *args, **kwargs):
        self.pipeline_class = Pipeline(workspace, flow)

    def handle(self, *args, **kwargs):
        request_data = self.__get_request_data(*args, **kwargs)
        response_data = self.pipeline_class.start(request_data=request_data)
        response = self.__make_response(response_data, request_data)

        return response

    def __make_response(self, response, request):
        request_headers = request.get("headers", {})

        response_status = response.get("status", 200)
        response_headers = response.get("headers", {})
        response_data = response.get("data", {})

        # Add debug in response
        if request.get("debug", "false") == "true":
            response_data["__debug__"] = response.get("__debug__", {})

        # Default json
        result = json.dumps(response_data)
        
        # Change response
        if request_headers.get("accept", None) == "application/json":
            result = result
        elif request_headers.get("accept", None) == "application/xml":
            result = None
        elif response_headers.get("content_type", None) == "application/xml":
            result = None

        result = Response(headers=response_headers, response=result, status=response_status)
        return result

    def __get_request_data(self, *args, **kwargs):
        request_data = {
            "headers": {k.lower().replace("-", "_"): v for k, v in dict(request.headers).items()},
            "params": locals().get("kwargs", {}),
            "qs": request.args.to_dict(),
            "form": request.form.to_dict(),
            "data": request.get_json(),
        }

        request_data["debug"] = request_data["headers"].get("x_orchestryzi_debug", "false")

        return request_data

    def get(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
