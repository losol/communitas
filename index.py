import dash
import dash_bootstrap_components as dbc
import dash_labs as dl

from app import app
from whitenoise import WhiteNoise

server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='assets/')

navbar = dbc.NavbarSimple(
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("top_nav")
        ],
    ),
    brand="Helsepanel",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-2",
)


app.layout = dbc.Container(
    dbc.Row(
        [navbar, dl.plugins.page_container]),
    class_name="mb-6",
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
