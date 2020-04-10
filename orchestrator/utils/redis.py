import redis as red
from orchestrator.settings import REDIS


class Redis:
    def __init__(self):
        self.workspace = self.__connect(REDIS["WORKSPACE"])
        self.quota = self.__connect(REDIS["QUOTA"])

    def __connect(self, config):
        return red.Redis(
            host=config["HOST"], port=config["PORT"], password=config["PASSWORD"], db=config["DB"]
        )
