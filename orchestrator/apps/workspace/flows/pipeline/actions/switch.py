from utils.action import GenericAction


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

            if condition.get("operator") == "greater than":
                result = condition.get("first_expression") > condition.get("second_expression")
                next_action = condition.get("next_action") if result else None
                break

            if condition.get("operator") == "less than":
                result = condition.get("first_expression") < condition.get("second_expression")
                next_action = condition.get("next_action") if result else None
                break

        if not next_action:
            condition_else = action_data.get("conditions")[-1]
            if condition_else.get("operator") == "else":
                next_action = condition_else.get("next_action")

        pipeline_context = {"next_action": next_action}

        return context, pipeline_context
