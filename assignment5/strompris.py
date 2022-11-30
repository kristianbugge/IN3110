#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
import datetime
import json
import altair as alt
import pandas as pd
import requests
import requests_cache
import io
import numpy as np
# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Make sure to document arguments and return value...

    date: datetime.date object
    location: str object that has a corresponding city name in dict
    returns: fetches the daily prices from hvakosterstrommen.no in a given area, and returns a pd.dataframe based on this data
    """
    if date is None:
        date = datetime.datetime.today()
    month_day = date.strftime("%m-%d")
    year = date.strftime("%y")
    year = "20" + year

    #check if date is after 2/10/2022
    if int(year) <= 2022 and int(date.strftime("%m")) <= 10:
        if int(date.strftime("%d")) <= 2:
            raise ValueError("Date must be after 2nd October 2022")

    url = (
        f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month_day}_{location}.json"
        )
    #get data
    r = requests.get(url)
    url_data = r.json()
    #turn into list of dict

    #We are only interested in NOK price and the time so we remove the others from the dicts
    for data in url_data:
        del data["EUR_per_kWh"]
        del data["EXR"]
        del data["time_end"]


    df = pd.DataFrame(url_data)
    df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")
    return df
# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Make sure to document arguments and return value...
    end_date: datetime.date object
    days: int, number of days BEFORE the end_date we want to get data for
    locations: tuple containing two strings, the area code and city name

    retruns: a merged pd.dataframe which are the dataframes from fetch_day_prices concatted.
    """
    #some checks
    if isinstance(end_date, str):
        time_str = str(end_date)
        end_date = datetime.datetime.strptime(time_str, '%Y-%m-%d')

    if locations is None:
        locations=tuple(LOCATION_CODES.keys())

    if end_date is None:
        end_date = datetime.datetime.today()

    #Create a list of all dataframes with desired dates and locations
    date_list = [end_date - datetime.timedelta(days = x) for x in range(days)]
    data_frames = []
    for location in locations:
        for date in date_list:
            df = fetch_day_prices(date, location)
            df["location_code"] = location
            df["location"] = LOCATION_CODES[location]
            data_frames.append(df)

    #lastly merge all dataframes and return them
    merged = pd.concat(data_frames)
    return merged
# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value

    """
    prices = (
        df.groupby(["location_code", "location", "time_start"])[["NOK_per_kWh"]]
        .sum()
        .reset_index()
    ).copy()
    plot = alt.Chart(prices).mark_line().encode(
        x = "time_start:T",
        y = "NOK_per_kWh:Q",
        color = "location",
        tooltip=[
            "location",
            "time_start",
            "NOK_per_kWh"
        ]
    ).properties(
        width = 700,
        height=400
    )

    return plot

# Task 5.6

ACTIVITIES = {
    "shower": 30,
    "baking": 2.5,
    "heat": 1
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    activity_cost = ACTIVITIES[activity]

    #we only want to plot for today
    df["total_cost"] = df["NOK_per_kWh"] * minutes / 60 * activity_cost
    prices = (
        df.groupby(["location", "time_start"])[["total_cost"]]
        .sum()
        .reset_index()
    ).copy()
    plot = alt.Chart(prices).mark_line().encode(
        x = "time_start:T",
        y = "total_cost:Q",
        color = "location",
        tooltip=[
            "location",
            "time_start",
            "total_cost"
        ]
    ).properties(
        width = 700,
        height=400
    )

    return plot

def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    #chart = plot_prices(df)
    chart = plot_activity_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
