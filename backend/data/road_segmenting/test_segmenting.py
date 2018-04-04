import unittest
from calculate_distance import calculate_road_length
from road_fetcher import vegnet_to_geojson

kommune = 5001
vegref = 'kg'
road_net = vegnet_to_geojson(kommune, vegref)[1]


class TestSegmenting(unittest.TestCase):

    def setUp(self):
        pass

    def test_distance_road(self):
        '''
        The total distance of the road should be within the margin of error
        given by the variable "margin"
        :return: True or false
        '''
        margin = 15
        max_length = 100
        road = road_net['features'][0]
        road_coordinates = road['geometry']['coordinates']
        distance = calculate_road_length(road_coordinates, max_length, False)[1]
        actual_distance = road['properties']['til_meter'] - road['properties']['fra_meter']
        print(distance, actual_distance)
        self.assertLessEqual(abs(distance - actual_distance), margin)


if __name__ == '__main__':
    unittest.main()
