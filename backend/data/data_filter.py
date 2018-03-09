import json


def production_data_filter(file_name):
    """
    This function filters the json input data, and returns the
    filtered input as a list dictionaries.
    :param file_name: File path to json input data
    :return out_data: Filtered list of dictionaries
    """
    data = json.load(open(file_name))
    out_data = []

    for feature in data['features']:
        properties = feature["properties"]
        # Format the time string to "YYYY-MM-DDThh:mm:ss" format
        time = properties["time"].replace("/", "-")
        time = time.replace(" ", "T")
        startlat = properties["startlat"]
        startlong = properties["startlong"]
        endlat = properties["endlat"]
        endlong = properties["endlon"]
        torrsprederaktiv = properties["torrsprederaktiv"]
        plogaktiv = properties["plogaktiv"]
        vatsprederaktiv = properties["vatsprederaktiv"]
        materialtype_kode = properties["materialtype_kode"]

        out_properties = {"time": time, "startlat": startlat, "startlong": startlong,
                          "endlat": endlat, "endlong": endlong, "torrsprederaktiv": torrsprederaktiv,
                          "plogaktiv": plogaktiv, "vatsprederaktiv": vatsprederaktiv,
                          "materialtype_kode": materialtype_kode}
        out_data.append(out_properties)
    return out_data
