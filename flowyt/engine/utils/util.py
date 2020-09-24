def can_cast(val, to_type):
    try:
        return to_type(val)
    except:
        return False