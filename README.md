This project is a Python + FastAPI web application that visualizes electricity prices for 5 cities in Norway. Data is fetched from the Strømpris API and displayed in an interactive GUI, allowing users to:

- View prices for different cities and times of day

- Select specific days to display in the graph

- Compare prices across cities

The API is automatically documented with Sphinx

Features
- Live electricity price data from Strømpris API

- Graph visualization of hourly prices

- City and date selection in the UI

- Automatic API documentation

- Built with Python, Flask, and common data/visualization libraries


Required packages and dependecies:

(requires python version >=3.8 )

Altair (altair==4.*)
Beautiful Soup (beautifulsoup4)
FastAPI (fastapi[all])
pandas
PyTest
Requests
Requests-Cache
Uvicorn

## how to run:

install packages: pip install -e .

open a terminal:

commando: python3 app.py
open the link given in the terminal to display the webpage
press ctrl + C to quit in the terminal
