import copy
import time

from engine.actions.action import GenericAction
from engine.debug import PipelineDebug


class Handle(GenericAction):
    can_execute_async = True

    def handle(self, action_data, execution_context, pipeline_context):
        start_time = time.time()

        pipeline_class = execution_context.pipeline_context.self_class
        pipeline_class.flow = action_data["flow"]

        dict_context = execution_context.toDict()

        # Change debug logs
        dict_context["pipeline_context"]["logs"] = PipelineDebug()
        dict_context["pipeline_context"]["logs"].workspace(
            dict_context["public"]["workspace_info"]["id"],
            dict_context["public"]["workspace_info"]["name"],
            time.time() - start_time,
        )

        result, dict_context, logs = pipeline_class.process(dict_context)

        execution_context.public.flow = {**execution_context.public.flow, **dict_context.public.flow}
        execution_context.public.workspace = {
            **execution_context.public.workspace,
            **dict_context.public.workspace,
        }

        pipeline_context["extra"] = {"extra_logs": {"trace": {"flows": logs["workspace"]["flows"]}}}
        execution_context.public.response = result

        return (execution_context, pipeline_context)
