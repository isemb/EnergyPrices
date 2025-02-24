"""
strompris fastapi app entrypoint
"""
import datetime
import os
from typing import List, Optional
import pandas as pd
import requests

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

"""
inp: year(2023), month(02), day(02), location(NO1)
locations: NO1-5 available
url: https://www.hvakosterstrommen.no/api/vi/prices/year/month-day_location.json


"""

@app.get("/", response_class=HTMLResponse)
def render_prices(request: Request):
    """
    Renders the strompris.html template with specific inputs: requst, current date, location codes and chart.

    Args:
        request (Request): The FastAPI Request object.

    Returns:
        TemplateResponse: HTML template containing fetched data for display.
    """
    
    data = fetch_prices(locations=LOCATION_CODES)
    chart = plot_prices(data)

    return templates.TemplateResponse("strompris.html", 
                                      {"request": request, "current_date": datetime.date.today(), "locations": LOCATION_CODES,"chart": chart.to_json()})




@app.get("/plot_prices.json")
def display_chart(locations : List[str]= Query(tuple(LOCATION_CODES.keys())), end: datetime.date=Query(datetime.date.today()), days: int=Query(7)): 
    """
    Fetches energy prices data for specified locations, end date, and number of days.

    Args:
        locations (List[str], optional): List of locations to fetch data for. Defaults to all locations.
        end (datetime.date, optional): End date for fetching data. Defaults to today's date.
        days (int, optional): Number of days to fetch prices for. Defaults to 7.

    Returns:
        dict: A dictionary containing the plot data in JSON format.
    """
    data = fetch_prices(locations=locations, end_date=end, days=days)
    chart = plot_prices(data)
    return chart.to_dict()



# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)



# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date




# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)





# mount your docs directory as static files at `/help`

@app.get("/docs", response_class=HTMLResponse)
def read_docs(request: Request):
    """
    Serve FastAPI documentation using a template named "fast_api_docs.html".

    Args:
        request (Request): The FastAPI Request object.

    Returns:
        TemplateResponse: HTML template containing FastAPI documentation.
    """
    return templates.TemplateResponse("fast_api_docs.html", {"request": request})


@app.get("/help", response_class=HTMLResponse)
async def serve_index(request: Request):
    """
    Serve the index.html file from Sphinx documentation.

    Args:
        request (Request): The FastAPI Request object.

    Returns:
        HTMLResponse: Response containing the content of index.html.
    """
    index_content = ""
    with open("docs/_build/html/index.html", "r") as file:
        index_content = file.read()
    return HTMLResponse(content=index_content, status_code=200)

@app.get("/{file_name}", response_class=HTMLResponse)
async def serve_specific_file(request: Request, file_name: str):
    """
    Serve specific Sphinx-generated HTML files.

    Args:
        request (Request): The FastAPI Request object.
        file_name (str): Name of the file to be served.

    Returns:
        HTMLResponse: Response containing the content of the specified file.
    """
    file_path = f"docs/_build/html/{file_name}"

    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            file_content = file.read()
        return HTMLResponse(content=file_content, status_code=200)
    else:
        return HTMLResponse(content=f"File not found {file_path}", status_code=404)
    
app.mount("/_static", StaticFiles(directory="docs/_build/html/_static"), name="_static")




def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
