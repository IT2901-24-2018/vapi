import re

import requests
from road_segmenter import road_segmentor

municipality = 5001
type_of_road = 'kg'
max_distance = 100
min_segments = 2

# Credentials for connecting and writing to the API
API_username = ""
API_password = ""


def filter_road(road):
    """
    Filteres the input road segment to satisfy DB layout.
    :param road: A dictionary containing a road segment
    :return: A filtered dict with the road segment
    """

    unfiltered_coordinates = ', '.join(str(item) for innerlist in road['geometry']['coordinates']
                                       for item in innerlist)
    separated_coordinates = re.sub('(,)([^,]*)(,)', r'\2\3', unfiltered_coordinates)

    filtered_road = {
        'coordinates':     separated_coordinates,
        'from_meter':      road['properties']['fra_meter'],
        'county':          road['properties']['fylke'],
        'srid':            road['properties']['geometri']['srid'],
        'hp':              road['properties']['hp'],
        'href':            road['properties']['href'],
        'category':        road['properties']['kategori'],
        'municipality':    road['properties']['kommune'],
        'connlink':        road['properties']['konnekteringslenke'],
        'shortform':       road['properties']['kortform'],
        'medium':          road['properties']['medium'],
        'startdate':       road['properties']['metadata']['startdato'],
        'number':          road['properties']['nummer'],
        'region':          road['properties']['region'],
        'endnode':         road['properties']['sluttnode'],
        'endposition':     road['properties']['sluttposisjon'],
        'startnode':       road['properties']['startnode'],
        'startposition':   road['properties']['startposisjon'],
        'status':          road['properties']['status'],
        'stretchdistance': road['properties']['strekningslengde'],
        'themecode':       road['properties']['temakode'],
        'to_meter':        road['properties']['til_meter'],
        'typeofroad':      road['properties']['typeVeg'],
        'roadsection':     road['properties']['vegavdeling'],
        'roadsectionid':   road['properties']['veglenkeid'],
        'vrefshortform':   road['properties']['vrefkortform']
    }

    return filtered_road


def format_to_db(municipality, type_road, max_distance, min_segments):
    """
    :return: Returns a filtered road network
    """
    road_network = road_segmentor(municipality, type_road, max_distance, min_segments)
    filtered_road_network = []
    for road in road_network:
        road_done = filter_road(road)
        if road_done['coordinates']:
            filtered_road_network.append(road_done)
    return filtered_road_network


def data_in(municipality, type_road, max_distance, min_segments):
    """
    :return: The status code of the finished post request.
    """
    url = 'http://localhost:8000/api/roadsegments/'
    filtered_network = format_to_db(municipality, type_road, max_distance, min_segments)

    r = requests.post(url, json=filtered_network, auth=(API_username, API_password))
    return "Status: {}\n{}".format(r.status_code, r.text)


if __name__ == '__main__':
    print(data_in(municipality, type_of_road, max_distance, min_segments))
