#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache
from datetime import date as d, timedelta

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:



def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Fetches electricity price data for a specific date and location from hvakosterstrommen.no API.

    Args: 
        date (Datetime.date (optional)): The date for which to fetch data. If None, defaults to today's date.
        location (str (optional)): The location code for which to fetch data. Defaults to "NO1".


    Returns: 
        pd.Dataframe : Dataframe containing the fetched data about the prices for the given location and date.
    
    """
    if date is None:
        date = d.today()

    year = date.year
    month = date.month
    day = date.day
    

    #hvis det er ensifret tall
    formatted_month = f'{month:02}'  
    formatted_day = f'{day:02}'
    url = f'https://www.hvakosterstrommen.no/api/v1/prices/{year}/{formatted_month}-{formatted_day}_{location}.json'

    response = requests.get(url) #request objekt
    print(response.raise_for_status())

    if response.status_code !=200:
        raise ValueError("Failed to fetch data!")
        
    
    data = response.json() #json objekt

    nok_prices = []
    time_starts = []

    for entry in data:
        nok_price = entry["NOK_per_kWh"]
        time_start = entry["time_start"]
        if nok_price is not None:  
            nok_prices.append(float(nok_price))
            

        if time_start is not None: 
            time_start = pd.to_datetime(entry["time_start"])
            time_starts.append(time_start)

    
    dataframe_data = {
        "NOK_per_kWh": nok_prices,
        "time_start": time_starts
    }

    df = pd.DataFrame(dataframe_data)
    df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")


    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {"NO1": "Oslo", "NO2": "Kristiansand", "NO3": "Trondheim", "NO4": "Tromsø", "NO5": "Bergen"}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

       Fetches electricity price data for multiple days and locations from hvakosterstrommen.no API.

    Args:
        end_date (datetime.date (optional)): The end date until which to fetch prices. Defaults to today's date.
        days (int (optional)): The number of days to fetch prices for, leading up to the end_date. Defaults to 7.
        locations (list[str] (optional)): The list of locations for which to fetch prices. Defaults to all locations.

    Returns:
        pd.DataFrame: A DataFrame containing prices for multiple days and locations.
    """

    if end_date is None:
        end_date = d.today()

    #alle de 7 dagene fra end_date
    day_list = []
    for i in range(days):
        n_days_ago = end_date - timedelta(i)
        day_list.append(n_days_ago)

   
    day_prices = []
    for location_code in locations:
        for day in day_list:
           
            day_prices_n = fetch_day_prices(day, location_code)
            # Legg til location code og name til DataFrames
            day_prices_n["location_code"] = location_code
            day_prices_n["location"] = LOCATION_CODES.get(location_code, "Unknown Location")
            day_prices_n["date"] = day  # Legg til kolonne for datoen (for plotting)
            day_prices_n["date"] = pd.to_datetime(day_prices_n["date"], utc=True) #???
            
            day_prices.append(day_prices_n)
            
    
    
    final_df = pd.concat(day_prices, ignore_index=True)
  
    return final_df
   

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    Creates a line chart showing energy prices over time for different locations.

    Args:
        df (pd.DataFrame): The DataFrame containing data to plot.

    Returns:
        alt.Chart: A chart visualizing energy prices over time for different locations.
    """
    

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('time_start:T', axis=alt.Axis(title='time_start')), 
        y=alt.Y('NOK_per_kWh:Q', axis=alt.Axis(title='NOK_per_kWh')),
        color='location:N'
    ).properties(
        width=800,
        height=400
    )

    return chart
    


# Task 5.4

#only 4110
def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this optional task")

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
