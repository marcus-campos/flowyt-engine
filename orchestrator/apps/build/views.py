from flask import request
from flask_restful import Resource, abort

from apps.build.serializers import BuildSerializer


class BuildDetail(Resource):
    def get(self, build_id):
        return build_id


class Build(Resource):
    serializer_class = BuildSerializer()

    def post(self):
        args = self.serializer_class.is_valid()
        return {'msg': 'oiii', 'body': args}, 201
