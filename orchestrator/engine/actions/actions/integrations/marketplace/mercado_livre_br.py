import xmltodict
from engine.actions.action import HttpAction
from engine.utils.http import HttpRequest


class MercadoLivreBR(HttpAction):
    SCHEMA = "integrations/marketplace/mercado_livre_br"
