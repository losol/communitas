import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    name="Hjem",
    top_nav=False,
    path="/"
)


def layout():
    return dbc.Container(children=[
        html.H1("Helsepanel", className="pt-5"),
        html.Div("Under bygging...")
    ])
