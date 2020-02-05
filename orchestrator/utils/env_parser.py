from orchestrator.settings import ENV_PATH

def parser(): 
    with open(ENV_PATH, 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    return data
    
def save(data):
    file = open(ENV_PATH, 'w')
    file.writelines(data)
    return data

    