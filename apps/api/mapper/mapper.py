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
    :rtype: dict[list]
    """
    with connection.cursor() as cursor:
        # Make a list of query parameters with an id for each production data entry and the geometric data
        params = []
        for i in range(len(sequence)):
            params.extend([i,
                           sequence[i]["startlong"], sequence[i]["startlat"],
                           sequence[i]["endlong"], sequence[i]["endlat"]])

        # Makes '(%s, %s, %s, %s, %s)' separated by ', ' equal to the number of data in production data input
        placeholder = ", ".join("(%s, %s, %s, %s, %s)" for _ in range(len(sequence)))

        stmt = """
        /*
        Instead of executing one query for each production data entry
        we make a sequence that contains all the entries
         */
        WITH sequence (lid, slon, slat, elon, elat) AS (VALUES {placeholder}),
        -- Make a linestring representing the start and end point of an entry
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
        -- Only calculate the distances for the segments that are within search radius
        WHERE ST_DWithin(line.line, segment.the_geom::geography, %s)
        ORDER BY lid ASC, distance ASC
        """.format(placeholder=placeholder)

        # Add search_radius to parameters
        params.append(search_radius)
        cursor.execute(stmt, params)
        columns = [col[0] for col in cursor.description]
        list_rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        result = {}
        for row in list_rows:
            if row["lid"] not in result:
                result[row["lid"]] = []
            result[row["lid"]].append(row)
        return result


def prioritize_candidates(lines):
    """
    Use distance and the difference between distance_between_start_end and
    distance_on_segment to decide which segment is better
    Removes bad matches and set a score attribute to use for prioritizing
    :param lines: Dictionary with a list for each production data line
    :type lines: dict[list]
    :return:
    """
    for key in lines:
        key_list = []
        for candidate in lines[key]:
            # Prevent divide by zero just in case
            if candidate["distance_between_start_end"] != 0:
                candidate["distance_diff"] = (abs(candidate["distance_between_start_end"]
                                                  - candidate["distance_on_segment"])
                                              / candidate["distance_between_start_end"])

                # Remove candidate if it has about a 90 degree angle (+- 30 degrees) to line
                # 90 degrees = 1 if distance is 0
                # Works better if the line is short or the candidate segment is straight
                if not (0.67 < candidate["distance_diff"] < 1.33):
                    # Lower score is better
                    if candidate["distance"] < 5:
                        # If within 5 m look for the most parallel segment
                        # Prioritize by lowering distance_diff by 1 making it negative in most cases
                        candidate["score"] = candidate["distance_diff"] - 1
                    else:
                        candidate["score"] = (candidate["distance"]) * (candidate["distance_diff"])
                    key_list.append(candidate)

        # Sort lists based on score
        lines[key] = sorted(key_list, key=lambda x: x["score"])
    return lines


def map_to_segment(prod_data):
    """
    Maps production data to road segments.
    Returns the prod-data dicts that mapped to a segment with the db id of the segment
    :param prod_data: List of dicts that include a startlong and startlat attribute
    :type prod_data: list[dict]
    :return: Mapped prod-data
    :rtype: list
    """

    lines = get_candidates(prod_data, MAX_MAPPING_DISTANCE)

    prioritized = prioritize_candidates(lines)

    mapped_data = []

    # Map to the highest prioritized segment
    for key in prioritized:
        if len(prioritized[key]) > 0:
            prod_data[int(prioritized[key][0]["lid"])]["segment"] = prioritized[key][0]["sid"]
            prod_data[int(prioritized[key][0]["lid"])]["start_point"] = prioritized[key][0]["start_mapped_point"]
            prod_data[int(prioritized[key][0]["lid"])]["end_point"] = prioritized[key][0]["end_mapped_point"]
            mapped_data.append(prod_data[int(prioritized[key][0]["lid"])])

    return mapped_data
