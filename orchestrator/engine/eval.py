import json
import time
import js2py

from dotmap import DotMap

def __run_python(source, run_context):
    try:
        result = eval(
            "{0}".format(source),
            run_context,
            {"json": json},
        )
    except SyntaxError:
        pass

    return result

def __run_javascript(source, run_context):
    try:
        wrapper = """
            const result = {0}
        """.format(source)
        context = js2py.EvalJs(run_context, enable_require=False)
        context.execute(wrapper)

        if type(context.result) is js2py.base.JsObjectWrapper:
            result = context.result.to_list()
            if not result:
                result = context.result.to_dict()

    except Exception:
        pass

    return result


def contexted_run(context, source, language):
    env = context.public.env
    flow = context.public.flow
    request = context.public.request
    session = context.public.session
    workspace = context.public.workspace
    workspace_info = context.public.workspace_info
    function = context.public.function
    response = context.public.response

    # Remove ${} from string
    source = source.replace("${", "")[:-1]
    source = source.replace("$(py){", "")
    source = source.replace("$(js){", "")
    result = None

    run_context = {
        "env": env,
        "flow": flow,
        "request": request,
        "session": session,
        "workspace": workspace,
        "function": function,
        "response": response,
        "workspace_info": workspace_info,
    }

    if language == "python":
        result = __run_python(source, run_context)

    if language == "javascript":
        result = __run_javascript(source, run_context)

    return result


def contexted_run_pipeline(context, source):
    pipeline = context

    # Remove ${} from string
    source = source.replace("${", "")[:-1]
    result = None

    try:
        result = eval("str({0})".format(source), {"pipeline": pipeline})
    except SyntaxError:
        pass

    if type(result) is not str:
        result = "null"

    return result
