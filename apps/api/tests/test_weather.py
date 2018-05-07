from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from rest_framework.test import APITestCase

from api.models import RoadSegment, WeatherData, ProductionData
from api.weather import weather

# docker-compose run --rm django  py.test apps/api/tests/test_weather.py
# check if more than one weather for each segment
# put in rain, check if there is weather
# update rain, check if it was updated
# update temperature, check if it is updated


class InsertOneWeatherDataTest(APITestCase):
    """
    Test weather data model.
    """
    def setUp(self):
        linestring = GEOSGeometry(
            'LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327,'
            '266876 7037333,266916 7037334,266955 7037332,267032 7037323,267127 7037314,267174 7037300,267181 7037296,'
            '267185 7037296,267191 7037300)', 32633
        )
        RoadSegment.objects.create(
            the_geom=linestring, county=5001, href=1, category=1, municipality=5001, startdate='2018-1-1', region=1,
            stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
        )
        segment = RoadSegment.objects.get()

        WeatherData.objects.create(
            start_time_period=timezone.now(), end_time_period=timezone.now() + timezone.timedelta(days=1), county_and_municipality_id=5001, value=2, unit="mm", degrees="30", segment=segment
        )


    def test_prod_data(self):
        """
        Check that there is one and only one item in prod-data table
        """
        self.assertEqual(WeatherData.objects.count(), 1)

    def test_for_precipitation(self):
        """
        Check that there is precipitation in the weather data
        """
        entry = WeatherData.objects.get()
        self.assertEqual(entry.value, 2)

    def test_for_temperature(self):
        """
        Check that there is temperature in the weather data
        """
        entry = WeatherData.objects.get()
        self.assertEqual(entry.degrees, 30)

    def test_for_correct_segment(self):
        """
        Check that the road segment has the correct weather data
        """
        segment = RoadSegment.objects.get()
        weather = WeatherData.objects.get()
        self.assertEqual(segment.id, weather.segment.id)

    def test_for_updated_value(self):
        entry = WeatherData.objects.get()
        self.assertEqual(entry.value, 2)
        weather.map_weather_to_segment([{"start_time_period": '2018-12-10T08:45:15Z',"end_time_period": '2018-12-11T08:45:15Z', "county_and_municipality_id": 5001,
                                         "value": 4, "unit": 'mm',"degrees": 30, "segment": 4}])
        entry2 = WeatherData.objects.get()
        self.assertEqual(entry2.value, 6)


    def test_for_existing_production_data(self):
        """
        Check that if there is already production data within weather time delta, do not apply weather data
        """
        entry=WeatherData.objects.get()
        self.assertEqual(entry.value, 2)
        ProductionData.objects.create(
            time=timezone.now(), startlat=64.3870750023729, startlong=64.3870750023729, endlat=64.3870750023729,
            endlong=64.3870750023729, dry_spreader_active=True,
            plow_active=True, wet_spreader_active=True, brush_active=True, material_type_code=True,
            segment=RoadSegment.objects.get()
        )
        weather.map_weather_to_segment([{"start_time_period": '2018-12-10T08:45:15Z',
                                         "end_time_period": '2018-12-11T08:45:15Z', "county_and_municipality_id": 5001,
                                         "value": 4, "unit": 'mm', "degrees": 30, "segment": 4}])
        entry = WeatherData.objects.get()
        self.assertEqual(entry.value, 2)


    def test_for_existing_weather_data(self):
        """
        Check that when you input production data, if there is already weather, reset the weather precipitation and
        update the start time period for the weather.
        """
        ProductionData.objects.create(
            time=timezone.now(), startlat=64.3870750023729, startlong=64.3870750023729, endlat=64.3870750023729,
            endlong=64.3870750023729, dry_spreader_active=True,
            plow_active=True, wet_spreader_active=True, brush_active=True, material_type_code=True,
            segment=RoadSegment.objects.get()
        )


# class InsertMultiWeatherDataTest(APITestCase):
#
