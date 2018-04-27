from backend.constants import MAX_MAPPING_DISTANCE
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.test import APITestCase

from api.mapper import mapper
from api.models import RoadSegment

import json
from os import path


class MapperSingleSegmentTest(APITestCase):
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


class MapperMultiSegmentTest(APITestCase):
    """
    Tests for mapper with more than one segment in db
    """
    def setUp(self):
        geojson = json.load(open(path.join(path.dirname(path.realpath(__file__)), "./test_segments.geojson")))
        linestrings = []
        for feature in geojson["features"]:
            linestrings.append(GEOSGeometry(str(feature["geometry"])))
        self.segments1 = []
        for i in [6, 7, 9, 10, 11]:
            self.segments1.append(RoadSegment.objects.create(
                the_geom=linestrings[i], county=1, href=1, category=1, municipality=1, startdate="2018-1-1", region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ))
        self.segments2 = []
        for i in [0, 1, 2, 4, 5, 8]:
            self.segments2.append(RoadSegment.objects.create(
                the_geom=linestrings[i], county=1, href=1, category=1, municipality=1, startdate="2018-1-1", region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ))

    def test_continuous_line_mapping(self):
        """
        Test mapping of a sequence of points that mostly follow a segments
        """
        geojson = json.load(open(path.join(path.dirname(path.realpath(__file__)), "./easy_prod_sequence.geojson")))
        sequence = []
        for feature in geojson["features"]:
            sequence.append({"startlong": feature["geometry"]["coordinates"][0],
                             "startlat": feature["geometry"]["coordinates"][1]})

        mapped_sequence = mapper.map_to_segment(sequence)

        # Test that all the points were mapped
        self.assertEqual(len(sequence), len(mapped_sequence))

        # Test that all the points were mapped to the correct segment
        for point in mapped_sequence[:5]:
            self.assertEqual(point["segment"], self.segments1[1].id, "{}".format(point))

        for point in mapped_sequence[5:13]:
            self.assertEqual(point["segment"], self.segments1[0].id, "{}".format(point))

        for point in mapped_sequence[13:17]:
            self.assertEqual(point["segment"], self.segments1[3].id, "{}".format(point))

        self.assertEqual(mapped_sequence[17]["segment"], self.segments1[4].id, "{}".format(mapped_sequence[17]))

    def test_multiple_lines_mapping(self):
        """
        Test mapping of a sequence of points that do not follow the path closely
        """
        geojson = json.load(open(path.join(path.dirname(path.realpath(__file__)), "./difficult_prod_sequence.geojson")))
        sequence = []
        for feature in geojson["features"]:
            sequence.append({"startlong": feature["geometry"]["coordinates"][0],
                             "startlat": feature["geometry"]["coordinates"][1]})

        mapped_sequence = mapper.map_to_segment(sequence)

        # Test that all the points were mapped
        self.assertEqual(len(sequence), len(mapped_sequence))

        # Test that all the points were mapped to the correct segment
        for point in mapped_sequence[:3]:
            self.assertEqual(point["segment"], self.segments2[2].id, "{}".format(point))

        # Point 3 will need smarter mapping to be correct

        for point in mapped_sequence[4:6]:
            self.assertEqual(point["segment"], self.segments2[0].id, "{}".format(point))

        for point in mapped_sequence[6:9]:
            self.assertEqual(point["segment"], self.segments2[1].id, "{}".format(point))

        # Point 9 will need smarter mapping to be correct

        for point in mapped_sequence[10:13]:
            self.assertEqual(point["segment"], self.segments2[4].id, "{}".format(point))

        # Point 13 will need smarter mapping to be correct

        for point in mapped_sequence[14:16]:
            self.assertEqual(point["segment"], self.segments2[4].id, "{}".format(point))
