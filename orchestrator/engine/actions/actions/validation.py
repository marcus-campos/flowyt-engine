from engine.actions.action import GenericAction
from cerberus import Validator


class Validation(GenericAction):
    def handle(self, action_data, action_context, pipeline_context):
        validate = Validator()

        if validate(document=action_context.public.request.data, schema=action_data.get("schema")):
            pipeline_context = {"next_action": action_data.get("next_action_success")}
        else:
            pipeline_context = {
                "next_action": action_data.get("next_action_fail"),
                "response": {"errors": validate.errors},
            }

        return action_context, pipeline_context
