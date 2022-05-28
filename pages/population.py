import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_labs as dl
import plotly.express as px


import requests
from pyjstat import pyjstat


dash.register_page(
    __name__,
    name="Befolkning",
    top_nav=True,
)

api_uri = "https://data.ssb.no/api/v0/en/table/12882/"
query = {
    "query": [
        {
            "code": "Region",
            "selection": {
                "filter": "vs:KommunFram2020Agg",
                "values": ["1804"]
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
                "values": ["2022", "2025", "2030", "2035", "2040", "2050"]
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

print(df)

year = 2025
population_at_year = df[df["year"] == str(year)]

print(population_at_year)

pop_figure = px.bar(data_frame=population_at_year, x="age", y="value")


def layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1(children='Befolkningsprognoser'),
                    className="mb-2")
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(children='Visualising trends across the world'),
                    className="lead")
            ]),

            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=pop_figure, id='pop_figure'), width=8)
            ])
        ])
    ])
