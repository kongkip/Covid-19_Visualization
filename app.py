import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from get_data import filter_by_country, get_countries
import flask

server = flask.Flask(__name__)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

colors = {
    'background': '#ffffff',
    'text': '#111111'
}

confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                        "/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                     "/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                        "/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

countries = confirmed["Country/Region"].unique()

covid_text = """
[WHO explains](https://www.who.int/health-topics/coronavirus)

Coronaviruses (CoV) are a large family of viruses that cause illness ranging from the common cold to more severe 
diseases such as Middle East Respiratory Syndrome (MERS-CoV) and Severe Acute Respiratory Syndrome (SARS-CoV). 

Coronavirus disease (COVID-19) is a new strain that was discovered in 2019 and has not been previously identified in humans.

##### Common signs of infection include respiratory symptoms:
* Fever
* Cough
* Shortness of Breath, and
* Breathing Deficulties

##### In severe cases can cause:
* pneumonia
* severe acute respirtory syndrome
* Kidney failure, and
* Death

## I created this dashboard to give you updates on reported cases
* Keep Calm and Wash your hands
* Select in the dropdown menu below the country of interest; included inside - Cruise Ship
"""

acknowledge = """
## [Project Repo](https://github.com/kongkip/Covid-19_Visualization)
## Acknowledgement:

* Data from [John Hopkins University Repo](https://github.com/CSSEGISandData/COVID-19)
* [WHO](https://www.who.int/)
"""

# %%
app.title = "Covid-19 Reports"

app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(children='Covid-19 World Wide reported cases', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        #     html.Div(children='Covid-19 cases.', style={
        #     'textAlign': 'center',
        #     'color': colors['text']
        # }),
        dcc.Markdown(children=
                     covid_text,
                     style={
                         "margin-top": 40,
                         "margin-left": 50,
                         "margin-right": 30}

                     ),
        dcc.Dropdown(
            id="country",
            options=[
                {'label': i, 'value': i} for i in countries
            ],
            # value=['Thailand'],
            multi=False,
            style={
                "margin-top": 40,
                "margin-left": 20,
                "margin-right": 50}
        ),
        # dcc.Markdown(children=covid_text

        # ),

        dcc.Graph(
            id='cases-data',

        ),

        dcc.Markdown(
            id="explanation",
            # children = """Explanations"""
            style={
                "margin-top": 60,
                "margin-left": 50,
                "margin-right": 50,
                "color": "#0000FF"}
        ),

        dcc.Markdown(
            children=acknowledge,
            style={
                "margin-top": 60,
                "margin-left": 50,
                "margin-right": 50}
        )
    ])


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
                    'size': 15,
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
                    'size': 15,
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
                    'size': 15,
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
    return u""" ## {} Current Reports: 
    
    * Current Confirmed : {}
    * Current Deaths : {}
    * Current Recoveries: {}
    * Date Rate : {}%
    * Recovery Rate : {}%""".format(country, confirmed_current, deaths_current, recovered_current, death_rate,
                                    recovery_rate)


if __name__ == "__main__":
    app.run_server(debug=False)
