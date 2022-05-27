from dash import dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash
import dash_labs as dl
from app import app


navbar = dbc.NavbarSimple(
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("top_nav")
        ],
    ),
    brand="Helsepanel",
    color="primary",
    dark=True,
    className="mb-2",
)


app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
