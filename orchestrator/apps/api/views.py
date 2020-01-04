from apps.api.serializers import StartSerializer
from apps.workspace.flows.pipeline.pipeline import Pipeline
from flask import request
from flask_restful import Resource


class StartFlow(Resource):

    serializer_class = StartSerializer()

    def __init__(self, workspace, flow, *args, **kwargs):
        self.pipeline_class = Pipeline(workspace, flow)

    def handle(self, *args, **kwargs):
        request_data = self.__get_request_data(*args, **kwargs)
        result = self.pipeline_class.start(request_data=request_data)

        status = result.get("status", 200)
        _status = result.get("_status", None)

        if _status:
            del result["_status"]
            status = _status

        return result, status

    def __get_request_data(self, *args, **kwargs):
        request_data = {
            "headers": dict(request.headers),
            "params": locals().get("kwargs", {}),
            "qs": request.args.to_dict(),
            "form": request.form.to_dict(),
            "data": request.get_json(),
        }

        return request_data

    def get(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.handle(*args, **kwargs)
