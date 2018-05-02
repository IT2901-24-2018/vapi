from api.models import RoadSegment


def map_weather_to_segment(weather_data):
    # Todo Map the weather to every segment.
    # Check if exisiting weather exists and add total value if needed
    segments = get_segments()


    return


def get_segments(municipality):
    matched_segments = RoadSegment.objects.filter(municipality=municipality)
    return matched_segments
