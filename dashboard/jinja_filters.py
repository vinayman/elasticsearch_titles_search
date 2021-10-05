def commify(number):
    return "{:,}".format(number)


def typed_value(value):
    if isinstance(value, list):
        return "; ".join(value)
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return value
