import copy

from calculate_distance import calculate_road_length
from road_fetcher import vegnet_to_geojson


def split_segment(road_segment, max_distance, segmented_road_network, min_gps):
    """
    Recursive function that splits the road segments into two new ones based on input criteria
    :param road_segment: A dict containing the road segment
    :param max_distance: Int. Max distance of a road segment
    :param segmented_road_network: List of new road segments after segmentation
    :param min_gps: Minimum amount of GPS points in a segment
    :return: Final compiled list of all segmented_road_network after being passed down recursively
    """
    coordinates = road_segment['geometry']['coordinates']
    index, meter = (calculate_road_length(coordinates, max_distance, False))
    before_fra_meter = road_segment['properties']['fra_meter']
    before_til_meter = road_segment['properties']['til_meter']

    segment_before_split = copy.deepcopy(road_segment)
    segment_before_split['geometry']['coordinates'] = segment_before_split['geometry']['coordinates'][:index]
    segment_before_split['properties']['til_meter'] = (before_fra_meter + int(meter))
    segment_before_split['properties']['strekningslengde'] = (segment_before_split['properties']['til_meter'] -
                                                              before_fra_meter)

    segment_after_split = copy.deepcopy(road_segment)
    segment_after_split['geometry']['coordinates'] = segment_after_split['geometry']['coordinates'][index:]
    segment_after_split['properties']['fra_meter'] = segment_before_split['properties']['til_meter']
    segment_after_split['properties']['strekningslengde'] = (before_til_meter -
                                                             segment_after_split['properties']['fra_meter'])

    segmented_road_network.append(segment_before_split)

    if check_split(segment_after_split, meter):
        if len(segment_after_split['geometry']['coordinates']) <= min_gps:
            return segmented_road_network.append(road_segment)
        segmented_road_network = split_segment(segment_after_split, meter, segmented_road_network, min_gps)
    else:
        segmented_road_network.append(segment_after_split)
    return segmented_road_network


def check_split(road_segment, max_distance):
    """
    Checks if road_segment is longer than meter, meaning it should be split
    :param road_segment: The road segment you want to check
    :param max_distance: Max length of a road segment
    :return: True or False, True meaning the road segment should be split
    """
    from_meter = road_segment['properties']['fra_meter']
    to_meter = road_segment['properties']['til_meter']
    if (to_meter - from_meter) > max_distance:
        return True
    else:
        return False


def road_segmentor(kommune, vegref, max_distance, min_gps):
    """
    Segments a list of road segments into a new list of shorter segments based on the max_distance
    :param kommune: Int, commune number
    :param vegref: String, road ID
    :param max_distance: Maximum length of a road segment
    :param min_gps: Minimum amount of gps points a road segment can have
    :return: New list of road segments split into shorter lengths
    """
    segmented_road_network = []
    results = vegnet_to_geojson(kommune, vegref)
    count, road_net = results[0], results[1]
    for key, values in road_net.items():
        if key != 'crs':
            for road_segment in range(0, count):
                if check_split(road_net['features'][road_segment], max_distance):
                    split_roads = split_segment(road_net['features'][road_segment],
                                                max_distance, [], min_gps)
                    if split_roads is not None:
                        for new_road in split_roads:
                            segmented_road_network.append(new_road)
                else:
                    segmented_road_network.append(road_net['features'][road_segment])
    return segmented_road_network
