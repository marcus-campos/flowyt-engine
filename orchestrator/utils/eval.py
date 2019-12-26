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
    source = source.replace('${', '')[:-1]
    result = None
    
    try:
        result = eval(source, {
            'env': env,
            'flow': flow,
            'request': request,
            'session': session,
            'workspace': workspace,
            'function': function,
            'response': response
        })
    except SyntaxError:
        pass

    if type(result) is not str:
        result = 'null'

    return result