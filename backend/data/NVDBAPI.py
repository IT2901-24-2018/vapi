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
    return convert_veiref(from_vegrefs)


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
    return convert_veiref(to_vegrefs)


def convert_veiref(list_of_veirefs):
    """
    This function converts the Vegrefs from the JSON file to fit the documentation for the vegrefs in the NVDB API.
    :param list_of_veirefs: A list of strings containing the vegrefs
    :return converted_veirefs: A list of the converted vegrefps
    """
    converted_veirefs = []
    for veiref in list_of_veirefs:
        split_veiref = veiref.split("-")
        correct_veiref = str(("5000" + split_veiref[1] + split_veiref[2] + "hp" + split_veiref[3] + "m"
                              + split_veiref[4]))
        converted_veirefs.append(correct_veiref)
    return converted_veirefs


def send_veiref(list_of_veirefs):
    """
    :param list_of_veirefs: A list containing the veirefs
    :return: Not decided yet. 204 error with API-requests so far.
    """
    base_url = "https://www.vegvesen.no/nvdb/api/v2/veg?vegreferanse="
    gathered_calls = []
    for veiref in list_of_veirefs:
        r = requests.get(base_url + veiref)
        if r.status_code == 200:
            gathered_calls.append(r.json())
        else:
            print("Could not perform API call due to status code: ", r.status_code, "on veigref: ", veiref)
    return gathered_calls
