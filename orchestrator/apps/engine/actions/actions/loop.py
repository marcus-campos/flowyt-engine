from apps.engine.actions.action import GenericAction


class Loop(GenericAction):
    def handle(self, action_data, context):
        loop_type = action_data.get("type")
        data = action_data.get("data")
        action = action_data.get("action")

        results = []

        if loop_type is "list":
            for index, value in enumerate(data):
                result = action(index, value)
                if result:
                    results.append(result)

        if loop_type is "range":
            for index in range(data):
                result = action(index)
                if result:
                    results.append(result)
        
        context.public.response = {
            "data": results
        }

        return context, None

