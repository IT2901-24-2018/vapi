def remove_keys(road):
    """
    :param road: A road segment as a dict
    :return: The same road segment without "felt" and "kvalitet".
    """
    road.pop("felt", None)
    road["geometri"].pop("kvalitet", None)
    return road


def remove_height(road_network):
    """
    Removes the height from road_network
    :param road_network: Unformatted geojson road network
    :return: road_network without height
    """
    for road in road_network["features"]:
        for list_coordinates in road["geometry"]["coordinates"]:
            if len(list_coordinates) > 2:
                del list_coordinates[2]
    return road_network


def filter_road(road):
    """
    Filteres the input road segment to satisfy DB layout.
    :param road: A dictionary containing a road segment
    :return: A filtered dict with the road segment
    """
    # Format the linestring correctly
    linestring = ""
    for pair in road["geometry"]["coordinates"]:
        linestring += str(pair[0]) + " " + str(pair[1]) + ","
    linestring = linestring.rstrip(",")
    geometry = "SRID={};LINESTRING({})".format(road["properties"]["geometri"]["srid"], linestring)

    filtered_road = {
        "the_geom":        geometry,
        "county":          road["properties"]["fylke"],
        "href":            road["properties"]["href"],
        "category":        road["properties"]["kategori"],
        "municipality":    road["properties"]["kommune"],
        "startdate":       road["properties"]["metadata"]["startdato"],
        "region":          road["properties"]["region"],
        "status":          road["properties"]["status"],
        "stretchdistance": road["properties"]["strekningslengde"],
        "typeofroad":      road["properties"]["typeVeg"],
        "roadsectionid":   road["properties"]["veglenkeid"],
        "vrefshortform":   road["properties"]["vrefkortform"],
    }

    return filtered_road
