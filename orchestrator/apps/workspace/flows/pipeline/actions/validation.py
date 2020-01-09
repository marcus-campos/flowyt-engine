from utils.action import GenericAction
from cerberus import Validator


class Validation(GenericAction):
    def handle(self, action_data, context):
        validate = Validator()

        if validate(document=context.public.request.data, schema=action_data.get("schema")):
            pipeline_context = {"next_action": action_data.get("next_action_success")}
        else:
            pipeline_context = {
                "next_action": action_data.get("next_action_fail"),
                "response": {"errors": validate.errors},
            }

        return context, pipeline_context
