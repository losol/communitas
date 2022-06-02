import dash
from dash import callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_labs as dl
import numpy as np
import plotly.graph_objs as go
from dash import dcc, html
import pandas as pd
import plotly
from datetime import date

from utilities import population

dash.register_page(
    __name__,
    name="Befolkning",
    top_nav=True,
)


def population_table(df, year):
    population_at_year = df[df["year"] == str(year)]

    # Pivot to get males and females on same row
    population_table = pd.pivot_table(
        population_at_year, index=['age'], columns=['sex'])

    # Define order and labels
    life_ages_list = ['0 years',
                      '1-5 years',
                      '6-12 years',
                      '13-15 years',
                      '16-19 years',
                      '20-44 years',
                      '45-66 years',
                      '67-79 years',
                      '80-89 years',
                      '90 years or older']

    population_table = population_table.reindex(life_ages_list)

    # Flatten to make life easier
    flat_population_table = population_table.droplevel(0, axis=1).reset_index()

    return flat_population_table


def layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1(children='Befolkningsprognose'),
                    className="mb-2")
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(children='Prognoser på befolkningssammensetningen. Basert på SSBs tabell 12882: Framskrevet folkemengde 1. januar, etter kjønn og alder, i 9 alternativer (K) 2020 - 2050'),
                    className="lead")
            ]),
            dbc.Row([
                dcc.Dropdown(id='region_selector',
                             options=[
                                 {'label': 'Bodø', 'value': '1804'},
                                 {'label': 'Oslo', 'value': '0301'},
                                 {'label': 'Tromsø', 'value': '5401'}],
                             value="1804")
            ]),
            dbc.Row([
                dcc.Slider(id='year_selector',
                           min=date.today().year,
                           max=2050,
                           value=date.today().year,
                           step=1,
                           marks={
                               2022: '2022',
                               2025: '2025',
                               2030: '2030',
                               2035: '2035',
                               2040: '2040',
                               2045: '2045',
                               2050: '2050'
                           },)
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='population_figure'), width=8)
            ])
        ])
    ])


@callback(
    Output(component_id='population_figure', component_property='figure'),
    Input(component_id='region_selector', component_property='value'),
    Input(component_id='year_selector', component_property='value')
)
def update_population_figure(selected_region_id, selected_year):
    df = population.get_population_prognosis(selected_region_id)
    population_at_year = population_table(df, selected_year)

    y = population_at_year['age']
    males = population_at_year['Males']
    females = population_at_year['Females']

    population_figure = go.Figure()

    # Add Trace to Figure
    population_figure.add_trace(go.Bar(
        y=y,
        x=males * -1,
        name='Menn',
        orientation='h',
        marker_color='#336699'
    ))

    # Add Trace to figure
    population_figure.add_trace(go.Bar(
        y=y,
        x=females,
        name='Kvinner',
        orientation='h',
        marker_color='#336677'
    ))

    # Update Figure Layout
    population_figure.update_layout(
        template='plotly_white',
        title=f'Befolkningspyramide',
        title_font_size=24,
        barmode='relative',
        bargap=0.0,
        bargroupgap=0,
        xaxis=dict(
            tickvals=[-10000, -5000, 0, 5000, 10000],
            title=f'Befolkning fordelt på alder',
            title_font_size=14
        )
    )

    return population_figure
