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
                "lambda": {
                    "test": Test()
                }
            },
            "private": {
                "integrations": self.workspace_class.integrations
            }
        }

        while process_pipeline:
            flow_class = Flow(self.workspace, start_flow)
            context["public"]["flow"] = flow_class.vars

            actions = flow_class.pipeline
            
            has_actions = True
            while has_actions:
                action = actions.next_action()

                if not action:
                    has_actions = False
                    return

                context = action.action.start(context)
                
                
                
            process_pipeline = False

            

class Test():
    def run(name):
        return name