import math

import utm


def distance_formula(start_list, end_list):
    """
    Calculates the distance between two points using the distance formula
    :param start_list: the first GPS point, given in UTM list form [start_x, start_y]
    :param end_list:  the second GPS point, given in UTM list form [start_x, start_y]
    :return: The distance between the first GPS point and the second GPS point
    """
    distance = math.sqrt(pow((start_list[0] - end_list[0]), 2) + pow((start_list[1] - end_list[1]), 2))
    return distance


def haversine_formula(start_list, end_list):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    :param start_list: the first GPS point, given in list form [start_lat, start_long]
    :param end_list: the second GPS point, given in list form [end_lat, end_long]
    :return: the distance between the first GPS point and the second GPS point, given in m
    """
    # convert decimal to radians
    earth_radius = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [start_list[0], start_list[1], end_list[0], end_list[1]])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin(dlon / 2), 2)
    c = 2 * math.asin(math.sqrt(a))
    return c * earth_radius


def utm_to_latlon(start_list, end_list, zone1, zone2):
    """
    Converts from UTM to latlong
    :param start_list: the first GPS point given in UTM list form [x, y]
    :param end_list: the second GPS point given in UTM list form [x, y]
    :param zone1: the number of the zone, from 0 to 66 or something
    :param zone2: the letter for the zone, from a to z
    :return: two latlong points in list form [[star_tlat, start_long], [end_lat, end_long]]
    """
    start = utm.to_latlon(start_list[0], start_list[1], zone1, zone2)
    end = utm.to_latlon(end_list[0], end_list[1], zone1, zone2)

    return [start[0], start[1]], [end[0], end[1]]


def calculate_road_length(gps_list, max_length_meter, haversine):
    """
    Calculate the length of a road given a list of gps points
    :param gps_list: A 2d list of gps points given in UTM format
    :param max_length_meter: Maximum length of the road segment
    :param haversine: True or False. Decides if the function uses the distance formula or the haversine formula
    :return: returns the index of the gps_point, and total length of the road in meters
    """

    length = 0
    index = 0
    for gps_point in gps_list:
        index += 1
        if gps_list.index(gps_point) > 0:
            prev = gps_list[gps_list.index(gps_point) - 1]
            if haversine:
                coordinates = utm_to_latlon(gps_point, prev, 32, 'V')
                length += haversine_formula(coordinates[0], coordinates[1])
            else:
                length += distance_formula(prev, gps_point)
            if length >= max_length_meter:
                return index, math.ceil(length)
    return index, math.ceil(length)
