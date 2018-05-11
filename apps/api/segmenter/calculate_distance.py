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


def utm_to_latlon(start_point, end_point, zone1, zone2):
    """
    Converts from UTM to latlong
    :param start_point: the first GPS point given in UTM list form [x, y]
    :param end_point: the second GPS point given in UTM list form [x, y]
    :param zone1: the number of the zone, from 0 to 66 or something
    :param zone2: the letter for the zone, from a to z
    :return: two latlong points in list form [[start_lat, start_long], [end_lat, end_long]]
    """
    start = utm.to_latlon(start_point[0], start_point[1], zone1, zone2)
    end = utm.to_latlon(end_point[0], end_point[1], zone1, zone2)

    return [start[0], start[1]], [end[0], end[1]]


def calculate_road_length(point_list, max_length_meter):
    """
    Calculate the length of a road given a list of point points
    :param point_list: A 2d list of point points given in UTM format
    :param max_length_meter: Maximum length of the road segment
    :return: returns the index of the point_point, and total length of the road in meters
    """
    length = 0
    for i in range(1, len(point_list)):
        prev = i - 1
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
