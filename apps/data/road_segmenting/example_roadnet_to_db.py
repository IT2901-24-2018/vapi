import os

import requests
from road_fetcher import vegnet_to_geojson
from road_filter import filter_road

# This municipality code is Trondheim
municipality = 5001
# This type of road code means k = communal, and g = walkways and bicycle roads
type_of_road = "kg"
# Values used for segmenting
max_distance = 100
min_segments = 2

# Credentials for connecting and writing to the API
API_username = os.environ["API_USERNAME"]
API_password = os.environ["API_PASSWORD"]


def format_to_db(municipality, type_road):
    """
    :return: Returns a filtered road network
    """
    road_network = vegnet_to_geojson(municipality, type_road)[1]["features"]
    filtered_road_network = []
    for road in road_network:
        road_done = filter_road(road)
        filtered_road_network.append(road_done)
    return filtered_road_network


def data_in(municipality, type_road):
    """
    Takes the municipality number and the type of road and gathers the road network, segments it and post it to the API.
    :return: The status code of the finished post request.
    """
    url = "http://localhost:8000/api/roadsegments/"
    filtered_network = format_to_db(municipality, type_road)

    r = requests.post(url, json=filtered_network, auth=(API_username, API_password))
    return "Status: {}\n{}".format(r.status_code, r.text)


if __name__ == "__main__":
    print(data_in(municipality, type_of_road))
