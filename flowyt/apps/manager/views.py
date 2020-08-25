import os
import secrets
from functools import wraps
from shutil import copyfile

from flask import request
from flask_restful import Resource, abort

from flowyt.settings import ENV_PATH, SECRET_KEY

from utils.middlewares import secret_key_required


class Setup(Resource):
    def get(self):
        if not SECRET_KEY:
            env_exists = os.path.exists(ENV_PATH)

            if not env_exists:
                secret_token = secrets.token_hex(32)

                copyfile(ENV_PATH + ".example", ENV_PATH)
                lines = open(ENV_PATH).read().splitlines()

                for index in range(len(lines)):
                    if lines[index].startswith("APP_SECRET_KEY="):
                        lines[index] = "APP_SECRET_KEY=" + secret_token

                open(ENV_PATH, "w").write("\n".join(lines))
                return (
                    {
                        "msg": "Initial settings added successfully. Restart Flowyt to apply the changes.",
                        "secret": secret_token,
                    },
                    200,
                )

        return (
            {"msg": "It is not possible to perform a new setup without first revoking the current token"},
            400,
        )

    @secret_key_required
    def delete(self):
        env_exists = os.path.exists(ENV_PATH)
        if env_exists:
            os.remove(ENV_PATH)
        return (
            {
                "msg": "The environment settings have been removed successfully! Restart Flowyt to apply the changes."
            },
            400,
        )


class Ping(Resource):
    def get(self):
        return {"msg": "It's all good!", "curious?": "https://www.youtube.com/watch?v=c4nunES9DyI"}


class Info(Resource):
    @secret_key_required
    def get(self):
        cpu = {
            "cpu{0}".format(index): percent
            for index, percent in enumerate(psutil.cpu_percent(interval=1, percpu=True))
        }
        memory = psutil.virtual_memory()
        return {
            "cpu": cpu,
            "memory": {
                "total": round((memory.total / 1024) / 1024),
                "used": round((memory.used / 1024) / 1024),
                "available": round((memory.available / 1024) / 1024),
                "free": round((memory.free / 1024) / 1024),
                "percent": memory.percent,
            },
        }
