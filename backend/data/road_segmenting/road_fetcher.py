import json

from nvdb_to_geojson import vegnett2geojson
from nvdbapi import NvdbVegnett
from road_filter import remove_keys


def format_vegnet(kommune, vegref):
    """
    Gathers road networks and formats it to be written to terminal, file or used by another program.
    :param kommune: Municipality number
    :param vegref: Vegreferanse for the road you want to gather the network for
    :return: Counter - number of road segments. Unformated_road_network - 1 line road network,
    formated_road_network - formated road network(duh)
    """
    raw_road_network = []
    counter = 0

    vegnett = NvdbVegnett()
    vegnett.addfilter_geo({'kommune': int(kommune), 'vegreferanse': str(vegref)})
    veg = vegnett.nesteForekomst()
    while veg:
        raw_road_network.append(remove_keys(veg))
        counter += 1
        veg = vegnett.nesteForekomst()
    formated_road_network = json.dumps(raw_road_network, sort_keys=True, indent=2, separators=(',', ':'))
    return counter, raw_road_network, formated_road_network


def vegnet_to_geojson(kommune, vegref):
    """
    :param kommune: Municipality number
    :param vegref: Vegreferanse for the road you want to gather the network for
    :return: Counter - number of road segments. Raw_road_network - Raw 1 line geojson,
    formated_geojson - formated geojson readibly by the human mind(duh)
    """
    v = NvdbVegnett()
    v.addfilter_geo({'kommune': int(kommune), 'vegreferanse': str(vegref)})
    raw_geojson, counter = vegnett2geojson(v)
    formatted_geojson = json.dumps(raw_geojson, sort_keys=True, indent=2, separators=(',', ':'))
    return counter, raw_geojson, formatted_geojson


def road_network_to_file(filename, road_network):
    """
    :param filename: Name of the file and the extension
    :param road_network: Unformatted geojson road network or raw_road_network
    :return: Nothing. Produces a file
    """
    with open(filename, 'w') as outfile:
        json.dump(road_network, outfile, sort_keys=True, indent=2, separators=(',', ':'))
