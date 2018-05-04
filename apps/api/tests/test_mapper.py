import json
from os import path

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.test import APITestCase
from vapi.constants import MAX_MAPPING_DISTANCE

from api.mapper.mapper import map_to_segment, get_candidates
from api.models import RoadSegment


class MapperMethodTests(APITestCase):
    """
    Tests for mapper
    """
    def setUp(self):
        geojson = json.load(open(path.join(path.dirname(path.realpath(__file__)), "./test_segments.geojson")))

        self.segments = []
        for i in [5, 6, 8, 9, 10]:
            self.segments.append(RoadSegment.objects.create(
                the_geom=str(geojson["features"][i]["geometry"]), county=geojson["features"][i]["properties"]["id"],
                href=1, category=1, municipality=1, startdate="2018-1-1", region=1, stretchdistance=1, typeofroad=1,
                roadsectionid=1, vrefshortform=1
            ))

    def test_get_candidates(self):
        geojson = json.load(open(path.join(path.dirname(path.realpath(__file__)), "./easy_prod_sequence.geojson")))
        sequence = []
        for i in range(0, len(geojson["features"]), 2):
            sequence.append({"startlong": geojson["features"][i]["geometry"]["coordinates"][0],
                             "startlat": geojson["features"][i]["geometry"]["coordinates"][1],
                             "endlong": geojson["features"][i + 1]["geometry"]["coordinates"][0],
                             "endlat": geojson["features"][i + 1]["geometry"]["coordinates"][1],
                             "id": i,
                             # Test attribute
                             # "id": "{}-{}".format(geojson["features"][i]["properties"]["id"],
                             #                      geojson["features"][i + 1]["properties"]["id"])
            })

        result = get_candidates(sequence, MAX_MAPPING_DISTANCE)

        correct_distance = [2.4114, 0.0, 18.2840, 4.4422, 4.6758, 3.8431, 0.3521, 4.4823, 0.0, 0.8275, 3.7591, 0.9372,
                          0.0, 0.2524]
        correct_start_end_distance = [12.3721, 12.6995, 12.6995, 13.6162, 13.6162, 9.8948, 12.8562, 10.8718, 13.8877,
                                      13.8877,
                                      13.8877, 27.0897, 20.5911, 20.5911]
        correct_mapped_distance = [10.4959, 15.7394, 0.0, 0.0, 15.2035, 9.7415, 11.9420, 10.4625, 3.9672, 2.0424,
                                   2.5904, 24.6627, 18.4799, 3.8543]

        for i in range(len(result)):
            # Test each candidate distance
            self.assertAlmostEqual(result[i]["distance"], correct_distance[i], 3)
            # Test distance between start and end points
            self.assertAlmostEqual(result[i]["distance_between_start_end"], correct_start_end_distance[i], 3)
            # Test distance between remapped start and end points
            self.assertAlmostEqual(result[i]["distance_on_segment"], correct_mapped_distance[i], 3)


    def test_map_to_segment(self):
        # Make test production data
        production_data_out_of_range = [{"startlat": 63.387075002372903, "startlong": 10.3277250005425}]
        production_data_in_range = [{"startlat": 63.387691997704202, "startlong": 10.3290819995141}]

        # Check that the out of range one does not map
        mapped_data = map_to_segment(production_data_out_of_range)
        self.assertEqual(len(mapped_data), 0)
        # Check that the in range one maps
        mapped_data = map_to_segment(production_data_in_range)
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
        for i in [5, 6, 8, 9, 10]:
            self.segments1.append(RoadSegment.objects.create(
                the_geom=linestrings[i], county=1, href=1, category=1, municipality=1, startdate="2018-1-1", region=1,
                stretchdistance=1, typeofroad=1, roadsectionid=1, vrefshortform=1
            ))
        self.segments2 = []
        for i in [0, 1, 2, 3, 4, 7]:
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
                             "startlat": feature["geometry"]["coordinates"][1]},)

        mapped_sequence = map_to_segment(sequence)

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
        for i in range(0, len(geojson["features"]), 2):
            sequence.append(
                {"startlong": geojson["features"][i]["geometry"]["coordinates"][0],
                 "startlat": geojson["features"][i]["geometry"]["coordinates"][1],
                 "endlong": geojson["features"][i + 1]["geometry"]["coordinates"][1],
                 "endlat": geojson["features"][i + 1]["geometry"]["coordinates"][1]
                }
            )


        mapped_sequence = map_to_segment(sequence)

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
