import requests
from pyjstat import pyjstat


selection_5years = {
    "filter": "agg:FemAarigGruppering",
    "values": [
        "F00-04",
        "F05-09",
        "F10-14",
        "F15-19",
        "F20-24",
        "F25-29",
        "F30-34",
        "F35-39",
        "F40-44",
        "F45-49",
        "F50-54",
        "F55-59",
        "F60-64",
        "F65-69",
        "F70-74",
        "F75-79",
        "F80-84",
        "F85-89",
        "F90-94",
        "F95-99",
        "F100G5+"
    ]
}

selection_lifestages = {
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

# Define order and labels
groups_lifestages = ['0 years',
                     '1-5 years',
                     '6-12 years',
                     '13-15 years',
                     '16-19 years',
                     '20-44 years',
                     '45-66 years',
                     '67-79 years',
                     '80-89 years',
                     '90 years or older']

groups_5year = ['0-4 years',
                '5-9 years',
                '10-14 years',
                '15-19 years',
                '20-24 years',
                '25-29 years',
                '30-34 years',
                '35-39 years',
                '40-44 years',
                '45-49 years',
                '50-54 years',
                '55-59 years',
                '60-64 years',
                '65-69 years',
                '70-74 years',
                '75-79 years',
                '80-84 years',
                '85-89 years',
                '90-94 years',
                '95-99 years',
                '100 years or older']


def get_population_prognosis(region_id, selection):
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
                "selection": selection
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
