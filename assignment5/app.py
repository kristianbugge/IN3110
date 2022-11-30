import datetime
from typing import Dict, List, Optional

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory = "templates")
today = (datetime.datetime.today())
minutes = 10

# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date


#create root page
@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(
        "strompris.html",
        {
        "request": request,
        "location_codes": LOCATION_CODES,
        "today": today,
        },
    )

# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

@app.get('/plot_prices.json')
def plot_prices_json(
    end: datetime.date = Query(default=today),
    days: int = Query(default=7),
    locations: Optional[List[str]] = Query(default=None),
    ):
    df = fetch_prices(end, days, locations)
    chart = plot_prices(df)
    return chart.to_dict()


# Task 5.6:
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date

@app.get('/activity')
async def activity(request: Request):
    return templates.TemplateResponse(
        "activity.html",
        {
        "request": request,
        "activity": ACTIVITIES,
        "minutes": minutes,
        "location_codes": LOCATION_CODES,
        "today": today,
        },
    )


# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)

@app.get('/plot_activity.json')
def plot_activity_json(
    minutes: float = Query(default=10),
    activity: Optional[str] = Query(default="shower"),
    locations: Optional[List[str]] = Query(default=None),
    ):
    print(today, minutes, activity, locations)
    print("----------------------------------------------------------------")

    df = fetch_prices(today, 1, locations)
    chart = plot_activity_prices(df, activity, minutes)
    return chart.to_dict()



# mount your docs directory as static files at `/help`

...

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000
    import uvicorn
    uvicorn.run(app, port=5000)
