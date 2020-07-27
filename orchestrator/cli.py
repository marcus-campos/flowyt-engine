import argparse
import json

from engine.manager import Engine
from utils.splash import loading
from apps.api.services.workspace_load import WorkspaceLoad
from pygments import highlight, lexers, formatters


engine_class = Engine()

if __name__ == "__main__":
    loading()

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workspace", help="Indicates the name of the workspace")
    parser.add_argument("-f", "--flow", help="Indicates the name of the flow")
    parser.add_argument("-i", "--input", help="Indicates input to be used in workspace")
    parser.add_argument("-d", "--debug", help="Indicates whether to display debug data")
    args = parser.parse_args()

    if args.workspace and args.flow:
        workspace_data = WorkspaceLoad().load(args.workspace.strip())
        result = None
        debug = "false"

        if args.debug:
            debug = args.debug.strip()

        if args.input:
            result = engine_class.start(
                workspace_data, {}, {**args.input, "debug": debug}, args.workspace.strip(), args.flow.strip()
            )
        else:
            result = engine_class.start(
                workspace_data, {}, {"debug": debug}, args.workspace.strip(), args.flow.strip()
            )

        if result:
            if debug == "false":
                del result["__debug__"]
                del result["exception"]

            result = json.dumps(result, indent=2)
            colorful_json = highlight(result, lexers.JsonLexer(), formatters.TerminalFormatter())
            print(colorful_json)
