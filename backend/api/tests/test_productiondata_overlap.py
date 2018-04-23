import pytz
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from rest_framework.test import APITestCase

from api.mapper import mapper
from api.models import ProductionData, RoadSegment

# Linestrings for road segments
LINESTRING1 = GEOSGeometry(
    "LINESTRING(10.3303171552224 63.3868660024525,10.3302398268529 63.3869038464144,"
    "10.3301611003161 63.386945332982,10.3300607531286 63.3870026563505,10.3300162455014 63.3870322226421,"
    "10.329917159294 63.3871064024165,10.3298590511032 63.3871468562417,10.3297727527221 63.3872028393556,"
    "10.3296691810762 63.3872602368836,10.3295951207924 63.3872952215492,10.3295295537324 63.3873297620642,"
    "10.3294876263839 63.387350870135,10.3294669107934 63.3873672789016,10.3294508648541 63.3873845585497,"
    "10.329437321074 63.3874074067165,10.329422954164 63.3874291477097,10.3294189666945 63.3874450243487,"
    "10.3294181185706 63.387458843438,10.3294232311167 63.387471782116,10.3294363426886 63.3874897470291,"
    "10.3294525545099 63.3875059254082,10.3294958916793 63.3875451142029,10.329546337561 63.3875800395332,"
    "10.329578357989 63.387597636003)",
    4326
)
LINESTRING2 = GEOSGeometry(
    "LINESTRING(10.329578357989 63.387597636003,10.329614923004 63.3876143911706,"
    "10.3296530686045 63.3876276019293,10.3296819761688 63.3876347534309,10.3297598296266 63.387654031469,"
    "10.3298589075503 63.3876784088804,10.3299625183947 63.3876983505985,10.3300483040782 63.3877144699349,"
    "10.3301204192608 63.3877259150878,10.3302229931225 63.3877448324512,10.3303208533203 63.3877668336902,"
    "10.3303878373982 63.3877826947371,10.330482985185 63.3878028989352,10.3305592982307 63.387815649334,"
    "10.3306268062333 63.3878282935607,10.3307181935182 63.3878481921356,10.33093874243 63.3878862602697,"
    "10.3310934584831 63.3879087751377,10.3312020718903 63.3879201548673,10.3312676892749 63.3879234741162,"
    "10.331299544437 63.387923617223,10.3313300913905 63.38792191939,10.3313549798389 63.3879180581121,"
    "10.3313868933047 63.3879092126673,10.3314212230004 63.3878978358587)",
    4326
)
LINESTRING3 = GEOSGeometry(
    "LINESTRING(10.3588772803006 63.3980595840774,10.35867781632 63.3980416514715,"
    "10.3586230900353 63.3980476936328,10.3585783730694 63.3980526234967,10.3585060995595 63.3980555762041,"
    "10.358350896654 63.3980480061694,10.3578191049594 63.3979993109289,10.3575831194302 63.3979679779841,"
    "10.3574824057577 63.3979533684211,10.3572966039781 63.3979304131954,10.3571747178054 63.3978867874508,"
    "10.3570775037304 63.3978406388763)",
    4326
)
LINESTRING4 = GEOSGeometry(
    "LINESTRING(10.3570775037304 63.3978406388763,10.356969796025 63.397781287755,"
    "10.3568513118478 63.3977018036882,10.3566608358951 63.3975826550319,10.3564502324674 63.3974615026546,"
    "10.3562913916411 63.3973711712422,10.3561418619147 63.3972741284506,10.3558302339342 63.3971291806423)",
    4326
)
LINESTRING5 = GEOSGeometry(
    "LINESTRING(10.3558302339342 63.3971291806423,10.3556821376616 63.3970567344079,"
    "10.3555442496339 63.396993071835,10.3554614583309 63.3969334529691,10.3553943764922 63.3968870244603,"
    "10.3553699363651 63.3968509784815)",
    4326
)

TIMEZONE = pytz.UTC


class OverlapHandlingTest(APITestCase):
    """
    Tests for handling overlapping production data
    """
    def setUp(self):
        """
        Set up database objects and test variables
        """
        segments = [
            RoadSegment.objects.create(
                the_geom=LINESTRING1, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING2, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING3, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING4, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING5, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            )
        ]
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[0]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[1]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[1]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[2]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[2]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[3]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[3]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[4]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[4]
        )
        self.mapped_data = [
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 0, 0, 0), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[1].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 0, 0, 30), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[1].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 0), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[2].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 30), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[3].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 1, 0), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[4].id}
        ]

    def test_find_segments_and_latest_time(self):
        """
        Test for finding earliest and latest times for a segment in mapped production data
        """
        segment_times = mapper.find_time_period_per_segment(self.mapped_data)
        self.assertEqual(len(segment_times), 4)

        correct_result = {
            str(self.mapped_data[1]["segment"]): {"earliest_time": self.mapped_data[0]["time"],
                                                  "latest_time": self.mapped_data[1]["time"]},
            str(self.mapped_data[2]["segment"]): {"earliest_time": self.mapped_data[2]["time"],
                                                  "latest_time": self.mapped_data[2]["time"]},
            str(self.mapped_data[3]["segment"]): {"earliest_time": self.mapped_data[3]["time"],
                                                  "latest_time": self.mapped_data[3]["time"]},
            str(self.mapped_data[4]["segment"]): {"earliest_time": self.mapped_data[4]["time"],
                                                  "latest_time": self.mapped_data[4]["time"]}
        }

        for segment in segment_times:
            self.assertEqual(segment_times[segment]["earliest_time"], correct_result[segment]["earliest_time"])
            self.assertEqual(segment_times[segment]["latest_time"], correct_result[segment]["latest_time"])

    def test_delete_overlapped_prod_data(self):
        """
        Test for deleting overlapped production data
        """
        mapper.handle_prod_data_overlap(self.mapped_data)
        prod_data = ProductionData.objects.all()
        self.assertEqual(len(prod_data), 1)


class OverlapHandlingOutdatedInputDataTest(APITestCase):
    """
    Test for handling overlapping data when the input data is old/outdated by data already in db
    """
    def setUp(self):
        """
        Set up database objects and test variables
        """
        segments = [
            RoadSegment.objects.create(
                the_geom=LINESTRING3, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING4, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING5, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ),
            RoadSegment.objects.create(
                the_geom=LINESTRING5, county=1, href=1, category=1, municipality=1,
                startdate=timezone.datetime(2018, 1, 1, 0, 0, 0), region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            )
        ]
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 3, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[0]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 3, 1, 0, 0, 30), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[0]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 1, 1, 0, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[1]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[2]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 30), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[2]
        )
        ProductionData.objects.create(
            time=timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 0), TIMEZONE), startlat=1, startlong=1,
            endlat=1, endlong=1, plow_active=True, segment=segments[3]
        )
        self.mapped_data = [
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 0, 0, 0), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[0].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 0, 0, 30), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[0].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 0), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[1].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 30), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[1].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 0, 59, 45), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[2].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 15), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[2].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 0, 59, 45), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[3].id},
            {"time": timezone.make_aware(timezone.datetime(2018, 2, 1, 1, 0, 15), TIMEZONE), "startlat": 1,
             "startlong": 1, "endlat": 1, "endlong": 1, "segment": segments[3].id}
        ]
        self.segment_times = {
            str(segments[0].id): {"earliest_time": self.mapped_data[0]["time"],
                                  "latest_time": self.mapped_data[1]["time"]},
            str(segments[1].id): {"earliest_time": self.mapped_data[2]["time"],
                                  "latest_time": self.mapped_data[3]["time"]},
            str(segments[2].id): {"earliest_time": self.mapped_data[4]["time"],
                                  "latest_time": self.mapped_data[5]["time"]},
            str(segments[3].id): {"earliest_time": self.mapped_data[6]["time"],
                                  "latest_time": self.mapped_data[7]["time"]}
        }

    def test_filter_prod_data(self):
        """
        Test for filtering out outdated production data based on the data already in db
        """
        filtered_prod_data = mapper.remove_outdated_prod_data(self.segment_times, self.mapped_data)

        # Outdated by a large margin
        self.assertNotIn(self.mapped_data[0], filtered_prod_data)
        self.assertNotIn(self.mapped_data[1], filtered_prod_data)
        # Not outdated by a large margin
        self.assertIn(self.mapped_data[2], filtered_prod_data)
        self.assertIn(self.mapped_data[3], filtered_prod_data)
        # Outdated by a small margin
        self.assertNotIn(self.mapped_data[4], filtered_prod_data)
        self.assertNotIn(self.mapped_data[5], filtered_prod_data)
        # Not outdated by a small margin
        self.assertIn(self.mapped_data[6], filtered_prod_data)
        self.assertIn(self.mapped_data[7], filtered_prod_data)
