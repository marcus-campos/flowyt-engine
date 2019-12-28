from dotmap import DotMap
from apps.workspace.workspace import Workspace
from apps.workspace.flows.flow import Flow
from apps.workspace.functions import Functions


class Pipeline:
    def __init__(self, workspace, flow):
        self.flow = flow
        self.workspace = workspace
        self.workspace_class = Workspace(self.workspace)
        self.functions_class = Functions(self.workspace)

    def start(self, request_data):
        # Config pipeline
        start_flow = self.flow
        context = {
            "public": {
                "workspace": {
                    "id": self.workspace_class.id,
                    "name": self.workspace_class.name,
                    "release": self.workspace_class.release,
                },
                "env": self.workspace_class.env,
                "session": {},
                "request": request_data,
                "function": self.functions_class.workspace_functions,
                "response": {},
            },
            "private": {"integrations": self.workspace_class.integrations},
            "pipeline_context": {},
        }

        # While proccess vars
        process_pipeline = True
        pipeline_response = {}
        while process_pipeline:
            # Load flow
            flow_class = Flow(self.workspace, start_flow)
            # Get action
            actions = flow_class.pipeline

            # While proccess vars
            has_actions = True
            action_response = {}
            while has_actions:
                # Context vars
                context["public"]["flow"] = flow_class.vars
                context["public"]["response"] = action_response
                context = DotMap(context)

                # Get next action
                action = actions.next_action(context.pipeline_context)
                if not action:
                    has_actions = False
                    # TODO: if next_flow not empty change start_flow
                    process_pipeline = False
                    return

                # Execute action
                context = action.action.start(context)

                # Add flow vars
                flow_class.vars = context.public.flow

                # Remove action response if exists
                if action_response == context.public.response:
                    action_response = {}
                    context.public.response = {}
                else:
                    action_response = context.public.response

                # Stop pipeline if get response
                if context.pipeline_context.get("response"):
                    process_pipeline = False
                    has_actions = False
                    pipeline_response = context.pipeline_context.get("response")

        return pipeline_response
