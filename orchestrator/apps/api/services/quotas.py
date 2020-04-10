import json

from utils.redis import Redis


class Quota:
    def __init__(self, subdomain):
        self.subdomain = subdomain
        self.redis = Redis().quota
        self.data = self.get_data(subdomain)

    def exceeded_limit(self):
        limit = self.data["limit"]
        used = self.data["used"]
        exceeded = False

        if limit == -1:
            exceeded = False
        elif used > limit:
            exceeded = True

        return exceeded

    def update(self):
        try:
            self.data["used"] += 1
            self.redis.set(self.subdomain, json.dumps(self.data))
            return True
        except:
            return False

    def get_data(self, subdomain):
        raw_data = self.redis.get(subdomain)

        if not raw_data:
            return {"used": 0, "limit": 10000}

        data = json.loads(raw_data)
        self.data = data
        return data
