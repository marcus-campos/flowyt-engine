from .default import Default
from .flow_var import FlowVar
from .request import Request
from .response import Response
from .start import Start
from .switch import Switch

__actions = {
    "start": Start,
    "flow_var": FlowVar,
    "request": Request,
    "switch": Switch,
    "response": Response,
}


def get_action(action_name):
    return __actions.get(action_name, Default)
