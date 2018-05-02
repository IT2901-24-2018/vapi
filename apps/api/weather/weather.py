from api.models import RoadSegment, WeatherData


def map_weather_to_segment(weather_data):
    # Todo Map the weather to every segment.
    # Check if exisiting weather exists and add total value if needed
    # Create PUT request for data that should be updated instead of created
    for weather in weather_data:
        mun_segments = get_segments(weather['county_and_municipality_id'])
        weather_for_mun = get_weather_for_mun(weather['county_and_municipality_id'])
        print("In weather")
        for road_id in mun_segments:
            for entry in weather_for_mun:
                print("We're checking")
                if road_id == entry['segment_id']:
                    #update
                    print(road_id)
                #Create new 


    return weather_data


def get_segments(municipality):
    queryset = RoadSegment.objects.filter(municipality=municipality).values('id')
    matched_segments = list(queryset)
    return matched_segments

def get_weather_for_mun(municipality):
    queryset = WeatherData.objects.filter(county_and_municipality_id=municipality).values()
    matched_weather = list(queryset)
    return matched_weather
