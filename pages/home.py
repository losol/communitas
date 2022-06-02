import dash
import dash_labs as dl
# import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    name="Hjem",
    top_nav=True,
    path="/"
)


def layout():
    return html.Div("Aasdf")
