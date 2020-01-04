import re
import ast
from utils.action import GenericAction


class Response(GenericAction):
    def start(self, context):
        self.action_data = self.load_action_data(self.action_data, context)
        context = self.handle(self.action_data, context)

        self.action_data = self.__load_dict_fields(self.action_data)

        pipeline_context = {"response": self.action_data}

        return self.next_action(context, pipeline_context)

    def __load_dict_fields(self, action_data):
        # Load json fields
        for key in action_data:
            if isinstance(action_data[key], dict):
                self.__load_dict_fields(action_data[key])

            data = self.__is_dict(str(action_data[key]))

            if data:
                action_data[key] = data

        return action_data

    def __is_dict(self, data):
        try:
            return ast.literal_eval(data)
        except ValueError as e:
            return False
