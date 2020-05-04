from .actions.default import Default
from .actions.flow_var import FlowVar
from .actions.integrations.data.redis import Redis
from .actions.integrations.data.sql_db import SqlDatabase
from .actions.jump import Jump
from .actions.loop import Loop
from .actions.request import Request
from .actions.response import Response
from .actions.run import Run
from .actions.start import Start
from .actions.switch import Switch
from .actions.validation import Validation
from .actions.workspace_var import WorkspaceVar

from .actions.integrations.marketplace.mercado_livre import MercadoLivre


__actions = {
    "start": Start,
    "flow_var": FlowVar,
    "workspace_var": WorkspaceVar,
    "request": MercadoLivre,
    "switch": Switch,
    "response": Response,
    "validation": Validation,
    "jump": Jump,
    "sql_db": SqlDatabase,
    "loop": Loop,
    "run": Run,
    "redis": Redis,
}


def get_action(action_name):
    return __actions.get(action_name, Default)
