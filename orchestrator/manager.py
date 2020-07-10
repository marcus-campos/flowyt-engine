import argparse

from engine.manager import Engine
from utils.splash import loading
from apps.api.services.workspace_load import WorkspaceLoad


engine_class = Engine()

if __name__ == "__main__":
    loading()

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workspace", help="Indicates the name of the workspace")
    parser.add_argument("-f", "--flow", help="Indicates the name of the flow")
    parser.add_argument("-d", "--data", help="Indicates data to be used in workspace")
    args = parser.parse_args()
    
    if args.workspace and args.flow:
        workspace_data = WorkspaceLoad().load(args.workspace)
        
        if args.data:
            engine_class.start(workspace_data, {}, args.data, args.workspace, args.flow)
        else:
            engine_class.start(workspace_data, {}, {}, args.workspace, args.flow)