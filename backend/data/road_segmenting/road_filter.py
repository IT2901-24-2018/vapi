# Circular imports suck
def remove_keys(road):
    """
    :param road: A road segment as a dict
    :return: The same road segment without "felt" and "kvalitet".
    """
    road.pop("felt", None)
    road["geometri"].pop("kvalitet", None)
    return road


def remove_height(road_network):
    for road in road_network["features"]:
        for list_coordinates in road["geometry"]["coordinates"]:
            if len(list_coordinates) > 2:
                del list_coordinates[2]
    return road_network
