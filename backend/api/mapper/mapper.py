import utm
from backend.settings.constants import MAX_MAPPING_DISTANCE
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

from api.models import DummyModel


def point_to_linestring_distance(point):
    """
    Returns closest segment and distance.
    :param point: lon lat
    :type point: tuple
    :return:
    :rtype: dict
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT S.id, "
                       "ST_Distance(S.the_geom::geography, "
                       "ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance "
                       "FROM api_dummymodel S "
                       "ORDER BY distance ASC "
                       "LIMIT 1", [point[0], point[1]])
        row = cursor.fetchone()

    return {"id": row[0], "distance": row[1]}


def map_to_segment(production_data):
    """
    Maps production data to road segments
    :param production_data:
    :type production_data: list
    :return:
    :rtype: list
    """

    mapped_data = []

    for prod_data in production_data:

        point = (prod_data["startlong"], prod_data["startlat"])
        segment = point_to_linestring_distance(point)

        if segment["distance"] <= MAX_MAPPING_DISTANCE:
            prod_data["segment"] = segment["id"]
            mapped_data.append(prod_data)

    return mapped_data


def main():
    prod_data = [{'startlat': 63.387691997704202, 'endlat': 63.3874419990294, 'endlong': 10.3290930003037,
                  'startlong': 10.3290819995141, 'time': '2016-11-04T08:45:15'}]

    mapped_prod_data = map_to_segment(prod_data)
    if len(mapped_prod_data) > 0:
        print("id: {}".format(mapped_prod_data[0]["roadsegment"]))
    else:
        print("No mapped data")


def save_dummy_segment(linestring, srid):
    """
    Save segment geo data.
    :param linestring:
    :param srid:
    :return:
    """
    if srid is not None:
        linestring = GEOSGeometry(linestring, srid=srid)
    else:
        linestring = GEOSGeometry(linestring)
    d = DummyModel(the_geom=linestring)
    d.save()


def utm_to_lonlat(utm_point, zone1, zone2):
    """
    Converts a geometrical point from utm to lon/lat
    :param utm_point:
    :param zone1:
    :param zone2:
    :return lonlat:
    """
    lat_lon = utm.to_latlon(utm_point[0], utm_point[1], zone1, zone2)
    return lat_lon[0], lat_lon[1]


def utm_linestring_to_lonlat_linetring(utm_coordinates, zone1, zone2):
    """
    Converts linestring from utm to lon/lat
    :param utm_coordinates: 2d array
    :param zone1:
    :type zone1: int
    :param zone2:
    :type zone2: basestring
    :return: lon/lat linestring
    :rtype: basestring
    """
    linestring = 'LINESTRING('
    for c in utm_coordinates:
        lonlat = utm_to_lonlat(c, zone1, zone2)
        linestring += '{0} {1},'.format(str(lonlat[0]), str(lonlat[1]))
    linestring = linestring.rstrip(',')
    linestring += ')'
    return linestring


if __name__ == '__main__':
    pass
