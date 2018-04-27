from django.contrib.gis.geos import GEOSGeometry
from rest_framework.test import APITestCase
from vapi.constants import MAX_MAPPING_DISTANCE

from api.mapper import mapper
from api.models import RoadSegment


class MapperTest(APITestCase):
    """
    Tests for mapper
    """
    def setUp(self):
        linestring = GEOSGeometry(
            "LINESTRING(266711 7037272,266712 7037276,266747 7037300,266793 7037316,266826 7037325,266835 7037327,"
            "266876 7037333,266916 7037334,266955 7037332,267032 7037323,267127 7037314,267174 7037300,267181 7037296,"
            "267185 7037296,267191 7037300)", 32633
        )
        RoadSegment.objects.create(
            the_geom=linestring, county=1, href=1, category=1, municipality=1, startdate="2018-1-1", region=1,
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
