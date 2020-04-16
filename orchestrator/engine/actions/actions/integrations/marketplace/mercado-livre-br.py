import xmltodict
from engine.actions.action import HttpAction
from engine.utils.http import HttpRequest


HTTP_STATUS_OK_200 = 200
HTTP_STATUS_MULTIPLE_CHOICES_300 = 300


class MercadoLivreBR(HttpAction):
    SCHEMA = "schemas/integrations/marketplace/mercado-livre-br"
