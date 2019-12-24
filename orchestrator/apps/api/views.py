from flask import request
from flask_restful import Resource, abort

from .serializers import BuildSerializer


class StartFlow(Resource):
    def get(self):
        return 'oi'

    def post(self, *args, **kwargs):
        print(locals().get('kwargs'))
        return 'oi'