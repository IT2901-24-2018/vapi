import requests
from road_segmenter import road_segmenter

municipality = 5001
type_of_road = 'kg'
max_distance = 100
min_segments = 2

# Credentials for connecting and writing to the API
try:
    from backend.settings.local import API_AUTHENTICATION
    API_username = API_AUTHENTICATION["username"]
    API_password = API_AUTHENTICATION["password"]
except ImportError:
    API_username = ""
    API_password = ""


def filter_road(road):
    """
    Filteres the input road segment to satisfy DB layout.
    :param road: A dictionary containing a road segment
    :return: A filtered dict with the road segment
    """
    # Quick temporary fix for empty and single point coordinates
    if len(road['geometry']['coordinates']) <= 1:
        return None

    # Format the linestring correctly
    linestring = ''
    for pair in road['geometry']['coordinates']:
        linestring += str(pair[0]) + ' ' + str(pair[1]) + ','
    linestring = linestring.rstrip(',')
    geometry = 'SRID={};LINESTRING({})'.format(road['properties']['geometri']['srid'], linestring)

    filtered_road = {
        'the_geom':        geometry,
        'from_meter':      road['properties']['fra_meter'],
        'county':          road['properties']['fylke'],
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
    road_network = road_segmenter(municipality, type_road, max_distance, min_segments)
    filtered_road_network = []
    for road in road_network:
        road_done = filter_road(road)
        if road_done:
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
