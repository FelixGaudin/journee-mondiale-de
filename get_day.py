import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import day_scraper

SITE = "https://www.journee-mondiale.com/"

def use_static_db():

    # as str because of json format
    current_day   = str(datetime.now().day)
    current_month = str(datetime.now().month)

    if not os.path.exists(day_scraper.OUTFILE):
        day_scraper.scrap()
    
    with open(day_scraper.OUTFILE) as events_file:
        events = json.load(events_file)
        if current_month in events and current_day in events[current_month]:
            return events[current_month][current_day]
    
    return []

def get_today_events():

    soup = BeautifulSoup(requests.get(SITE).content, "html.parser")

    container = soup.find("div", {"id": "journeesDuJour"})

    if container == None:
        return use_static_db()

    potentials = container.find_all('h2')

    events = []

    for p in potentials:
        if p.has_attr('itemprop'):
            events.append(p.text)

    return events


if __name__ == "__main__":
    print(get_today_events())