import json


def filter_data(file_name):
    """
    This function filters the json input data, converts linestring to a 2d array, and returns the
    filtered input as a dictionary
    :param file_name: File path to json input data
    :return out_data: Filtered json file as dictionary
    """
    data = json.load(open(file_name))
    out_data = {"features": []}

    for feature in data['features']:
        out_linestring = []

        properties = feature["properties"]
        time = properties["time"].replace("\/", "-")
        startlat = properties["startlat"]
        startlong = properties["startlong"]
        endlat = properties["endlat"]
        endlong = properties["endlon"]
        torrsprederaktiv = properties["torrsprederaktiv"]
        plogaktiv = properties["plogaktiv"]
        vatsprederaktiv = properties["vatsprederaktiv"]
        materialtype_kode = properties["materialtype_kode"]
        from_vegref = properties["from_vegref"]
        to_vegref = properties["to_vegref"]
        id = properties["id"]

        temp = properties["the_geom"].split(";")
        srid = temp[0].lstrip("SRID=")
        temp[1] = temp[1].lstrip("LINESTRING(")
        temp[1] = temp[1].rstrip(")")
        linestring = temp[1].split(",")
        for x in linestring:
            out_linestring.append(x.split(" "))

        the_geom = {"srid": srid, "linestring": out_linestring}

        name = properties["name"]
        description = properties["descriptio"]

        out_properties = {"time": time, "startlat": startlat, "startlong": startlong,
                          "endlat": endlat, "endlong": endlong, "torrsprederaktiv": torrsprederaktiv,
                          "plogaktiv": plogaktiv, "vatsprederaktiv": vatsprederaktiv,
                          "materialtype_kode": materialtype_kode, "from_vegref": from_vegref,
                          "to_vegref": to_vegref, "id": id, "the_geom": the_geom, "name": name,
                          "description": description}

        out_feature = {"type": feature["type"], "properties": out_properties,
                       "geometry": {"type": feature["geometry"]["type"],
                                    "coordinates": feature["geometry"]["coordinates"]}}
        out_data["features"].append(out_feature)
    return out_data
