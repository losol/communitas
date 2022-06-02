import requests
from pyjstat import pyjstat


def get_population_prognosis(region_id):
    api_uri = "https://data.ssb.no/api/v0/en/table/12882/"
    query = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "vs:KommunFram2020Agg",
                    "values": [region_id]
                }
            },
            {
                "code": "Kjonn",
                "selection": {
                    "filter": "item",
                    "values": ["1", "2"]
                }
            },
            {
                "code": "Alder",
                "selection": {
                    "filter": "agg:Funksjonell4",
                    "values": [
                        "F311",
                        "F312",
                        "F313",
                        "F314",
                        "F315",
                        "F316",
                        "F317",
                        "F318",
                        "F319",
                        "F320"
                    ]
                }
            },
            {
                "code": "ContentsCode",
                "selection": {
                    "filter": "item",
                    "values": ["Personer"]
                }
            },
            {
                "code": "Tid",
                "selection": {
                    "filter": "item",
                    "values": list(range(2022, 2051))
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    res = requests.post(api_uri, json=query)
    if(res.status_code != 200):
        print("Error: " + str(res.status_code))
        exit(1)

    ds = pyjstat.Dataset.read(res.text)
    df = ds.write('dataframe')

    return df
