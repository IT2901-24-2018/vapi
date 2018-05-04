from api.models import RoadSegment, WeatherData
from django.db.models import F
from copy import deepcopy


def map_weather_to_segment(weather_data):
    print(weather_data)
    number_of_updated_weather = 0
    mapped_weather = []
    print("funcion run")
    for weather in weather_data:
        mun_segments = get_segments(weather['county_and_municipality_id'])
        weather_for_mun = get_weather_for_mun(weather['county_and_municipality_id'])
        print("before loop")
        for segment_id in mun_segments:
            print("it came this far")
            has_weather = False
            for entry in weather_for_mun:
                if segment_id['id'] == entry['segment_id']:
                    has_weather = True
                    number_of_updated_weather += 1
                    print("it was same")
                    update_weather_data(weather, segment_id['id'])
            if not has_weather:
                print('it was not same')
                copy_weather = deepcopy(weather)
                copy_weather['segment'] = segment_id['id']
                mapped_weather.append(copy_weather)
    return number_of_updated_weather, mapped_weather


def update_weather_data(inserted_weather, segment_id):
    print("tried to pudate")
    weather = WeatherData.objects.get(segment=segment_id)
    weather.value = F('value') + inserted_weather['value']
    weather.degrees = inserted_weather['degrees']
    weather.save(update_fields=['value', 'degrees'])


def get_segments(municipality):
    queryset = RoadSegment.objects.filter(municipality=municipality).values('id')
    matched_segments = list(queryset)
    return matched_segments

def get_weather_for_mun(municipality):
    queryset = WeatherData.objects.filter(county_and_municipality_id=municipality).values()
    matched_weather = list(queryset)
    return matched_weather
