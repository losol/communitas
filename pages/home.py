from dash import dash, html


from dash import dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash
import dash_labs as dl


dash.register_page(
    __name__,
    name="Hjem",
    top_nav=True,
    path="/"
)


def layout():
    return html.Div("Aasdf")
