from .default import Default
from .start import Start
from .flow_var import FlowVar
from .request import Request
from .switch import Switch
from .response import Response

__actions = {"start": Start, "flow_var": FlowVar, "request": Request, "switch": Switch, "response": Response}


def get_action(action_name):
    return __actions.get(action_name, Default)
