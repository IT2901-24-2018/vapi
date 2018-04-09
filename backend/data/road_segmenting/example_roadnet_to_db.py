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
    filtered_road = {}

    filtered_road['coordinates']        = ', '.join(str(item) for innerlist in road['geometry']['coordinates']
                                                    for item in innerlist)
    filtered_road['from_meter']         = road['properties']['fra_meter']
    filtered_road['county']             = road['properties']['fylke']
    filtered_road['srid']               = road['properties']['geometri']['srid']
    filtered_road['hp']                 = road['properties']['hp']
    filtered_road['href']               = road['properties']['href']
    filtered_road['category']           = road['properties']['kategori']
    filtered_road['municipality']       = road['properties']['kommune']
    filtered_road['connlink']           = road['properties']['konnekteringslenke']
    filtered_road['shortform']          = road['properties']['kortform']
    filtered_road['medium']             = road['properties']['medium']
    filtered_road['startdate']          = road['properties']['metadata']['startdato']
    filtered_road['number']             = road['properties']['nummer']
    filtered_road['region']             = road['properties']['region']
    filtered_road['endnode']            = road['properties']['sluttnode']
    filtered_road['endposition']        = road['properties']['sluttposisjon']
    filtered_road['startnode']          = road['properties']['startnode']
    filtered_road['startposition']      = road['properties']['startposisjon']
    filtered_road['status']             = road['properties']['status']
    filtered_road['stretchdistance']    = road['properties']['strekningslengde']
    filtered_road['themecode']          = road['properties']['temakode']
    filtered_road['to_meter']           = road['properties']['til_meter']
    filtered_road['typeofroad']         = road['properties']['typeVeg']
    filtered_road['roadsection']        = road['properties']['vegavdeling']
    filtered_road['roadsectionid']      = road['properties']['veglenkeid']
    filtered_road['vrefshortform']      = road['properties']['vrefkortform']

    return filtered_road


def format_to_db(kommune, type_road, max_distance, min_segments):
    """
    :return: Returns a filtered road network
    """
    road_network = road_segmentor(kommune, type_road, max_distance, min_segments)
    filtered_road_network = []
    for road in road_network:
        road_done = filter_road(road)
        if road_done['coordinates']:
            filtered_road_network.append(road_done)
    return filtered_road_network


def data_in(kommune, type_road, max_distance, min_segments):
    """
    :return: The status code of the finished post request.
    """
    url = 'http://localhost:8000/api/roadsegments/'
    filtered_network = format_to_db(kommune, type_road, max_distance, min_segments)

    r = requests.post(url, json=filtered_network, auth=(API_username, API_password))
    return "Status: {}\n{}".format(r.status_code, r.text)


if __name__ == '__main__':
    print(data_in(municipality, type_of_road, max_distance, min_segments))

