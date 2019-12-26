from dotmap import DotMap
from apps.workspace.workspace import Workspace
from apps.workspace.flows.flow import Flow


class Pipeline():

    def __init__(self, workspace, flow):
        self.flow = flow
        self.workspace = workspace

        self.workspace_class = Workspace(self.workspace)      

    def start(self, request_data):
        start_flow = self.flow
        process_pipeline = True
        context = {
            "public": {
                "workspace": {
                    "id": self.workspace_class.id,
                    "name": self.workspace_class.name,
                    "release": self.workspace_class.release
                },
                "env": self.workspace_class.env,
                "session": {},
                "request": request_data,
                "function": {
                    "test": run
                },
                "response": {}
            },
            "private": {
                "integrations": self.workspace_class.integrations
            },
            "pipeline_context": {}
        }

        while process_pipeline:
            flow_class = Flow(self.workspace, start_flow)
            actions = flow_class.pipeline
            
            has_actions = True
            action_response = {}
            while has_actions:
                context["public"]["flow"] = flow_class.vars
                context["public"]["response"] = action_response
                context = DotMap(context)
                
                action = actions.next_action()
                if not action:
                    has_actions = False
                    return

                context = action.action.start(context)

                flow_class.vars = context.public.flow
                
                action_response = context.public.input
                context.public.input = {}
                
            process_pipeline = False

            


def run(name):
    return name