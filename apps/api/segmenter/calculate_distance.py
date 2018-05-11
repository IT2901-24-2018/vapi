import math

import utm


def distance_formula(start_point, end_point):
    """
    Calculates the distance between two points using the distance formula
    :param start_point: the first GPS point, given in UTM list form [start_x, start_y]
    :param end_point:  the second GPS point, given in UTM list form [start_x, start_y]
    :return: The distance between the first GPS point and the second GPS point
    """
    distance = math.sqrt((start_point[0] - end_point[0])**2 + (start_point[1] - end_point[1])**2)
    return distance


def haversine_formula(start_point, end_point):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    :param start_point: the first GPS point, given in list form [start_lat, start_long]
    :param end_point: the second GPS point, given in list form [end_lat, end_long]
    :return: the distance between the first GPS point and the second GPS point, given in m
    """
    # convert decimal to radians
    earth_radius = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [start_point[0], start_point[1], end_point[0], end_point[1]])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)**2)
    c = 2 * math.asin(math.sqrt(a))
    return c * earth_radius


def utm_to_latlon(start_point, end_point, zone1, zone2):
    """
    Converts from UTM to latlong
    :param start_point: the first GPS point given in UTM list form [x, y]
    :param end_point: the second GPS point given in UTM list form [x, y]
    :param zone1: the number of the zone, from 0 to 66 or something
    :param zone2: the letter for the zone, from a to z
    :return: two latlong points in list form [[star_tlat, start_long], [end_lat, end_long]]
    """
    start = utm.to_latlon(start_point[0], start_point[1], zone1, zone2)
    end = utm.to_latlon(end_point[0], end_point[1], zone1, zone2)

    return [start[0], start[1]], [end[0], end[1]]


def calculate_road_length(point_list, max_length_meter, haversine):
    """
    Calculate the length of a road given a list of point points
    :param point_list: A 2d list of point points given in UTM format
    :param max_length_meter: Maximum length of the road segment
    :param haversine: True or False. Decides if the function uses the distance formula or the haversine formula
    :return: returns the index of the point_point, and total length of the road in meters
    """
    length = 0
    for i in range(1, len(point_list)):
        prev = i - 1
        if haversine:
            coordinates = utm_to_latlon(point_list[i], point_list[prev], 32, "V")
            length += haversine_formula(coordinates[0], coordinates[1])
        else:
            length += distance_formula(point_list[prev], point_list[i])
        if length >= max_length_meter:
            return i, math.ceil(length)
    return len(point_list)-1, round(length)


def calculate_road_length_simple(point_list):
    """
    Goes through a 2D list of coordinates points and returns the total stretchdistance
    :param point_list: A 2D list of coordinates with floats as values
    :return: The stretchdistance in int
    """
    length = 0
    for i in range(1, len(point_list)):
        prev = i - 1
        length += distance_formula(point_list[prev], point_list[i])
    return round(length)
