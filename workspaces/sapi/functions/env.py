import os

def get():
    return {
        "base_url": os.environ['BASE_URL'],
        "client_id": os.environ['CLIENT_ID'],
        "client_secret": os.environ['CLIENT_SECRET'],
        "client_username": os.environ['CLIENT_USERNAME'],
        "client_password": os.environ['CLIENT_PASSWORD']
    }