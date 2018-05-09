from copy import deepcopy

from django.db.models import F
from django.utils.dateparse import parse_datetime

from api.models import ProductionData, RoadSegment, WeatherData


def map_weather_to_segment(weather_data):
    """
    :param weather_data: List containing weather data as specified in models
    :return: number_of_updated_weather: The total number of weather objects that were updated
    :return: mapped_weather: List containing mapped weather linked to road segments
    """
    number_of_updated_weather = 0
    mapped_weather = []
    for weather in weather_data:
        mun_segments = get_segments(weather['county_and_municipality_id'])
        weather_for_mun = get_weather_for_mun(weather['county_and_municipality_id'])
        for segment_id in mun_segments:
            has_weather = False
            for entry in weather_for_mun:
                if segment_id['id'] == entry['segment_id']:
                    has_weather = True
                    number_of_updated_weather += 1
                    if not check_for_existing_data(entry):
                        update_weather_data(weather, segment_id['id'])
            if not has_weather:
                copy_weather = deepcopy(weather)
                copy_weather['segment'] = segment_id['id']
                mapped_weather.append(copy_weather)
    return number_of_updated_weather, mapped_weather


def check_for_existing_data(entry):
    """
    :param entry: JSON weather object
    :return: True or False if the same road segment has production data within the time range for the weather
    """
    start = entry['start_time_period']
    end = entry['end_time_period']
    segment_id = entry['segment_id']
    prod_data_list = ProductionData.objects.filter(segment=segment_id)
    for data in prod_data_list:
        return start <= data.time <= end
    return False


def handle_prod_weather_overlap(mapped_data):
    """
    :param mapped_data: A list containing the mapped json production data.
    :return: Nothing. Updated the weather associated with the road segment if true
    """
    # If prod data time corresponds to the 1 day weather in the database, zero the precipitation
    for prod_data in mapped_data:
        if 'plow_active' in prod_data or 'brush_active' in prod_data:
            if prod_data['plow_active'] or prod_data['brush_active']:
                if check_time_period(prod_data):
                    # Zero the precipitation
                    print("WE ARE IN BBY")
                    reset_precipitation(prod_data)


def reset_precipitation(prod_data):
    """
    :param prod_data: JSON production data object
    :return: Nothing. Updates the weather object associated with the common road segment
    """
    weather = WeatherData.objects.get(segment=prod_data['segment'])
    weather.start_time_period = prod_data['time']
    weather.value = 0
    weather.save(update_fields=['start_time_period', 'value'])


def check_time_period(prod_data):
    """
    :param prod_data: One production data JSON object
    :return: True if the prod data is between start and end time for weather object
    """
    weather_element = list(WeatherData.objects.filter(segment=prod_data['segment']).values('start_time_period',
                                                                                           'end_time_period'))
    if weather_element:
        start_weather_time = weather_element[0]['start_time_period']
        end_weather_time = weather_element[0]['end_time_period']
        parsed_weather = parse_datetime(prod_data['time'])
        return start_weather_time <= parsed_weather <= end_weather_time
    return False


def update_weather_data(inserted_weather, segment_id):
    """
    :param inserted_weather: User entered weather as JSON
    :param segment_id: ID to road segment
    :return: Nothing. Updates connecting weather accordingly
    """
    weather = WeatherData.objects.get(segment=segment_id)
    weather.value = F('value') + inserted_weather['value']
    weather.degrees = inserted_weather['degrees']
    weather.end_time_period = inserted_weather['end_time_period']
    weather.save(update_fields=['value', 'degrees', 'end_time_period'])


def get_segments(municipality):
    """
    :param municipality: Municipality number
    :return: A list with all road segments with that municipality
    """
    queryset = RoadSegment.objects.filter(municipality=municipality).values('id')
    matched_segments = list(queryset)
    return matched_segments


def get_weather_for_mun(municipality):
    """
    :param municipality: Municipality number
    :return: A list with all weather objects with that municipality
    """
    queryset = WeatherData.objects.filter(county_and_municipality_id=municipality).values()
    matched_weather = list(queryset)
    return matched_weather
