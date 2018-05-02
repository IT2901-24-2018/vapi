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


def line_to_linestring_distance(line, search_radius):
    """
    Returns closest segment and distance.
    Uses built in postgis functions to find the distance in meters between
    a line (input) and all the segments in the database. Then it returns
    the closest one or None if no segments within the MAX_MAPPING_DISTANCE.
    :param line: list with start and end points (lon/lat)
    :type line: list
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
            ST_SetSRID(ST_MakeLine(ST_MakePoint(%s, %s), ST_MakePoint(%s, %s)), 4326)::geography
          ) AS distance
          FROM api_roadsegment segment
        )
        SELECT id, distance
        FROM segment
        WHERE distance <= %s
        ORDER BY distance ASC
        LIMIT 1
        """
        cursor.execute(stmt, [line[0][0], line[0][1], line[1][0], line[1][1], search_radius])
        row = cursor.fetchone()

    if row is not None:
        return {"id": row[0], "distance": row[1]}
    else:
        return None


def closest_point_on_linestring(points, segment):
    """
    Finds the closest point on the segment from point
    :param points: List of one or two lon/lat points
    :type points: list
    :param segment: The id of a segment
    :type segment: int
    :return: List of the closest start and end points on the segment
    :rtype: list
    """
    return_points = []
    for point in points:
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
            return_points.append(cursor.fetchone()[0])

    return return_points


def map_to_segment(production_data):
    """
    Maps production data to road segments.
    Returns the prod-data dicts that mapped to a segment with the db id of the segment
    :param production_data: List of dicts that include a startlong and startlat attribute
    :type production_data: list
    :return: Mapped prod-data
    :rtype: list
    """

    mapped_data = []

    for prod_data in production_data:

        if "endlat" in prod_data and "endlong" in prod_data:
            line = [(prod_data["startlong"], prod_data["startlat"]), (prod_data["endlong"], prod_data["endlat"])]
            segment = line_to_linestring_distance(line, MAX_MAPPING_DISTANCE)
        else:
            segment = point_to_linestring_distance(
                (prod_data["startlong"], prod_data["startlat"]), MAX_MAPPING_DISTANCE
            )

        if segment is not None:

            if "endlat" in prod_data and "endlong" in prod_data:
                mapped_points = closest_point_on_linestring(
                    [(prod_data["startlong"], prod_data["startlat"]), (prod_data["endlong"], prod_data["endlat"])],
                    segment["id"]
                )
            else:
                mapped_points = closest_point_on_linestring(
                    [(prod_data["startlong"], prod_data["startlat"])], segment["id"]
                )

            prod_data["segment"] = segment["id"]
            prod_data["start_point"] = mapped_points[0]
            if len(mapped_points) > 1:
                prod_data["end_point"] = mapped_points[1]
            mapped_data.append(prod_data)

    return mapped_data
