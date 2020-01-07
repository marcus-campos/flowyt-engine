import json
import time

from dotmap import DotMap


def contexted_run(context, source):
    env = context.public.env
    flow = context.public.flow
    request = context.public.request
    session = context.public.session
    workspace = context.public.workspace
    function = context.public.function
    response = context.public.response

    # Remove ${} from string
    source = source.replace("${", "")[:-1]
    result = None

    try:
        result = eval(
            "{0}".format(source),
            {
                "env": env,
                "flow": flow,
                "request": request,
                "session": session,
                "workspace": workspace,
                "function": function,
                "response": response,
            },
            {"json": json},
        )
    except SyntaxError:
        pass

    if type(result) in [int, float]:
        result = str(result)

    if type(result) is DotMap:
        aux_result = result.toDict()
        if type(aux_result) is dict and aux_result != {}:
            result = aux_result
    elif type(result) is list:
        new_result = []
        for item in result:
            if type(item) is DotMap:
                aux_result = item.toDict()
                if type(aux_result) is dict and aux_result != {}:
                    new_result.append(aux_result)
        result = new_result
    elif type(result) is not str:
        result = "null"

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
