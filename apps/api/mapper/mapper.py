from django.db import connection
from vapi.constants import MAX_MAPPING_DISTANCE


def point_to_linestring_distance(point, search_radius):
    """
    Returns closest segment and distance.
    Uses built in postgis functions to find the distance in meters between
    a point (input) and all the segments in the database. Then it returns
    the closest one or None if no segments within the MAX_MAPPING_DISTANCE.
    :param point: lon lat
    :type point: tuple
    :param search_radius: Max distance to segment
    :type search_radius: int
    :return: Segment id and distance to it
    :rtype: dict
    """
    with connection.cursor() as cursor:
        stmt = """
        WITH segment (id, distance)
        AS
        -- Find distance to segment and id
        (
          SELECT segment.id AS id,
          ST_Distance(
            segment.the_geom::geography,
            -- Make a point with srid 4326 since the point is lon lat
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
          ) AS distance
          FROM api_roadsegment segment
        )
        SELECT id, distance
        FROM segment
        WHERE distance <= %s
        ORDER BY distance ASC
        LIMIT 1
        """
        cursor.execute(stmt, [point[0], point[1], search_radius])
        row = cursor.fetchone()

    if row is not None:
        return {"id": row[0], "distance": row[1]}
    else:
        return None


def closest_point_on_linestring(point, segment):
    """
    Finds the closest point on the segment from point
    :param point: lon/lat
    :type point: tuple
    :param segment: The id of a segment
    :type segment: int
    :return: The closest point on the segment
    :rtype: string
    """
    with connection.cursor() as cursor:
        stmt = """
        WITH prod
        AS
        (
          SELECT ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geometry AS point
        )
        SELECT ST_AsText(ST_ClosestPoint(segment.the_geom, prod.point))
        FROM api_roadsegment AS segment, prod
        WHERE id = %s
        """
        cursor.execute(stmt, [point[0], point[1], segment])
        row = cursor.fetchone()

    return row[0]


def map_to_segment(production_data):
    """
    Maps production data to road segments.
    Returns the prod-data dicts that mapped to a segment with the db id of the segment
    :param production_data: List of dicts that include a startlon and startlat
    :type production_data: list
    :return: Mapped prod-data
    :rtype: list
    """

    mapped_data = []

    for prod_data in production_data:

        point = (prod_data["startlong"], prod_data["startlat"])
        segment = point_to_linestring_distance(point, MAX_MAPPING_DISTANCE)

        # Only do if segment is not None
        if segment is not None:

            mapped_point = closest_point_on_linestring(point, segment["id"])

            prod_data["segment"] = segment["id"]
            prod_data["closest_point"] = mapped_point
            mapped_data.append(prod_data)

    return mapped_data



