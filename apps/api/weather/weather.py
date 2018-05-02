from api.models import RoadSegment


def map_weather_to_segment(weather_data):
    # Todo Map the weather to every segment.
    # Check if exisiting weather exists and add total value if needed
    for weather in weather_data:
        mun_segments = get_segments(weather['county_and_municipality_id'])
        for road in mun_segments:
            print("Do something")
    return weather_data


def get_segments(municipality):
    queryset = RoadSegment.objects.filter(municipality=municipality).values('id')
    matched_segments = list(queryset)
    return matched_segments
