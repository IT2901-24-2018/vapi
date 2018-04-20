from backend.settings.constants import MAX_MAPPING_DISTANCE
from django.db import connection


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
        stmt = '''
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
        '''
        cursor.execute(stmt, [point[0], point[1], search_radius])
        row = cursor.fetchone()

    if row:
        return {"id": row[0], "distance": row[1]}
    else:
        return None


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
            prod_data["segment"] = segment["id"]
            mapped_data.append(prod_data)

    return mapped_data


def find_newest_prod_on_segment(prod_data):
    """
    Finds the segment id and latest time connected to it
    :param prod_data: Mapped production data
    :return: dict of segments and the latest time they were handled
    """
    relevant_data = {}
    for data in prod_data:
        if data['segment'] not in relevant_data:
            relevant_data[str(data['segment'])] = data['time']
        elif relevant_data[str(data['segment'])] < data['time']:
            relevant_data[str(data['segment'])] = data['time']

    return relevant_data


def delete_old_production_data(prod_data):
    """
    Deletes obsolete production data after inserting new
    :param prod_data: Production data mapped to a segment
    :type prod_data: list
    :return: None
    """
    relevant_data = find_newest_prod_on_segment(prod_data)

