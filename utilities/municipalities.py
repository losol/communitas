import requests
import json


def update_municipalities():
    """Updates the list of norwegian municipalities, and stores it in 'data/Kartverket/municipalities.json'"""

    api_url = "https://ws.geonorge.no/kommuneinfo/v1/kommuner?sorter=kommunenavn"
    req = requests.get(api_url)

    with open('data/Kartverket/municipalities.json', 'wb') as f:
        f.write(req.content)


def read_municipalities():
    with open('data/Kartverket/municipalities.json') as f:
        data = json.load(f)
    return data


def options_list():
    options = []
    for i in read_municipalities():
        if i['kommunenavnNorsk'] == i['kommunenavn']:
            options.append({"label": i['kommunenavnNorsk'],
                            "value": i['kommunenummer']})
        else:
            options.append({"label": f"{i['kommunenavnNorsk']} / {i['kommunenavn']}",
                            "value": i['kommunenummer']})
    return options


def municipality_name(id):
    """Returns an municipality name 

    Parameters
    ----------
    id : str
      The id of the municipality

    Returns
    -------
    str
      a string with the municipality name."""

    for i in read_municipalities():
        if i['kommunenummer'] == id:
            return i['kommunenavn']

    return 'Unknown'


if __name__ == "__main__":
    update_municipalities()
