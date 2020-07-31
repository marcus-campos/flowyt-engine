import asyncio
import json
from functools import wraps

import psutil
import xmltodict
from engine.manager import Engine
from flask import Response, request
from flask_restful import Resource
from orchestrator.settings import SECRET_KEY, SERVER_NAME, WORKSPACE_STORAGE_MODE
from pymongo import MongoClient

from apps.api.serializers import StartSerializer
from apps.api.services.quotas import Quota
from apps.api.services.routes import Router
from apps.api.services.workspace_load import WorkspaceLoad
from utils.middlewares import secret_key_required


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


class Monitoring:
    LOG = {"request": None, "response": {}, "trace": {}}

    def __init__(self, request, response, trace):
        self.LOG["request"] = request
        self.LOG["response"] = response
        self.LOG["trace"] = trace

    def save(self, log_config):
        if log_config:
            asyncio.run(self.__store_logs(log_config))

    async def __store_logs(self, log_config):
        config = log_config
        client = MongoClient(
            "mongodb://{0}:{1}@{2}:{3}/".format(
                config["user"], config["password"], config["host"], config["port"]
            )
        )

        db = client[config["database"]]
        logs = db["flowyt_logs"]
        log = logs.insert_one(self.LOG)


class StartFlow(Resource):
    engine_class = Engine()
    serializer_class = StartSerializer()
    workspace_load_class = WorkspaceLoad()

    def handle(self, workspace, method, path, *args, **kwargs):
        subdomain = kwargs.get("__subdomain__", "")
        is_exceeded = False

        # Check quota
        if WORKSPACE_STORAGE_MODE != "local":
            quota_class = Quota(subdomain)
            is_exceeded = quota_class.exceeded_limit()

        if is_exceeded:
            return {"message": "The request limit has been reached."}, 429

        # Load workspace
        workspace_data = self.workspace_load_class.load(workspace, subdomain)

        if not workspace_data:
            return {"message": "The requested workspace was not found on the server."}, 404

        # Check route
        flow = Router(SERVER_NAME, subdomain, workspace_data["routes"]).match(path, workspace, method)

        # Start engine
        request_data = self.__get_request_data(*args, **kwargs)
        response_data = self.engine_class.start(workspace_data, request_data, None, workspace, flow)

        # Update quota
        quota_class.update()

        # Response
        response, monitor = self.__make_response(response_data, request_data)

        # Save logs
        log_config = workspace_data["config"].get("logs", None)
        monitor.save(log_config)

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

        # Monitoring logs
        response_log = {"status": response_status, "headers": response_headers, "response": response_data}
        monitor = Monitoring(request, response_log, response.get("__debug__", {}))

        # Response
        result = Response(headers=response_headers, response=result, status=response_status)
        return result, monitor

    def __get_request_data(self, *args, **kwargs):
        request_data = {
            "headers": {k.lower().replace("-", "_"): v for k, v in dict(request.headers).items()},
            "params": locals().get("kwargs", {}),
            "qs": request.args.to_dict(),
            "form": request.form.to_dict(),
            "data": request.get_json(),
            # "files": request.file,
        }

        # Remove
        if "__subdomain__" in request_data["params"]:
            del request_data["params"]["__subdomain__"]

        if request_data["headers"].get("content_type") == "application/xml":
            request_data["data"] = xmltodict.parse(request.data, xml_attribs=False)

        request_data["debug"] = request_data["headers"].get("x_flowyt_debug", "false")

        return request_data

    def get(self, *args, **kwargs):
        return self.handle(method="GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.handle(method="POST", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.handle(method="PUT", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.handle(method="DELETE", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.handle(method="PATCH", *args, **kwargs)

    def trace(self, *args, **kwargs):
        return self.handle(method="TRACE", *args, **kwargs)

    def options(self, *args, **kwargs):
        return self.handle(method="OPTIONS", *args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.handle(method="CONNECT", *args, **kwargs)
