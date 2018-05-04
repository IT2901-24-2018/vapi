import unittest

from api.segmenter.calculate_distance import calculate_road_length_simple
from apps.data.road_segmenting.road_fetcher import vegnet_to_geojson
from api.segmenter.road_segmenter import segment_network, split_segment
from vapi.constants import MAX_SEGMENT_LENGTH, MIN_COORDINATES_LENGTH
from apps.data.road_segmenting.road_filter import filter_road
from apps.api.segmenter.road_segmenter import geometry_to_list


def convert(road):
    road = filter_road(road)
    road["the_geom"] = geometry_to_list(road["the_geom"])
    return road


class TestSegmenting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kommune = 5001
        cls.vegref = "kg"
        cls.max_segment_distance = MAX_SEGMENT_LENGTH
        cls.min_coordinates_length = MIN_COORDINATES_LENGTH
        network = vegnet_to_geojson(cls.kommune, cls.vegref)
        cls.count, cls.road_net = network[0], network[1]["features"]

        temp = []
        for road in cls.road_net:
            temp.append(filter_road(road))
        cls.road_net_segmented = segment_network(temp, cls.max_segment_distance, cls.min_coordinates_length)

    def setUp(self):
        pass

    def test_road_segmenter_list(self):
        """
        road_segmenter should return a list
        :return: Nothing
        """
        self.assertIsInstance(self.road_net_segmented, list, "The road segmenter did not return a list")

    def test_road_segmenter_list_elements(self):
        """
        Every element in the split segments should be a dict
        :return: Nothing
        """
        error_message = "Not all elements in the split list are of type dict \n"
        for segment in self.road_net_segmented:
            self.assertIsInstance(segment, dict, error_message)

    def test_split_segment_geometry_len(self):
        """
        Given a list of roads segments, the split segments should always have a length
        of 2 or more
        :return: Nothing
        """
        error_message = "Segment has less than " + str(self.min_coordinates_length) + " GPS coordinates"
        for segment in self.road_net_segmented:
            # coordinates are split by commas, so the count of commas+1 should be the same as the count of coordinates
            coordinates_amount = segment["the_geom"].count(",")
            self.assertGreaterEqual(coordinates_amount+1, self.min_coordinates_length, error_message)

    def test_road_filter(self):
        """
        Tests if road_filter returns a string, otherwise segmentation will crash in later stages
        :return:
        """
        for road in self.road_net:
            road = filter_road(road)
            self.assertIsInstance(road["the_geom"], str, "road_filter should turn geometry into a string")

    def test_geometry_conversion(self):
        """
        Tests if geometry_to_list works properly, otherwise the segmenter can't split segments
        :return:
        """
        for road in self.road_net:
            road = convert(road)
            self.assertIsInstance(road["the_geom"], dict, "geometry_to_list should return a "
                                                          "dictionary")
            self.assertIsInstance(road["the_geom"]["coordinates"], list, "geometry_to_list should return a turn the "
                                                                         "coordinates into a list")

    def test_calculate_road_length(self):
        """
        The total distance of the segmented road should be similar to the length before segmentation, within
        a margin given by the variable "margin"
        :return: Nothing
        """
        margin = 3
        for road in self.road_net:
            road = convert(road)

            length_before = calculate_road_length_simple(road["the_geom"]["coordinates"])

            road_segmented = split_segment(road, self.max_segment_distance, [], self.min_coordinates_length)

            length_after = 0
            for segment in road_segmented:
                length_after += calculate_road_length_simple(segment["the_geom"]["coordinates"])

            self.assertLess(abs(length_after - length_before), margin, "The difference between the original "
                                                                       "length and the segmented length is "
                                                                       "too large")

    def test_split_segment_chaining(self):
        """
        Every connected segment should start with the end gps point of the previous segment
        :return: Nothing
        """
        for road in self.road_net:
            road = convert(road)
            road_segmented = split_segment(road, self.max_segment_distance, [], self.min_coordinates_length)

            for i in range(1, len(road_segmented)):
                curr_segment = road_segmented[i]
                prev_segment = road_segmented[i-1]
                end_coordinate = len(prev_segment["the_geom"]["coordinates"])-1

                self.assertEqual(curr_segment["the_geom"]["coordinates"][0],
                                 prev_segment["the_geom"]["coordinates"][end_coordinate],
                                 "Segments are not correctly chained")

    def test_split_segment_negative_length(self):
        """
        No road segments should have a negative road length
        :return:
        """
        for segment in self.road_net_segmented:
            self.assertGreater(segment["stretchdistance"], 0, "Stretchdistance must be of at least 1 meter")

    def test_duplicate_segments(self):
        """
        Test if there are multiple segments with the same coordinates
        """
        length = len(self.road_net_segmented)-1
        for i in range(length):
            road = self.road_net_segmented[i]["the_geom"]
            for x in range(i+1, length):
                other_road = self.road_net_segmented[x]["the_geom"]
                self.assertNotEqual(road, other_road, "Duplicate segment geometry coordinates")


if __name__ == "__main__":
    unittest.main()
