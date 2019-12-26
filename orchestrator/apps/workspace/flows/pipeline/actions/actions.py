from .default import Default
from .start import Start
from .flow_var import FlowVar
from .request import Request

__actions = {"start": Start, "flow_var": FlowVar, "request": Request}


def get_action(action_name):
    return __actions.get(action_name, Default)
