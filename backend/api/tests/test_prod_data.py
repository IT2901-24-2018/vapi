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
        linestring1 = GEOSGeometry(
            "LINESTRING(10.3303171552224 63.3868660024525,10.3302398268529 63.3869038464144,10.3301611003161 63.386945332982,10.3300607531286 63.3870026563505,10.3300162455014 63.3870322226421,10.329917159294 63.3871064024165,10.3298590511032 63.3871468562417,10.3297727527221 63.3872028393556,10.3296691810762 63.3872602368836,10.3295951207924 63.3872952215492,10.3295295537324 63.3873297620642,10.3294876263839 63.387350870135,10.3294669107934 63.3873672789016,10.3294508648541 63.3873845585497,10.329437321074 63.3874074067165,10.329422954164 63.3874291477097,10.3294189666945 63.3874450243487,10.3294181185706 63.387458843438,10.3294232311167 63.387471782116,10.3294363426886 63.3874897470291,10.3294525545099 63.3875059254082,10.3294958916793 63.3875451142029,10.329546337561 63.3875800395332,10.329578357989 63.387597636003)",
            4326
        )
        linestring2 = GEOSGeometry(
            "LINESTRING(10.329578357989 63.387597636003,10.329614923004 63.3876143911706,10.3296530686045 63.3876276019293,10.3296819761688 63.3876347534309,10.3297598296266 63.387654031469,10.3298589075503 63.3876784088804,10.3299625183947 63.3876983505985,10.3300483040782 63.3877144699349,10.3301204192608 63.3877259150878,10.3302229931225 63.3877448324512,10.3303208533203 63.3877668336902,10.3303878373982 63.3877826947371,10.330482985185 63.3878028989352,10.3305592982307 63.387815649334,10.3306268062333 63.3878282935607,10.3307181935182 63.3878481921356,10.33093874243 63.3878862602697,10.3310934584831 63.3879087751377,10.3312020718903 63.3879201548673,10.3312676892749 63.3879234741162,10.331299544437 63.387923617223,10.3313300913905 63.38792191939,10.3313549798389 63.3879180581121,10.3313868933047 63.3879092126673,10.3314212230004 63.3878978358587)",
            4326
        )
        linestring3 = GEOSGeometry(
            "LINESTRING(10.3588772803006 63.3980595840774,10.35867781632 63.3980416514715,10.3586230900353 63.3980476936328,10.3585783730694 63.3980526234967,10.3585060995595 63.3980555762041,10.358350896654 63.3980480061694,10.3578191049594 63.3979993109289,10.3575831194302 63.3979679779841,10.3574824057577 63.3979533684211,10.3572966039781 63.3979304131954,10.3571747178054 63.3978867874508,10.3570775037304 63.3978406388763)",
            4326
        )
        linestring4 = GEOSGeometry(
            "LINESTRING(10.3570775037304 63.3978406388763,10.356969796025 63.397781287755,10.3568513118478 63.3977018036882,10.3566608358951 63.3975826550319,10.3564502324674 63.3974615026546,10.3562913916411 63.3973711712422,10.3561418619147 63.3972741284506,10.3558302339342 63.3971291806423)",
            4326
        )
        linestring5 = GEOSGeometry(
            "LINESTRING(10.3558302339342 63.3971291806423,10.3556821376616 63.3970567344079,10.3555442496339 63.396993071835,10.3554614583309 63.3969334529691,10.3553943764922 63.3968870244603,10.3553699363651 63.3968509784815)",
            4326
        )
        segments = [
            RoadSegment.objects.create(
                the_geom=linestring1, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=linestring2, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=linestring3, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=linestring4, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=linestring5, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            )
        ]

        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[0]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[1]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[1]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[2]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[2]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[3]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[3]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[4]
        )
        ProductionData.objects.create(
            time=timezone.datetime(2018, 1, 1, 0, 0, 0), startlat=1, startlong=1, endlat=1, endlong=1, plow_active=True,
            segment=segments[4]
        )
        self.mapped_data = [
            {"time": timezone.datetime(2018, 2, 1, 0, 0, 0), "startlat": 1, "startlong": 1, "endlat": 1, "endlong": 1,
             "segment": segments[1].id},
            {"time": timezone.datetime(2018, 2, 1, 0, 0, 30), "startlat": 1, "startlong": 1, "endlat": 1, "endlong": 1,
             "segment": segments[1].id},
            {"time": timezone.datetime(2018, 2, 1, 0, 0, 0), "startlat": 1, "startlong": 1, "endlat": 1, "endlong": 1,
             "segment": segments[2].id},
            {"time": timezone.datetime(2018, 2, 1, 0, 0, 30), "startlat": 1, "startlong": 1, "endlat": 1, "endlong": 1,
             "segment": segments[3].id},
            {"time": timezone.datetime(2018, 2, 1, 0, 1, 0), "startlat": 1, "startlong": 1, "endlat": 1, "endlong": 1,
             "segment": segments[4].id}
        ]

    def test_find_segments_and_latest_time(self):
        relevant_segments = mapper.find_newest_prod_on_segment(self.mapped_data)
        self.assertEqual(len(relevant_segments), 4)
        correct_result = {str(self.mapped_data[1]["segment"]): self.mapped_data[1]["time"],
                          str(self.mapped_data[2]["segment"]): self.mapped_data[2]["time"],
                          str(self.mapped_data[3]["segment"]): self.mapped_data[3]["time"],
                          str(self.mapped_data[4]["segment"]): self.mapped_data[4]["time"]}
        for segment in relevant_segments:
            self.assertEqual(relevant_segments[segment], correct_result[segment])

    def test_delete_overlapped_prod_data(self):
        mapper.handle_prod_data_overlap(self.mapped_data)
        prod_data = ProductionData.objects.all()
        self.assertEqual(len(prod_data), 1)
