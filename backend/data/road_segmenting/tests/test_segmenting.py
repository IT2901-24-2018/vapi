import unittest

from calculate_distance import calculate_road_length
from road_fetcher import vegnet_to_geojson
from road_segmenter import segment_network, split_segment


class TestSegmenting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kommune = 5001
        cls.vegref = "kg"
        cls.max_segment_length = 100
        cls.min_segment_length = 2
        network = vegnet_to_geojson(cls.kommune, cls.vegref)
        cls.count, cls.road_net = network[0], network[1]
        cls.split_segments = segment_network(cls.road_net, cls.count,
                                             cls.max_segment_length, cls.min_segment_length)

    def setUp(self):
        pass

    def test_road_segmenter_list(self):
        """
        road_segmenter should return a list
        :return: Nothing
        """
        self.assertIsInstance(self.split_segments, list, "The road segmenter did not return a list")

    def test_road_segmenter_list_elements(self):
        """
        Every element in the split segments should be a dict
        :return: Nothing
        """
        count = 0
        error_message = "Not all elements in the split list are of type dict: \n"
        for road in self.split_segments:
            if not isinstance(road, dict):
                count += 1
                error_message += "Index: " + str(self.split_segments.index(road)) + ", typeof: " + \
                                 str(type(road)) + "\n"
        self.assertLess(count, 1, error_message)

    def test_split_segment_geometry_len(self):
        """
        Given a list of roads segments, the split segments should always have a length
        of 2 or more
        :return: Nothing
        """
        count = 0
        error_message = "These segments have less than " \
                        + str(self.min_segment_length) + " GPS points \n"
        for road in self.split_segments:
            if len(road["geometry"]["coordinates"]) < self.min_segment_length:
                count += 1
                error_message += "Veglenkeid: " + str(road["properties"]["veglenkeid"]) + ", coordinates: " + \
                                 str(road["geometry"]["coordinates"]) + "\n"
        self.assertLess(count, 1, (count, "errors:", error_message))

    def test_calculate_road_length(self):
        """
        The total distance of the segmented road should be similar to the length before segmentation, within
        a margin given by the variable "margin"
        :return: Nothing
        """
        margin = 8
        errors = 0
        error_message = "Issues are with these segments: \n"
        for key, values in self.road_net.items():
            if key != "crs":
                for i in range(0, self.count):
                    road = self.road_net["features"][i]
                    length_actual = road["properties"]["strekningslengde"]
                    length_original = calculate_road_length(road["geometry"]["coordinates"], 1000, False)[1]
                    road_segmented = split_segment(road, self.max_segment_length, [], self.min_segment_length)

                    length_new = 0
                    for segment in road_segmented:
                        length_new += calculate_road_length(segment["geometry"]["coordinates"], 1000, False)[1]
                    if abs(length_actual - length_new) > margin:
                        errors += 1
                        error_message += "Veglenkeid: " + str(road["properties"]["veglenkeid"]) + \
                                         ", actual length: " + str(length_actual) + ", original: " + \
                                         str(length_original) + ", new:" + str(length_new) + "\n"
        self.assertLess(errors, 1, (errors, "errors:", error_message))

    def test_split_segment_chaining(self):
        """
        Every connected segment should start with the end gps point of the previous segment
        :return: Nothing
        """
        errors = 0
        error_message = "Issues are with these " + str(errors) + " links: \n"
        for key, values in self.road_net.items():
            if key != "crs":
                for i in range(0, self.count):
                    road = self.road_net["features"][i]
                    road_segmented = split_segment(road, self.max_segment_length, [], self.min_segment_length)

                    for segment in range(1, len(road_segmented)):
                        prev = road_segmented[segment-1]["geometry"]["coordinates"]
                        end_prev = prev[len(prev)-1]
                        start_curr = road_segmented[segment]["geometry"]["coordinates"][0]

                        if end_prev != start_curr:
                            errors += 1
                            error_message += "Veglenkeid: " + str(road["properties"]["veglenkeid"]) + \
                                ", does not start at " + str(end_prev) + ", instead: " + str(start_curr) + "\n"
        self.assertLess(errors, 1, (errors, "errors:", error_message))

    def test_split_segment_road_length(self):
        # This test is a little useless to be honest, we don't necessarily care
        # if a road segment goes over the limit. It does however give us an idea
        # of how accurate the segmentation is
        """
        Given a list of road segments, the length of the split segments should all be
        within a margin of error given by the variable "margin"
        :return: Nothing
        """
        margin = 50
        errors = 0
        for road in self.split_segments:
            if (road["properties"]["strekningslengde"] - self.max_segment_length) > margin:
                errors += 1

        self.assertLess(errors, 50, (errors, "roads exceeded the road length limit"))

    def test_split_segment_negative_length(self):
        """
        No road segments should have a negative road length
        :return:
        """
        errors = 0
        for road in self.split_segments:
            if road["properties"]["strekningslengde"] < 0:
                errors += 1

        self.assertLess(errors, 1, ("This many segments are under 0 meters:", errors))


if __name__ == "__main__":
    unittest.main()
