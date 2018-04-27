import json


def production_data_filter(file_name):
    """
    This function filters the json input data, and returns the
    filtered input as a list of dictionaries.
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

        out_properties = {"time": time, "startlat": startlat, "startlong": startlong,
                          "endlat": endlat, "endlong": endlong}

        # Add the production types/properties if not null.
        if properties["torrsprederaktiv"] is not None:
            out_properties["dry_spreader_active"] = properties["torrsprederaktiv"]
        if properties["plogaktiv"] is not None:
            out_properties["plow_active"] = properties["plogaktiv"]
        if properties["vatsprederaktiv"] is not None:
            out_properties["wet_spreader_active"] = properties["vatsprederaktiv"]
        if properties["materialtype_kode"] is not None:
            # Remove ".0" from "d.0" and cast as int
            out_properties["material_type_code"] = int(properties["materialtype_kode"].rstrip(".0"))

        out_data.append(out_properties)
    return out_data
