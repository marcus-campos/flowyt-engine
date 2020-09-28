def safe_cast(val, to_type):
    try:
        new_val = to_type(val)
        return new_val
    except:
        return False

def can_cast(val, to_type):
    return True if safe_cast(val, to_type) else False