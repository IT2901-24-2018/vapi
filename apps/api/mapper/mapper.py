from django.db import connection
from vapi.constants import MAX_MAPPING_DISTANCE


def get_candidates(sequence, search_radius):
    """
    Returns closest segment and distance.
    Uses built in postgis functions to find the distance in meters between
    a line (input) and all the segments in the database. Then it returns
    the closest one or None if no segments within the MAX_MAPPING_DISTANCE.
    :param sequence: list with start and end points (lon/lat)
    :type sequence: list[dict]
    :param search_radius: Max distance to segment
    :type search_radius: int
    :return: Segment id and distance to it
    :rtype: dict
    """
    with connection.cursor() as cursor:
        params = []
        for i in range(len(sequence)):
            params.extend([i,
                           sequence[i]["startlong"], sequence[i]["startlat"],
                           sequence[i]["endlong"], sequence[i]["endlat"]])

        placeholder = ", ".join("(%s, %s, %s, %s, %s)" for _ in range(len(sequence)))

        stmt = """
        WITH sequence (lid, slon, slat, elon, elat) AS (VALUES {placeholder}),
        line AS
        (
          SELECT *, (ST_SetSRID(ST_MakeLine(
            ST_MakePoint(slon, slat), ST_MakePoint(elon, elat)
          ), 4326)::geography) AS line,
          ST_SetSRID(ST_MakePoint(slon, slat), 4326)::geography AS spoint,
          ST_SetSRID(ST_MakePoint(elon, elat), 4326)::geography AS epoint
          FROM sequence
        )
        
        SELECT line.lid AS lid, segment.id AS sid,
        -- Test (Remove this)
        segment.county AS testid,
        -- Test end
        (
        -- Find distance to segment
          SELECT ST_Distance(
            segment.the_geom::geography,
            line.line
          ) AS distance
        ),
        -- Map start point to closest point on segment
        (SELECT ST_AsText(ST_ClosestPoint(
          segment.the_geom, ST_SetSRID(ST_MakePoint(line.slon, line.slat), 4326))) AS start_mapped_point
        ),
        -- Map end point to closest point on segment
        (SELECT ST_AsText(ST_ClosestPoint(
          segment.the_geom, ST_SetSRID(ST_MakePoint(line.elon, line.elat), 4326))) AS end_mapped_point
        ),
        -- Find distance between start point and end point
        (SELECT ST_Distance(line.spoint, line.epoint)) AS distance_between_start_end,
        -- Find distance between the remapped start and end points
        (SELECT ST_Distance(
          ST_ClosestPoint(segment.the_geom, ST_SetSRID(ST_MakePoint(line.slon, line.slat), 4326))::geography,
          ST_ClosestPoint(segment.the_geom, ST_SetSRID(ST_MakePoint(line.elon, line.elat), 4326))::geography
        )) AS distance_on_segment
        FROM api_roadsegment AS segment, line
        WHERE ST_DWithin(line.line, segment.the_geom::geography, %s)
        ORDER BY lid ASC, distance ASC
        """.format(placeholder=placeholder)

        # Add search_radius to parameters
        params.append(search_radius)
        cursor.execute(stmt, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def map_to_segment(production_data):
    """
    Maps production data to road segments.
    Returns the prod-data dicts that mapped to a segment with the db id of the segment
    :param production_data: List of dicts that include a startlong and startlat attribute
    :type production_data: list[dict]
    :return: Mapped prod-data
    :rtype: list
    """

    candidates = get_candidates(production_data, MAX_MAPPING_DISTANCE)

    mapped_data = []

    # Check for each prod-data id what segment is best
    # Criteria is the closest distance and most similar distance_between_start_end and distance_on_segment

    for candidate in candidates:

        # Check what segment to map to



        if True:

            production_data[int(candidate["lid"])]["segment"] = candidate["sid"]
            production_data[int(candidate["lid"])]["start_point"] = candidate["start_mapped_point"]
            production_data[int(candidate["lid"])]["end_point"] = candidate["end_mapped_point"]
            mapped_data.append(production_data[int(candidate["lid"])])

    return mapped_data
