import xmltodict
from engine.actions.action import HttpAction
from engine.utils.http import HttpRequest


class MercadoLivre(HttpAction):
    SCHEMA = "integrations/marketplace/mercado_livre"
    ACTION_CONTEXT = {"access_token": 123, "site_id": "MLB"}
