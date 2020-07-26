import copy
from engine.actions.action import GenericAction


class Handle(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        pipeline_class = execution_context.pipeline_context.__class
        pipeline_class.flow = action_data["flow"]

        dict_context = copy.copy(execution_context.toDict())
        result = pipeline_class.process(dict_context)
        execution_context.public.response = result
        return execution_context, None
