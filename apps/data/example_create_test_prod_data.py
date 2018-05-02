import os

import data_filter
import requests

# Credentials for connecting and writing to the API
API_username = os.environ["API_USERNAME"]
API_password = os.environ["API_PASSWORD"]


def data_in():
    url = "http://localhost:8000/api/prod-data/"
    prod_data_path = "../Driftsdata_SubSet_Small.geojson"
    data = data_filter.production_data_filter(os.path.join(os.path.dirname(os.path.realpath(__file__)), prod_data_path))

    # Choose a sequence from data
    # roads = data[121:]
    roads = data

    r = requests.post(url, json=roads, auth=(API_username, API_password))
    print("Status: {}\n{}".format(r.status_code, r.text))


if __name__ == "__main__":
    data_in()
