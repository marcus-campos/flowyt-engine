from engine.actions.action import GenericAction


class Loop(GenericAction):
    def handle(self, action_data, action_context, pipeline_context):
        loop_type = action_data.get("type")
        data = action_data.get("data")
        action = action_data.get("action")

        results = []

        if loop_type == "list":
            for index, value in enumerate(data):
                result = action(index, value)
                if result:
                    results.append(result)

        if loop_type == "range":
            for index in range(data):
                result = action(index)
                if result:
                    results.append(result)

        action_context.public.response = {"data": results}

        return action_context, pipeline_context
