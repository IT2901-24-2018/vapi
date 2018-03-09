from nvdb_to_geojson import *
from nvdbapi import *
import json

def vegnet_to_file(filename, kommune, vegref):
    full_veg = []
    counter = 0

    vegnett = nvdbVegnett()
    vegnett.addfilter_geo( { 'kommune' : kommune, 'vegreferanse' : vegref })
    veg = vegnett.nesteForekomst()
    while veg:
        full_veg.append(veg)
        counter += 1
        veg = vegnett.nesteForekomst()
    with open(filename, 'w') as outfile:
        print(json.dump(full_veg, outfile, sort_keys = True, indent = 2, separators=(',', ':')))
    return counter

print(vegnet_to_file("roadnet.json", 5001, 'kg'))

