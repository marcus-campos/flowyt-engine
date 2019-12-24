from flask_restful import reqparse

parser = reqparse.RequestParser(bundle_errors=True)


class GenericSerializer():
    def __init__(self):
        self.rules(parser)

    def _rules(self, rule):
        pass

    def is_valid(self):
        return parser.parse_args()