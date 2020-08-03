import copy


def remove_from_dict(data):
    new_data = copy.deepcopy(data)
    if new_data:
        del new_data[0]
    print(len(new_data))
    return new_data