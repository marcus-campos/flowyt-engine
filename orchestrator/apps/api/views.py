import json
import psutil
from functools import wraps

import xmltodict
from flask import Response, request
from flask_restful import Resource
from orchestrator.settings import SECRET_KEY

from apps.api.serializers import StartSerializer
from engine.pipeline import Pipeline
from utils.middlewares import secret_key_required


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
            if type(response_data) is list:
                response_data = {"data": response_data}
            response_data["__debug__"] = response.get("__debug__", {})

        if "exception" in response:
            response_data["exception"] = response.get("exception")
            if not response_data.get("exception"):
                response_data["exception"] = "Something went wrong. Enable debug mode to see more details."

            if "__debug__" in response_data:
                if not response_data.get("__debug__"):
                    del response_data["__debug__"]

        # Default json
        result = json.dumps(response_data)

        # Change response
        if request_headers.get("accept") == "application/json":
            result = result
        elif (
            request_headers.get("accept") == "application/xml"
            or response_headers.get("Content-Type") == "application/xml"
        ):
            if request.get("debug") == "true":
                response_data = {"root": response_data}
            result = xmltodict.unparse(response_data)
            response_headers["Content-Type"] = "application/xml"

        result = Response(headers=response_headers, response=result, status=response_status)
        return result

    def __get_request_data(self, *args, **kwargs):
        request_data = {
            "headers": {k.lower().replace("-", "_"): v for k, v in dict(request.headers).items()},
            "params": locals().get("kwargs", {}),
            "qs": request.args.to_dict(),
            "form": request.form.to_dict(),
            "data": request.get_json(),
            # "files": request.file,
        }

        if request_data["headers"].get("content_type") == "application/xml":
            request_data["data"] = xmltodict.parse(request.data, xml_attribs=False)

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


class Workspaces(Resource):
    def __init__(self, workspaces_urls):
        self.workspaces_urls = workspaces_urls

    @secret_key_required
    def get(self):
        urls = []

        for url in self.workspaces_urls:
            urls.append(
                {
                    "path": url.get("path"),
                    "methods": url.get("methods"),
                    "workspace": url.get("kwargs").get("workspace"),
                    "flow": url.get("kwargs").get("flow"),
                    "subdomain": url.get("subdomain"),
                }
            )
        return urls


class Ping(Resource):
    def get(self):
        return {"msg": "It's all good!", "curious?": "https://www.youtube.com/watch?v=c4nunES9DyI"}


class Info(Resource):
    @secret_key_required
    def get(self):
        cpu = {
            "cpu{0}".format(index): percent
            for index, percent in enumerate(psutil.cpu_percent(interval=1, percpu=True))
        }
        memory = psutil.virtual_memory()
        return {
            "cpu": cpu,
            "memory": {
                "total": round((memory.total / 1024) / 1024),
                "used": round((memory.used / 1024) / 1024),
                "available": round((memory.available / 1024) / 1024),
                "free": round((memory.free / 1024) / 1024),
                "percent": memory.percent,
            },
        }
