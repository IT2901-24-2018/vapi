from nvdb_to_geojson import *
from nvdbapi import *
import json

#TODO: Add function for removing fields. Instead of appending veg, append deepcopy without fields

def format_vegnet(kommune, vegref):
    unformated_road_network = []
    counter = 0

    vegnett = nvdbVegnett()
    vegnett.addfilter_geo({'kommune': int(kommune), 'vegreferanse': str(vegref)})
    veg = vegnett.nesteForekomst()
    while veg:
        unformated_road_network.append(veg)
        counter += 1
        veg = vegnett.nesteForekomst()
    formated_road_network = json.dumps(unformated_road_network, sort_keys=True, indent=2, separators=(',', ':'))
    return counter, unformated_road_network, formated_road_network


def format_vegnet_to_file(filename, road_network):
    with open(filename, 'w') as outfile:
        json.dump(road_network, outfile, sort_keys=True, indent=2, separators=(',', ':'))


def vegnet_to_gjson(kommune, vegref):
    v = nvdbVegnett()
    v.addfilter_geo({'kommune': int(kommune), 'vegreferanse': str(vegref)})
    road_network_gjson = vegnett2geojson(v)
    formatted_gjson = json.dumps(road_network_gjson, sort_keys=True, indent=2, separators=(',', ':'))
    return road_network_gjson, formatted_gjson, road_network_gjson[1]


def gjson_to_file(filename, gjson_road_network):
    with open(filename, 'w') as outfile:
        json.dump(gjson_road_network, outfile, sort_keys=True, indent=2, separators=(',', ':'))
