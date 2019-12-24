from flask import request
from flask_restful import Resource, abort

import json

from apps.api.serializers import StartSerializer
from apps.engine.pipeline import Pipeline

class StartFlow(Resource):

    serializer_class = StartSerializer()
    pipeline_class = Pipeline()

    def __init__(self, workspace, flow, *args, **kwargs):
        self.workspace = workspace
        self.flow = flow

    def handle(self, *args, **kwargs):
        request_data = self.__get_request_data(*args, **kwargs)
        self.pipeline_class.start(
            workspace=self.workspace, 
            flow=self.flow,
            request_data=request_data
        )
    
    def __get_request_data(self, *args, **kwargs):
        request_data = {
            "headers": dict(request.headers),
            "params": locals().get('kwargs', {}),
            "qs": request.args.to_dict(),
            "form": request.form.to_dict(),
            "data": request.get_json()
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
