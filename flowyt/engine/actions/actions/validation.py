from cerberus import Validator
from engine.actions.action import GenericAction


class Validation(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        validate = Validator()

        if validate(document=execution_context.public.request.data, schema=action_data.get("schema")):
            pipeline_context = {"next_action": action_data.get("next_action_success")}
        else:
            pipeline_context = {
                "next_action": action_data.get("next_action_fail"),
                "response": {"errors": validate.errors},
            }

        return execution_context, pipeline_context
