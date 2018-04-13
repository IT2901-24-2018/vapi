from backend.settings.constants import MAX_MAPPING_DISTANCE
from django.db import connection


def point_to_linestring_distance(point):
    """
    Returns closest segment and distance.
    :param point: lon lat
    :type point: tuple
    :return:
    :rtype: dict
    """
    with connection.cursor() as cursor:
        stmt = '''
        WITH segment (id, distance) 
        AS
        -- Find distance to segment and id
        (
          SELECT S.id AS id, 
          ST_Distance(S.the_geom::geography, 
          ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance 
          FROM api_roadsegment S
        ) 
        SELECT id, distance 
        FROM segment 
        WHERE distance <= %s 
        ORDER BY distance ASC 
        LIMIT 1
        '''
        cursor.execute(stmt, [point[0], point[1], MAX_MAPPING_DISTANCE])
        row = cursor.fetchone()

    if row:
        return {"id": row[0], "distance": row[1]}
    else:
        return None


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

        # Only do if segment is not None
        if segment:
            prod_data["segment"] = segment["id"]
            mapped_data.append(prod_data)

    return mapped_data


def delete_old_production_data(time):
    """
    Delete prod-data that is older than input
    :param time:
    """
    pass


def main():
    prod_data = [{'startlat': 63.387691997704202, 'startlong': 10.3290819995141, 'time': '2016-11-04T08:45:15'}]

    mapped_prod_data = map_to_segment(prod_data)
    if len(mapped_prod_data) > 0:
        print("id: {}".format(mapped_prod_data[0]["segment"]))
    else:
        print("No mapped data")


# if __name__ == '__main__':
#     pass
