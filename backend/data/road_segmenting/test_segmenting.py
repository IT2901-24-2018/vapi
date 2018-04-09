import unittest
from calculate_distance import calculate_road_length
from road_fetcher import vegnet_to_geojson, road_network_to_file
from road_segmenter import road_segmentor


class TestSegmenting(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.kommune = 5001
        self.vegref = 'kg'
        self.max_segment_length = 100
        self.min_segment_length = 2
        self.road_net = vegnet_to_geojson(self.kommune, self.vegref)[1]
        self.split_segments = road_segmentor(self.kommune, self.vegref,
                                             self.max_segment_length, self.min_segment_length)

    def setUp(self):
        pass

    def test_road_segmentor_list(self):
        '''
        road_segmentor should return a list
        :return:
        '''
        self.assertIsInstance(self.split_segments, list)

    def test_road_segmentor_list_elements(self):
        '''
        every element in the split segments should be a dict
        :return:
        '''
        count = 0
        for road in self.split_segments:
            if not isinstance(road, dict):
                count += 1
        self.assertLess(count, 1)

    def test_split_segment_geometry_len(self):
        '''
        Given a list of roads segments, the split segments should always have a length
        of 2 or more
        :return:
        '''
        count = 0
        for road in self.split_segments:
            if len(road['geometry']['coordinates']) < self.min_segment_length:
                count += 1
                print(road['properties']['veglenkeid'], road['geometry']['coordinates'])
        self.assertLess(count, 1)

    def test_calculate_road_length(self):
        '''
        The total distance of the road should be within the margin of error
        given by the variable "margin"
        :return: True or false
        '''
        margin = 15
        road = self.road_net['features'][0]
        road_coordinates = road['geometry']['coordinates']
        distance = calculate_road_length(road_coordinates, self.max_segment_length, False)[1]
        actual_distance = road['properties']['til_meter'] - road['properties']['fra_meter']
        self.assertLessEqual(abs(distance - actual_distance), margin)

    def test_split_segment_road_length(self):
        # This test is a little useless to be honest, we don't necessarily care
        # if a road segment goes over the limit. It does however give us an idea
        # of how accurate the segmentation is
        '''
        Given a list of road segments, the length of the split segments should all be
        within a margin of error given by the variable "margin"
        :return:
        '''
        margin = 50
        error = 0
        for road in self.split_segments:
            if (road['properties']['strekningslengde'] - self.max_segment_length) > margin:
                error += 1
        print(str(error) + ' veier gikk over grensen i lengde')
        self.assertLess(error, 20)

    # test post to db

    # test deletion from db


if __name__ == '__main__':
    unittest.main()
