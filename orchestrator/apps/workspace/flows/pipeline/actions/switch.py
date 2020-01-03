from utils.action import GenericAction


class Switch(GenericAction):
    def __init__(self):
        self.action_data = None

    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)

        next_action = self.handle(self.action_data, context)
        pipeline_context = {"next_action": next_action}

        return self.next_action(context, pipeline_context)

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

        return next_action
