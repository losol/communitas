from dash import Dash
import dash_bootstrap_components as dbc
import dash_labs as dl

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           plugins=[dl.plugins.pages])
