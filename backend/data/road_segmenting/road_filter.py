# Circular imports suck
def remove_keys(road):
    """
    :param road: A road segment as a dict
    :return: The same road segment without "felt" and "kvalitet".
    """
    road.pop("felt", None)
    road['geometri'].pop("kvalitet", None)
    return road
