import copy


def remove_from_dict(data):
    new_data = copy.deepcopy(data)
    if new_data:
        del new_data[0]
    return new_data

def test_async():
     print("Passou aqui 123")
