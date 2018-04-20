from backend.settings.constants import MAX_MAPPING_DISTANCE
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
import datetime

from api.mapper import mapper
from api.models import ProductionData, RoadSegment
from api.serializers import ProductionDataSerializer


class InsertOneProductionDataTest(APITestCase):
    """
    Test ProductionData model.
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
        d = RoadSegment.objects.get()

        ProductionData.objects.create(
            time=timezone.now(), startlat=60.7758584, startlong=20.756444, endlat=60.45454, endlong=20.57575,
            plow_active=True, segment=d
        )

    def test_prod_data(self):
        """
        Check that there is one and only one item in prod-data table
        """
        self.assertEqual(ProductionData.objects.count(), 1)

    def test_boolean_fields(self):
        """
        Test the boolean fields
        """
        prod_data = ProductionData.objects.all()

        # run test on the different optional fields
        self.assertEqual(prod_data[0].plow_active, True)
        self.assertIsNone(prod_data[0].dry_spreader_active)
        self.assertIsNone(prod_data[0].wet_spreader_active)
        self.assertIsNone(prod_data[0].brush_active)
        self.assertIsNone(prod_data[0].material_type_code)


class GetAllProductionDataTest(APITestCase):
    """
    Test module for GET all prod data API
    """
    def setUp(self):
        # Set up users
        User.objects.create_user(username="normal_user", password="testpassword")
        User.objects.create_user(username="staff", password="testpassword", is_staff=True)

        linestring = GEOSGeometry(
            'LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327,'
            '266876 7037333,266916 7037334,266955 7037332,267032 7037323,267127 7037314,267174 7037300,267181 7037296,'
            '267185 7037296,267191 7037300)', 32633
        )
        RoadSegment.objects.create(
            the_geom=linestring, county=1, href=1, category=1, municipality=1, startdate='2018-1-1', region=1,
            stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
        )
        d = RoadSegment.objects.get()

        # Create data in db
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.7758584, startlong=20.756444, endlat=60.45454, endlong=20.57575,
            plow_active=True, segment=d
        )
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.4564577, startlong=20.465565, endlat=60.646566, endlong=20.4564, segment=d
        )
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.56345345, startlong=20.3453453, endlat=60.3453453, endlong=20.4354,
            wet_spreader_active=True, segment=d
        )

    def test_get_all_prod_data_authenticated_staff(self):
        """
        Test GET request while authenticated as staff
        """
        self.client.login(username='staff', password='testpassword')

        # Create instance of GET request
        url = reverse('productiondata-list')
        response = self.client.get(url)

        # Get data from db and run test
        prod_data = ProductionData.objects.all()
        serializer = ProductionDataSerializer(prod_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_prod_data_authenticated(self):
        """
        Test GET request while authenticated, but not staff
        """
        self.client.login(username='normal_user', password='testpassword')

        # Create instance of GET request
        url = reverse('productiondata-list')
        response = self.client.get(url)

        # Run test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_prod_data_not_authenticated(self):
        """
        Test GET request while not authenticated
        """
        # Create instance of GET request
        url = reverse('productiondata-list')
        response = self.client.get(url)

        # Run test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostProductionDataTest(APITestCase):
    """
    Tests for posting data to the production data endpoint.
    """
    def setUp(self):
        # Make users
        User.objects.create_user(username="normal_user", password="testpassword")
        User.objects.create_user(username="staff", password="testpassword", is_staff=True)

        linestring = GEOSGeometry(
            'LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327,'
            '266876 7037333,266916 7037334,266955 7037332,267032 7037323,267127 7037314,267174 7037300,267181 7037296,'
            '267185 7037296,267191 7037300)', 32633
        )
        RoadSegment.objects.create(
            the_geom=linestring, county=1, href=1, category=1, municipality=1, startdate='2018-1-1', region=1,
            stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
        )

        # Make the test data
        self.data = [{
            "time": "2018-02-02T00:00:00", "startlat": 63.387075002372903, "startlong": 10.3277250005425,
            "endlat": 60.45454, "endlong": 20.57575, "plow_active": True
        }, {
            "time": "2018-02-02T00:01:00", "startlat": 63.387691997704202, "startlong": 10.3290819995141,
            "endlat": 60.646566, "endlong": 20.45645, "plow_active": True
        }]

    def test_post_prod_data_list_authenticated(self):
        """
        Testing that the endpoint takes in correctly formatted data and stores it in db.
        """
        # Authenticate user
        self.client.login(username="normal_user", password="testpassword")

        # Post the data
        url = reverse('productiondata-list')
        response = self.client.post(url, self.data, format='json')

        # Check the status code, then check that the number of objects in the database matches the number
        # of objects that are within range in the POST request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionData.objects.count(), 1)

    def test_post_prod_data_list_authenticated_staff(self):
        """
        Testing that the endpoint takes in correctly formatted data and stores it in db.
        """
        # Authenticate user
        self.client.login(username="staff", password="testpassword")

        # Post the data
        url = reverse('productiondata-list')
        response = self.client.post(url, self.data, format='json')

        # Check the status code, then check that the number of objects in the database matches the number
        # of objects that are within range in the POST request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionData.objects.count(), 1)

    def test_post_prod_data_list_unauthenticated(self):
        """
        Testing that the endpoint has the correct restrictions on permissions.
        """
        url = reverse('productiondata-list')
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MapperTest(APITestCase):
    """
    Tests for mapper
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

    def test_distance_from_point_to_linestring(self):
        production_data = [{"startlat": 63.387691997704202, "startlong": 10.3290819995141},
                           {"startlat": 63.387441999029399, "startlong": 10.3290930003037}]
        result = []
        for data in production_data:
            result.append(mapper.point_to_linestring_distance((data["startlong"], data["startlat"]),
                                                              MAX_MAPPING_DISTANCE))

        self.assertAlmostEqual(result[0]["distance"], 19.7805, 3)
        self.assertAlmostEqual(result[1]["distance"], 9.9352, 3)

    def test_map_to_segment(self):
        # Make test production data
        production_data_out_of_range = [{"startlat": 63.387075002372903, "startlong": 10.3277250005425}]
        production_data_in_range = [{"startlat": 63.387691997704202, "startlong": 10.3290819995141}]

        # Check that the out of range one does not map
        mapped_data = mapper.map_to_segment(production_data_out_of_range)
        self.assertEqual(len(mapped_data), 0)
        # Check that the in range one maps
        mapped_data = mapper.map_to_segment(production_data_in_range)
        self.assertEqual(len(mapped_data), 1)


class OverlapHandlingTest(APITestCase):
    """
    Tests for handling overlapping production data
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
        d = RoadSegment.objects.get()

        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=63.387691997704202, startlong=10.3290819995141, endlat=60.45454, endlong=20.57575,
            plow_active=True, segment=d
        )
        self.mapped_data = [
            {"time": timezone.now(), "startlat": 63.387441999029399, "startlong": 10.3290930003037, "endlat": 1,
             "endlong": 1, "segment": d.id},
            {"time": timezone.now(), "startlat": 63.387441999029399, "startlong": 10.3290930003037, "endlat": 1,
             "endlong": 1, "segment": d.id}
        ]

    def test_find_segments_and_latest_time(self):
        # relevant_segments = mapper.find_newest_prod_on_segment(self.mapped_data)
        # self.assertEqual(len(relevant_segments), 1)
        pass
