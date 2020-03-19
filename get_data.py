import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

confirmed = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
    "/time_series_19-covid-Confirmed.csv")
deaths = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
    "/time_series_19-covid-Deaths.csv")
recovered = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
    "/time_series_19-covid-Recovered.csv")


# create a time series data
def get_countries():
    return confirmed["Country/Region"].unique()


def prepare_data(case):
    """
    case:
        pandas data frame for either cofirmed/deaths/recovered
    """
    # select only the columns with time
    case_T = case[case.columns[-54:]].T

    # set columns names to Country/Region
    case_T.columns = case["Country/Region"]

    # transform index to datetime
    case_T.index = pd.to_datetime(case_T.index)

    # sum data of regions in the same country
    regions_count = pd.value_counts(confirmed["Country/Region"]).reset_index()
    regions_count.columns = ["Country/Region", "Counts"]
    to_drop = list(regions_count[regions_count["Counts"] > 1]["Country/Region"].values)
    case_T_copy = case_T.copy()
    case_T_copy = case_T_copy.drop(to_drop, axis=1)
    for i in to_drop:
        case_T_copy[i] = case_T[i].sum(axis=1)

    return case_T_copy


#  filter data by country
def filter_by_country(country, confirmed_prepared, deaths_prepared, recovered_prepared):
    country_all = pd.DataFrame(
        data=
        confirmed_prepared[country].values,
        columns=[
            "Confirmed",
        ],
        index=confirmed_prepared.index
    )

    country_all["Deaths"] = deaths_prepared[country].values
    country_all["Recovered"] = recovered_prepared[country].values
    country_all.index = pd.to_datetime(country_all.index)

    return country_all
