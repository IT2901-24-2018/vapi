import unittest

from api.segmenter.calculate_distance import (calculate_road_length, calculate_road_length_simple,
                                              utm_to_latlon)


class TestCalculateDistance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.coordinates = [[271160.30566, 7042104.25293],
                           [271164.5, 7042102.1001], [271167.6001, 7042101.8999],
                           [271171.1001, 7042102.69971], [271177.1001, 7042106.5],
                           [271182.69995, 7042111.30029], [271186.80005, 7042115.5],
                           [271188.8999, 7042118.5], [271195.69995, 7042124.0],
                           [271204.69995, 7042131.19971], [271213.6001, 7042137.3999],
                           [271221.1001, 7042142.6001], [271227.3999, 7042147.0],
                           [271230.6001, 7042148.3999], [271234.5, 7042147.6001],
                           [271239.8999, 7042146.8999], [271245.8999,  7042147.3999],
                           [271249.69995, 7042149.30029], [271252.8, 7042152.2]]
        cls.coordinate_single = [271160.30566, 7042104.25293]
        cls.coordinate_single_latlong = [63.43360, 4.41107]
        cls.max_length = 100
        cls.min_coordinates = 2
        cls.zone1 = 32
        cls.zone2 = "V"

    def setUp(self):
        """
        Needs to be here for the tests to run
        """
        pass

    def test_int(self):
        """
        The distance calculator should always return an int
        :return: None
        """
        self.assertIsInstance(calculate_road_length_simple(self.coordinates), int)
        self.assertIsInstance(calculate_road_length(self.coordinates, self.max_length)[1], int)

    def test_correct_split_index(self):
        """
        This example, given that the max road length is 100, should split at index = 16, where the length exceeds 100m
        :return: None
        """
        split_index = calculate_road_length(self.coordinates, self.max_length)[0]
        self.assertEqual(split_index, 16)

    def test_correct_length(self):
        """
        The calculate_road_length function should return 103 meters, where the road exceeds 100 meters, while the
        calculate_road_length_simple function should return the total length of the road, which is 111
        :return: None
        """
        self.assertEqual(calculate_road_length(self.coordinates, self.max_length)[1], 103)
        self.assertEqual(calculate_road_length_simple(self.coordinates), 111)

    def test_utm_conversion(self):
        """
        The utm converter should return the list in latlong format
        :return: None
        """
        coord = utm_to_latlon(self.coordinate_single, self.coordinate_single, self.zone1, self.zone2)[0]
        coord[0] = round(coord[0], 5)
        coord[1] = round(coord[1], 5)
        self.assertEqual(coord, self.coordinate_single_latlong)
