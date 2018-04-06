import numpy as np
from math import pow
from api.models import DummyModel
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

# To functions for finding the distance from a point to a line.
# None of them use a reasonable measure for distance.

# TODO: look into PostGIS ST_Distance


def point_to_line_distance(point, line):
    """
    https://stackoverflow.com/questions/27161533/find-the-shortest-distance-between-a-point-and-line-segments-not-line

    Calculate the distance between a point and a line segment.

    To calculate the closest distance to a line segment, we first need to check
    if the point projects onto the line segment.  If it does, then we calculate
    the orthogonal distance from the point to the line.
    If the point does not project to the line segment, we calculate the
    distance to both endpoints and take the shortest distance.

    :param point: Numpy array of form [x,y], describing the point.
    :type point: numpy.array
    :param line: list of endpoint arrays of form [P1, P2]
    :type line: list of numpy.array
    :return: The minimum distance to a point.
    :rtype: float
    """
    # unit vector
    unit_line = line[1] - line[0]
    norm_unit_line = unit_line / np.linalg.norm(unit_line)

    diff = (
        (norm_unit_line[0] * (point[0] - line[0][0])) +
        (norm_unit_line[1] * (point[1] - line[0][1]))
    )

    x_seg = (norm_unit_line[0] * diff) + line[0][0]
    y_seg = (norm_unit_line[1] * diff) + line[0][1]

    # decide if the intersection point falls on the line segment
    lp1_x = line[0][0]  # line point 1 x
    lp1_y = line[0][1]  # line point 1 y
    lp2_x = line[1][0]  # line point 2 x
    lp2_y = line[1][1]  # line point 2 y
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
    if is_betw_x and is_betw_y:
        # compute the perpendicular distance to the theoretical infinite line
        segment_dist = (
            np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
            np.linalg.norm(unit_line)
        )
        return segment_dist
    else:
        # if not, then return the minimum distance to the segment endpoints
        endpoint_dist = min(
            np.linalg.norm(line[0] - point),
            np.linalg.norm(line[1] - point)
        )
        return endpoint_dist


# Not correct
def distance(p0, p1, p2):  # p0 is the point
    """
    https://stackoverflow.com/questions/27461634/calculate-distance-between-a-point-and-a-line-segment-in-latitude-and-longitude
    """
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    nom = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = pow((pow((y2 - y1), 2) + pow((x2 - x1), 2)), 0.5)
    result = nom / denominator
    return result


def save_dummy_segment():
    linestring = GEOSGeometry('LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327)')
    d = DummyModel(the_geom=linestring)
    d.save()





def point_to_linestring_distance():
    with connection.cursor() as cursor:
        point = GEOSGeometry('{"type": "Point", "coordinates": [63.3870750023729, 10.3277250005425]}')
        cursor.execute("SELECT ST_Distance(ST_GeomFromText(%s, 32633),"
                       "SELECT the_geom FROM api_dummymodels)", [point])
        row = cursor.fetchone()

    return row


if __name__ == '__main__':

    # p1 = np.array([63.387075002372903, 10.3277250005425])
    # p2 = np.array([63.387642998353499, 10.3282330021124])
    # p3 = np.array([63.387691997704202, 10.3290819995141])

    p1 = np.array([3, 3])
    p2 = np.array([3, 10])
    p3 = np.array([0, 0])

    # print(p3 - p1)

    # print(np.cross(p2 - p1, p3 - p1) / norm(p2 - p1))

    print(point_to_line_distance(p3, [p1, p2]))
    print(distance(p3, p1, p2))
