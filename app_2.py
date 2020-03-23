import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
# from get_data import filter_by_country, get_countries
import flask
import pathlib
# from get_data import prepare_data
from get_scraping import get_county_data, get_all_data
import plotly.graph_objects as go

server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device, initial-scale=1"}],
    server=server
)

app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
app.title = "Covid-19 Reports"

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"

all_data = get_all_data()
countries = all_data["Country/Other"].unique()[:193]


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Covid-19 cases"),
                    html.H6("Reports and visualization dashboard")
                ],
            ),
            # html.Div(
            #     id="banner-logo",
            #     children=[
            #         html.Button(
            #             id="learn-more-button", children="LEARN MORE", n_clicks=0
            #         ),
            #         html.Img(id="logo",src=app.get_asset_url("dash-logo-new-png"))
            #     ],
            # )
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Information On Covid-19 ",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=[
                            dcc.Markdown(
                                id="info",
                                children=[
                                    """
                                    # About the Virus
                                    [WHO explains](https://www.who.int/health-topics/coronavirus)

                                    Coronaviruses (CoV) are a large family of viruses that cause illness ranging from 
                                    the common cold to more severe diseases such as Middle East Respiratory Syndrome 
                                    (MERS-CoV) and Severe Acute Respiratory Syndrome (SARS-CoV). 

                                    Coronavirus disease (COVID-19) is a new strain that was discovered in 2019 and 
                                    has not been previously identified in humans. 

                                    ##### Common signs of infection include respiratory symptoms:
                                    * Fever
                                    * Cough
                                    * Shortness of Breath, and
                                    * Breathing Difficulties
                                    ##### In severe cases can cause:
                                    * pneumonia
                                    * severe acute respiratory syndrome
                                    * Kidney failure, and
                                    * Death
                                    ### This dashboard gives you updates on reported cases
                                    * Keep Calm and Wash your hands

                                    ## Acknowledgement:
                                    * [Project Repo](https://github.com/kongkip/Covid-19_Visualization)
                                    * Data from [John Hopkins University Repo](https://github.com/CSSEGISandData/COVID-19)
                                    * [WHO](https://www.who.int/)
                                    """
                                ],
                                style={
                                    "margin-top": 20
                                }
                            )
                        ]
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Visualize Cases",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=[
                            # dcc.Markdown(
                            #     id="total-cases",
                            #     children=["""
                            #         ### Total cases : {}
                            #         ### Total Deaths : {}
                            #         ### Total Recovered : {}
                            #         """.format(total_confirmed, total_deaths, total_recovered)
                            #               ]
                            # ),
                            dcc.Dropdown(
                                id="country",
                                options=[
                                    {'label': i, 'value': i} for i in countries
                                ],
                                multi=False,
                            ),
                            dcc.Graph(
                                id="cases-data"
                            ),
                            dcc.Markdown(
                                id="explanation",
                            )
                        ]
                    ),
                ],
            )
        ],
    )


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs()
            ]
        )
    ]
)


@app.callback(
    Output("cases-data", "figure"),
    [Input("country", "value")]
)
def update_country(country):
    df = get_county_data(country, all_data).iloc[:193]
    colors = ["#0544f2", "#05e2f2", "#fc0f03", "#fc0f03", "#05f74e", "#e7fc03", "#fc9d03"]
    return {
        'data': [
            go.Bar(x=df.columns[1:-1], y=df.values[0][1:-1],
                   marker={"color": colors})
        ],
        'layout':
            go.Layout(title='{} Covid-19 cases'.format(country), barmode='stack')
    }


@app.callback(
    Output("explanation", "children"),
    [Input("country", "value")]
)
def explain(country):
    df = get_county_data(country, all_data).iloc[:193]

    confirmed_current = df["Total_Cases"].values[0]
    deaths_current = df["Total_Deaths"].values[0]
    recovered_current = df["Total_Recovered"].values[0]
    new_cases = df["New_Cases"].values[0]
    new_deaths = df["New_Deaths"].values[0]
    active_cases = df["Active_Cases"].values[0]
    serious_cases = df["Serious_Critical"].values[0]

    death_rate = round((deaths_current / confirmed_current) * 100,3)
    recovery_rate = round((recovered_current / confirmed_current) * 100, 3)
    return u""" #### {} Current Reports: 

    * Current Confirmed : {}
    * Current Deaths : {}
    * Current Recoveries: {}
    * Date Rate : {}%
    * Recovery Rate : {}%
    * New Cases : {}
    * New Deaths : {}
    * Active Cases: {}
    * On critical condition: {}
    """.format(country,
               int(confirmed_current),
               int(deaths_current),
               int(recovered_current),
               death_rate,
               recovery_rate,
               int(new_cases),
               int(new_deaths),
               int(active_cases),
               int(serious_cases))


if __name__ == "__main__":
    app.run_server(debug=False)
