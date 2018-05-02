from api.models import RoadSegment, WeatherData
from copy import deepcopy


def map_weather_to_segment(weather_data):
    # Todo Map the weather to every segment.
    # Check if exisiting weather exists and add total value if needed
    # Create PUT request for data that should be updated instead of created

    mapped_weather = []

    for weather in weather_data:
        mun_segments = get_segments(weather['county_and_municipality_id'])
        weather_for_mun = get_weather_for_mun(weather['county_and_municipality_id'])
        for segment_id in mun_segments:
            has_weather = False
            for entry in weather_for_mun:
                if segment_id == entry['segment_id']:
                    #update
                    has_weather = True
            if not has_weather:
                copy_weather = deepcopy(weather)
                copy_weather['segment'] = segment_id
                mapped_weather.append(copy_weather)
    print(mapped_weather)
    return weather_data


def get_segments(municipality):
    queryset = RoadSegment.objects.filter(municipality=municipality).values('id')
    matched_segments = list(queryset)
    return matched_segments

def get_weather_for_mun(municipality):
    queryset = WeatherData.objects.filter(county_and_municipality_id=municipality).values()
    matched_weather = list(queryset)
    return matched_weather
