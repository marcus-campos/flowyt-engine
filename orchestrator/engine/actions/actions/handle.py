import copy
from engine.actions.action import GenericAction


class Handle(GenericAction):
    def handle(self, action_data, context):
        pipeline_class = context.private.pipeline_class
        pipeline_class.flow = action_data["flow"]

        dict_context = copy.deepcopy(context.toDict())
        result = pipeline_class.process(dict_context)
        context.public.response = result
        return context, None
