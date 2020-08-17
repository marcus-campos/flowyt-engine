import copy
from datetime import datetime, timezone

import pytz


def remove_from_dict(data):
    new_data = copy.deepcopy(data)
    if new_data:
        del new_data[0]
    return new_data


def add_sys_date(data):
    new_data = copy.deepcopy(data)
    dt = datetime.now(pytz.timezone("America/Sao_Paulo"))
    new_data["sys_created_at"] = dt
    return new_data
