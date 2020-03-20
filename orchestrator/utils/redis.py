import redis as red
from orchestrator.settings import REDIS

redis = red.Redis(host=REDIS["host"], port=REDIS["port"], password=REDIS["password"], db=REDIS["db"])
