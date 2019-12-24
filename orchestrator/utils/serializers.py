from flask_restful import reqparse


class GenericSerializer():
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.rules(self.parser)

    def rules(self, rule):
        pass

    def is_valid(self):
        return self.parser.parse_args()