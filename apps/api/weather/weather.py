from django.db import connection


def map_weather_to_segment(weather_data):
    # Todo Map the weather to every segment.
    # Check if exisiting weather exists and add total value if needed
    segments = get_segments(5001)


    return segments


def get_segments(municipality):
    with connection.cursor() as cursor:
        stmt = """
        SELECT * FROM api_roadsegment
        WHERE api_roadsegment.municipality=municipality
        """
        cursor.execute(stmt, municipality)
        data = cursor.fetchall()
    if data:
        return data
    else:
        return None


map_weather_to_segment(3)
