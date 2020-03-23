import re
import requests
import urllib.request
import time
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

url = "https://www.worldometers.info/coronavirus/#countries"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
# column_names_soup = soup.findAll("tr")[0]
# pattern = re.compile("<th.*?>(.*)</th>")
#
# column_names = []
# for i in column_names_soup.findAll("th"):
#     column_name = pattern.findall(str(i))
#     column_names.append(column_name)

df = pd.DataFrame(data=np.zeros((388, 9)),
                  columns=["Country/Other", "Total_Cases", "New_Cases",
                           "Total_Deaths", "New_Deaths", "Total_Recovered",
                           "Active_Cases", "Serious_Critical", "Total_cases_1m_prop"])

trs = soup.findAll("tr")

a_pattern = re.compile("<a.*?>(.*)</a>")
row_pattern = re.compile("<td.*?>(.*)</td>")


def get_all_data():
    locs = 0
    for i in range(len(trs)):
        i += 1
        rows = trs[i].findAll("td")
        for j in range(len(rows)):
            if j == 0:
                value = rows[j].findAll("a")
                country = a_pattern.findall(str(value))
                if len(country) == 0:
                    country = row_pattern.findall(str(rows[j]))
                j += 1
            else:
                total_cases = row_pattern.findall(str(rows[1]))[0].replace(",", "")
                new_cases = row_pattern.findall(str(rows[2]))[0].replace(",", "").replace("+", "")
                if new_cases == "":
                    new_cases = 0
                total_deaths = row_pattern.findall(str(rows[3]))[0].replace("                                ",
                                                                            "").replace(",", "").replace(' ', "")
                if total_deaths == "":
                    total_deaths = 0
                new_deaths = row_pattern.findall(str(rows[4]))[0].replace(",", "").replace("+", "")
                if new_deaths == "":
                    new_deaths = 0
                total_recovered = row_pattern.findall(str(rows[5]))[0].replace(",", "")
                if total_recovered == "":
                    total_recovered = 0
                active_cases = row_pattern.findall(str(rows[6]))[0].replace(",", "")
                serious_critical = row_pattern.findall(str(rows[7]))[0].replace(",", "")
                if serious_critical == "":
                    serious_critical = 0
                total_cases_1m_prob = row_pattern.findall(str(rows[8]))[0].replace(",", "")
                if total_cases_1m_prob == "":
                    total_cases_1m_prob = 0
        df.iloc[locs] = [country[0], int(total_cases), int(new_cases), int(total_deaths),
                         int(new_deaths), int(total_recovered),
                         int(active_cases), int(serious_critical), float(total_cases_1m_prob)]
        locs += 1
        if locs == 388:
            break
    return df


def get_county_data(country, all_data):
    country_data = all_data[all_data["Country/Other"] == country]
    return country_data
