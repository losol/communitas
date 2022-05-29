import dash_bootstrap_components as dbc
import dash_labs as dl
from dash import Dash

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           plugins=[dl.plugins.pages])
