import copy

from api.segmenter.calculate_distance import calculate_road_length, calculate_road_length_simple


def split_segment(road_segment, max_distance, segmented_road_network, min_gps):
    """
    Recursive function that splits the road segments into two new ones based on input criteria
    :param road_segment: A dict containing the road segment
    :param max_distance: Int. Max distance of a road segment
    :param segmented_road_network: List of new road segments after segmentation
    :param min_gps: Minimum amount of GPS points in a segment
    :return: Final compiled list of all segmented_road_network after being passed down recursively
    """
    coordinates = road_segment["the_geom"]["coordinates"]
    index, meter = (calculate_road_length(coordinates, max_distance, False))

    segment_before_split = copy.deepcopy(road_segment)
    segment_before_split["the_geom"]["coordinates"] = segment_before_split["the_geom"]["coordinates"][:index]
    segment_before_split["stretchdistance"] = calculate_road_length_simple(
        segment_before_split["the_geom"]["coordinates"])

    segment_after_split = copy.deepcopy(road_segment)
    segment_after_split["the_geom"]["coordinates"] = segment_after_split["the_geom"]["coordinates"][index-1:]
    segment_after_split["stretchdistance"] = calculate_road_length_simple(
        segment_after_split["the_geom"]["coordinates"])

    if len(segment_before_split["the_geom"]["coordinates"]) >= min_gps:
        segmented_road_network.append(segment_before_split)
    else:
        segmented_road_network.append(road_segment)
        return segmented_road_network

    if check_split(segment_after_split, meter):
        if len(segment_after_split["the_geom"]["coordinates"]) <= min_gps:
            segmented_road_network.append(road_segment)
            return segmented_road_network
        segmented_road_network = split_segment(segment_after_split, meter, segmented_road_network, min_gps)
    else:
        if len(segment_after_split["the_geom"]["coordinates"]) >= min_gps:
            segmented_road_network.append(segment_after_split)
    return segmented_road_network


def check_split(road_segment, max_distance):
    """
    Checks if road_segment is longer than meter, meaning it should be split
    :param road_segment: The road segment you want to check
    :param max_distance: Max length of a road segment
    :return: True or False, True meaning the road segment should be split
    """

    if (calculate_road_length_simple(road_segment["the_geom"]["coordinates"])) > max_distance:
        return True
    else:
        return False


def segment_network(road_network, max_distance, min_gps):
    """
    :param road_network: A dict containing the road network. Specified in the wiki
    :param max_distance: Max distance for each road segment
    :param min_gps: Minimum number of gps points for each road segment
    :return: The segmented road network
    """
    segmented_road_network = []
    for road_segment in road_network:
        road_segment["the_geom"] = geometry_to_list(road_segment["the_geom"])

        if road_segment["stretchdistance"] < 1:
            print("Found an invalid stretchdistance:", road_segment["stretchdistance"],
                  ", roadsectionid:", road_segment["roadsectionid"])
            new_distance = calculate_road_length_simple(road_segment["the_geom"]["coordinates"])
            road_segment["stretchdistance"] = new_distance
            print("setting stretchdistance to:", new_distance)

        if len(road_segment["the_geom"]["coordinates"]) > min_gps and check_split(road_segment, max_distance):
            split_roads = split_segment(road_segment, max_distance, [], min_gps)

            if split_roads:
                for new_road in split_roads:
                    segmented_road_network.append(new_road)
        else:
            segmented_road_network.append(road_segment)

    for road_segment in segmented_road_network:
        road_segment["the_geom"] = list_to_geometry(road_segment["the_geom"]["coordinates"],
                                                    road_segment["the_geom"]["srid"])
    return segmented_road_network


def geometry_to_list(geometry):
    """
    Converts the_geom to a dictionary containing SRID and a list of coordinate points
    :param geometry: the_geom in string format
    :return: A ditionary containing srid as a string and coordinates as a 2D list with float values
    """
    coordinates_list = []
    temp = geometry.split(";")
    srid, coordinates = temp[0], temp[1]
    srid = srid[5:]

    temp = coordinates[11:len(coordinates)-1].split(",")
    for pair in temp:
        coord_pair = []
        for number in pair.split(" "):
            coord_pair.append(float(number))
        coordinates_list.append(coord_pair)
    return {"srid": int(srid), "coordinates": coordinates_list}


def list_to_geometry(coord_list, srid):
    """
    Takes a coordinates list and an srid and combines them into the_geom in string format
    :param coord_list: A 2D array of coordinate points with floats as values
    :param srid: srid in string format
    :return: the_geom in string format "SRID=1234;LINESTRING(1 2,3 4,5 6)
    """
    linestring = ""
    for pair in coord_list:
        linestring += str(pair[0]) + " " + str(pair[1]) + ","
    linestring = linestring.rstrip(",")
    geometry = "SRID={};LINESTRING({})".format(srid, linestring)
    return geometry
