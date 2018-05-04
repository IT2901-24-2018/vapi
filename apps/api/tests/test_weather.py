from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from rest_framework.test import APITestCase

from api.models import RoadSegment, WeatherData

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
            the_geom=linestring, county=1, href=1, category=1, municipality=1, startdate='2018-1-1', region=1,
            stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
        )
        segmentID = RoadSegment.objects.get()

        WeatherData.objects.create(
            time=timezone.now(), county_and_municipality_id=5001, value=2, unit="mm", degrees="30", segment=segmentID
        )

    def test_prod_data(self):
        """
        Check that there is one and only one item in prod-data table
        """
        self.assertEqual(WeatherData.objects.count(), 1)

    def test_for_rain(self):
        entry = WeatherData.objects.get()
        self.assertEqual(entry.value, 2)

    def test_for_temperature(self):
        entry = WeatherData.objects.get()
        self.assertEqual(entry.degrees, 30)
