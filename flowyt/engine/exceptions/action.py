from .base import FlowytException


class UnsynchronizedActionException(FlowytException):
    def __init__(self, action_name=None):
        self.message = "You cannot perform this action asynchronously"

        if action_name:
            self.message = "You cannot perform the {0} action asynchronously".format(action_name)
        super().__init__(self.message)
