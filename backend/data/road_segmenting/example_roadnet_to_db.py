import requests
from road_segmenter import road_segmentor


def filter_json(road):
    filtered_road = {}

    filtered_road['coordinates']        = ', '.join(str(item) for innerlist in road['geometry']['coordinates']
                                                for item in innerlist)
    filtered_road['fra_meter']          = road['properties']['fra_meter']
    filtered_road['fylke']              = road['properties']['fylke']
    filtered_road['srid']               = road['properties']['geometri']['srid']
    filtered_road['hp']                 = road['properties']['hp']
    filtered_road['href']               = road['properties']['href']
    filtered_road['kategori']           = road['properties']['kategori']
    filtered_road['kommune']            = road['properties']['kommune']
    filtered_road['konnekteringslenke'] = road['properties']['konnekteringslenke']
    filtered_road['kortform']           = road['properties']['kortform']
    filtered_road['medium']             = road['properties']['medium']
    filtered_road['startdato']          = road['properties']['metadata']['startdato']
    filtered_road['nummer']             = road['properties']['nummer']
    filtered_road['region']             = road['properties']['region']
    filtered_road['sluttnode']          = road['properties']['sluttnode']
    filtered_road['sluttposisjon']      = road['properties']['sluttposisjon']
    filtered_road['startnode']          = road['properties']['startnode']
    filtered_road['startposisjon']      = road['properties']['startposisjon']
    filtered_road['status']             = road['properties']['status']
    filtered_road['strekningslengde']   = road['properties']['strekningslengde']
    filtered_road['temakode']           = road['properties']['temakode']
    filtered_road['til_meter']          = road['properties']['til_meter']
    filtered_road['typeveg']            = road['properties']['typeVeg']
    filtered_road['vegavdeling']        = road['properties']['vegavdeling']
    filtered_road['veglenkeid']         = road['properties']['veglenkeid']
    filtered_road['vrefkortform']       = road['properties']['vrefkortform']

    return filtered_road


def format_to_db():

    road_network = road_segmentor(5001, 'kg', 100, 2)
    finished_road_network = []
    for road in road_network:
        road_done = filter_json(road)
        if road_done['coordinates']:
            finished_road_network.append(road_done)
    return finished_road_network


def data_in():
    url = 'http://localhost:8000/api/roadsegments/'
    test = format_to_db()

    #for element in test:
    r = requests.post(url, json=test, auth=('kuk', '1234qweasd'))
    print("Status: {}\n{}".format(r.status_code, r.text))

if __name__ == '__main__':
   data_in()

