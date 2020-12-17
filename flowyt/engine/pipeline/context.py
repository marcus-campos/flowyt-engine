from engine.utils.dotmap import DotMap


class Context:
    public = {}
    private = {}
    pipeline = {}

    def __init__(self, public, private, pipeline):
        self.public = public
        self.private = private
        self.pipeline = pipeline

    def to_dotmap(self):
        dictionary = self.__dict__
        return DotMap(dictionary)
