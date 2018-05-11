import unittest

from apps.api.segmenter.road_segmenter import geometry_to_list
from apps.data.road_segmenting.road_fetcher import vegnet_to_geojson
from apps.data.road_segmenting.road_filter import filter_road
from vapi.constants import MAX_SEGMENT_LENGTH, MIN_COORDINATES_LENGTH

from api.segmenter.calculate_distance import calculate_road_length_simple
from api.segmenter.road_segmenter import segment_network, split_segment


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

        # Apparently the setUpClass is a bit funky and the road_net does not stay filtered after setUpClass is run,
        # so instead it is done in each test function it is needed instead of here.
        road_net_list = []
        for road in cls.road_net:
            road_net_list.append(filter_road(road))
        cls.road_net_segmented = segment_network(road_net_list, cls.max_segment_distance, cls.min_coordinates_length)

    def setUp(self):
        pass

    def test_road_segmenter_list(self):
        """
        The road_segmenter function should return a list
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
        The road_filter function should return a string, otherwise segmentation will crash in later stages
        :return: Nothing
        """
        for road in self.road_net:
            road = filter_road(road)
            self.assertIsInstance(road["the_geom"], str, "road_filter should turn geometry into a string")

    def test_geometry_conversion(self):
        """
        The geometry_to_list function should return a dictionary containing coordinates as a list,
        otherwise the segmenter can't split segments
        :return: Nothing
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
        :return: Nothing
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

    def test_missing_coordinates(self):
        """
        All original coordinates should still be present after segmenting road network
        :return: Nothing
        """
        for road in self.road_net:
            road = convert(road)
            coordinates_original = road["the_geom"]["coordinates"]

            road_segmented = split_segment(road, self.max_segment_distance, [], self.min_coordinates_length)
            coordinates_segmented = []
            for segment in road_segmented:
                coordinates_segmented.extend(segment["the_geom"]["coordinates"])

            for coordinate in coordinates_original:
                self.assertTrue(coordinate in coordinates_segmented, "Missing coordinate after segmenting")

    def test_over_and_undersegmenting(self):
        """
        The segmenter should only run on segments that are over the limit in length, it should never segment something
        shorter than that. In other words the segmented road should still be only one segment
        :return: Nothing
        """
        i = 0
        for road in self.road_net:
            i += 1
            converted_road = convert(road)
            road_coords_length = len(converted_road["the_geom"]["coordinates"])
            road_distance = calculate_road_length_simple(converted_road["the_geom"]["coordinates"])
            road_segmented = segment_network([filter_road(road)], self.max_segment_distance,
                                             self.min_coordinates_length)
            road_segmented_length = len(road_segmented)
            if road_distance < self.max_segment_distance:
                self.assertTrue(road_segmented_length == 1, "This road was segmented, but should not have been.")
            elif road_coords_length >= 2*self.min_coordinates_length and road_distance > self.max_segment_distance:
                self.assertTrue(road_segmented_length > 1, ("This road should have been segmented, but was not. "
                                "Stretchdistance:", road_distance, "Coordinates:",
                                                            converted_road["the_geom"]["coordinates"], i))


if __name__ == "__main__":
    unittest.main()
