from road_fetcher import *
from calculate_distance import *

def split_segment(road_net, road_segment):
    # Main logic for splittig segment
    # TODO Create logic for calling calculate_distance and splitting the segment accordingly
    for coordinate in range(0, len(road_net['features'][road_segment]['geometry']['coordinates'])):
        start_coordinate = (road_net['features'][road_segment]['geometry']['coordinates'][coordinate])[0:2]
    return None


def check_split(road_segment, meter):
    from_meter = road_segment['properties']['fra_meter']
    to_meter = road_segment['properties']['til_meter']
    print(from_meter, to_meter)
    if (to_meter - from_meter) > meter:
        return True
    else:
        return False


def main(kommune, vegref, meter):
    # TODO Clean up the function and segment it correctly
    segmented_road_network = []
    results = vegnet_to_geojson(kommune, vegref)
    count, road_net = results[0], results[1]
    for key, values in road_net.items():
        if key != 'crs':
            for road_segment in range(0, count):
                if check_split(road_net['features'][road_segment], meter):
                    # TODO Segment it and add it to our road network list
                        split_segment(road_net, road_segment)
                else:
                    # TODO Add segment to road network list
                    return None


main(5001, 'kg', 100)
