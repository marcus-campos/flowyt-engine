import redis as red
from orchestrator.settings import REDIS

redis = red.Redis(host=REDIS["HOST"], port=REDIS["PORT"], password=REDIS["PASSWORD"], db=REDIS["DB"])
