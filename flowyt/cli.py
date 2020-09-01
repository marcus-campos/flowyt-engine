import argparse
import json
import time

from engine.manager import Engine
from pygments import formatters, highlight, lexers

from apps.api.services.workspace_load import WorkspaceLoad
from utils.splash import loading

engine_class = Engine()

if __name__ == "__main__":
    loading()
    print("Running...")

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
            debug = "true" if args.debug.strip() != "false" else "false"

        if args.input:
            args_data = json.loads(args.input)
            result = engine_class.start(
                workspace_data, {}, {**args_data, "debug": debug}, args.workspace.strip(), args.flow.strip()
            )
        else:
            result = engine_class.start(
                workspace_data, {}, {"debug": debug}, args.workspace.strip(), args.flow.strip()
            )

        if result:
            if debug == "false":
                del result["__debug__"]
                if "exception" in result:
                    del result["exception"]

            if args.debug.strip() == "simplified":
                for flow in range(len(result["__debug__"]["workspace"]["flows"])):
                    for action in range(len(result["__debug__"]["workspace"]["flows"][flow]["actions"])):
                        del result["__debug__"]["workspace"]["flows"][flow]["actions"][action]["data"]

            result = json.dumps(
                result, indent=2, default=lambda o: f"<non-serializable: {type(o).__qualname__}>"
            )
            colorful_json = highlight(result, lexers.JsonLexer(), formatters.TerminalFormatter())
            print("")
            print(colorful_json)
