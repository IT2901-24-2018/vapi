from road_fetcher import *

def split_segment(road_network):
    # Main logic
    return None


def distance_between_utm(list_start, list_end):
    # Calculates the distance between two UTM coordinates so we can properly split it
    #x1, x2
    #y1, y2
    #distance = sqrt((x1-x2)² + (y1-y2)²)
    #do we need to take height into the calculation?
    return None


def check_split(road, meter):
    # check if road segment is too long
    return None


def main(kommune, vegref):
    results = vegnet_to_geojson(kommune, vegref)
    count, road_net = results[0], results[1]
    for key, values in road_net.items():
        if(key != 'crs'):
            for x in range(0, count):
                print(road_net['features'][x]['geometry']['coordinates'][0])
