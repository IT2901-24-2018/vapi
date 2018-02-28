import json
import requests


def get_from_vegref(file_name_path):
    """
    This function will return the from_vegref from the converted DAU data. Returns a list
    :param file_name_path: File path to json input data
    :return: from_vegref: From vegref in the data as strings
    """

    open_data = json.load(open(file_name_path))
    from_vegrefs = []

    for feature in open_data['features']:
        properties = feature["properties"]
        from_vegrefs.append(str(properties["from_vegref"]))
    return convert_vegref(from_vegrefs)


def get_to_vegref(file_name_path):
    """
    Returns a list containing the to_vegref data from a JSON file.
    :param file_name_path: Path to the JSON file.
    :return: List containing the vegrefs. Strings
    """
    open_data = json.load(open(file_name_path))
    to_vegrefs = []

    for feature in open_data['features']:
        properties = feature["properties"]
        to_vegrefs.append(str(properties["to_vegref"]))
    return convert_vegref(to_vegrefs)


def convert_vegref(list_of_vegrefs):
    """
    This function converts the Vegrefs from the JSON file to fit the documentation for the vegrefs in the NVDB API.
    :param list_of_vegrefs: A list of strings containing the vegrefs
    :return converted_vegrefs: A list of the converted vegrefps
    """
    converted_vegrefs = []
    for vegref in list_of_vegrefs:
        split_vegref = vegref.split("-")
        correct_vegref = str(("5000" + split_vegref[1] + split_vegref[2] + "hp" + split_vegref[3] + "m"
                              + split_vegref[4]))
        converted_vegrefs.append(correct_vegref)
    return converted_vegrefs


def get_vegref_info(list_of_vegrefs):
    """
    :param list_of_vegrefs: A list containing the vegrefs
    :return: gathered_calls: A list containing JSON objects as dicts.
    """
    base_url = "https://www.vegvesen.no/nvdb/api/v2/veg?vegreferanse="
    gathered_veg = []
    for vegref in list_of_vegrefs:
        r = requests.get(base_url + vegref)
        if r.status_code == requests.codes.ok:
            gathered_veg.append(r.json())
        else:
            print("Could not perform API call due to status code: ", r.status_code, "on veggref: ", vegref)
    return gathered_veg


def get_veglenke_info(gathered_veg):
    """
    :param gathered_veg: A list containing dicts
    :return: A list containing all the api requests. Data added to a list as dicts
    """
    base_url = "https://www.vegvesen.no/nvdb/api/v2/vegnett/lenker/"
    gathered_vegnett = []
    for veg in gathered_veg:
        vegref_id = str(veg['veglenke']['id'])
        r = requests.get(base_url + vegref_id)
        if r.status_code == requests.codes.ok:
            print(r.json())
            gathered_vegnett.append(r.json())
        else:
            print("Could not perform API call due to status code: ", r.status_code, "on road: ", vegref_id)
    return gathered_vegnett
