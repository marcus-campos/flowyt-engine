from .actions.default import Default
from .actions.flow_var import FlowVar
from .actions.request import Request
from .actions.response import Response
from .actions.start import Start
from .actions.switch import Switch
from .actions.validation import Validation
from .actions.workspace_var import WorkspaceVar

__actions = {
    "start": Start,
    "flow_var": FlowVar,
    "workspace_var": WorkspaceVar,
    "request": Request,
    "switch": Switch,
    "response": Response,
    "validation": Validation,
}


def get_action(action_name):
    return __actions.get(action_name, Default)
