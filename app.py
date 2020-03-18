import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
from get_data import filter_by_country, get_countries
import flask
import pathlib

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

confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                        "/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                     "/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                        "/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

countries = confirmed["Country/Region"].unique()


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
    df = filter_by_country(country, confirmed, deaths, recovered)
    return {
        'data': [
            dict(
                x=df.index,
                y=df["Confirmed"],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name="Confirmed"
            ),
            dict(
                x=df.index,
                y=df["Deaths"],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name="Deaths"
            ),
            dict(
                x=df.index,
                y=df["Recovered"],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name="Recovered"
            )
        ],
        'layout': dict(
            xaxis={
                'title': "Date"
            },
            yaxis={
                'title': "Number of cases",
            },
            title="{} Covid-19 cases".format(country)

            ,
            margin={'l': 40, 'b': 30, 't': 60, 'r': 20},
            height=450,
            hovermode='closest'
        )
    }


@app.callback(
    Output("explanation", "children"),
    [Input("country", "value")]
)
def explain(country):
    df = filter_by_country(country, confirmed, deaths, recovered)

    confirmed_current = df["Confirmed"].values[-1]
    deaths_current = df["Deaths"].values[-1]
    recovered_current = df["Recovered"].values[-1]

    death_rate = (deaths_current / confirmed_current) * 100
    recovery_rate = (recovered_current / confirmed_current) * 100
    return u""" #### {} Current Reports: 

    * Current Confirmed : {}
    * Current Deaths : {}
    * Current Recoveries: {}
    * Date Rate : {}%
    * Recovery Rate : {}%""".format(country, confirmed_current,
                                    deaths_current,
                                    recovered_current,
                                    death_rate,
                                    recovery_rate)


if __name__ == "__main__":
    app.run_server(debug=False)

