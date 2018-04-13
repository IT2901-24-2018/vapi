import backend.data.data_filter as filter
import requests

# Credentials for connecting and writing to the API
try:
    from backend.settings.local import API_AUTHENTICATION
    API_username = API_AUTHENTICATION["username"]
    API_password = API_AUTHENTICATION["password"]
except ImportError:
    API_username = ""
    API_password = ""


def data_in():
    url = 'http://localhost:8000/api/prod-data/'
    data = filter.production_data_filter('../../../Driftsdata_SubSet_Small.geojson')

    # Choose a sequence from data
    # roads = data[121:]
    roads = data[1:2]

    print(roads)

    r = requests.post(url, json=roads, auth=(API_username, API_password))
    print("Status: {}\n{}".format(r.status_code, r.text))


if __name__ == '__main__':
    data_in()
