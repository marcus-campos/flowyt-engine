import os
import secrets

from functools import wraps
from shutil import copyfile

from flask import request
from flask_restful import Resource, abort
from orchestrator.settings import ENV_PATH, SECRET_KEY, SRC_DIR

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
                        "msg": "Initial settings added successfully. Restart Orchestryzi to apply the changes.",
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
                "msg": "The environment settings have been removed successfully! Restart Orchestryzi to apply the changes."
            },
            400,
        )
