from apps.engine.actions.action import GenericAction


class Switch(GenericAction):
    def handle(self, action_data, context):
        next_action = None

        for condition in action_data.get("conditions"):
            if condition.get("operator") == "equal":
                result = condition.get("first_expression") == condition.get("second_expression")
                next_action = condition.get("next_action") if result else None
                break

            if condition.get("operator") == "different":
                result = condition.get("first_expression") != condition.get("second_expression")
                next_action = condition.get("next_action") if result else None
                break

            if condition.get("operator") == "greater_than":
                result = condition.get("first_expression") > condition.get("second_expression")
                next_action = condition.get("next_action") if result else None
                break

            if condition.get("operator") == "less_than":
                result = condition.get("first_expression") < condition.get("second_expression")
                next_action = condition.get("next_action") if result else None
                break

        if not next_action:
            next_action = action_data.get("next_action_else")

        pipeline_context = {"next_action": next_action}

        return context, pipeline_context
