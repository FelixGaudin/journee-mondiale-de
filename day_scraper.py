import requests
from bs4 import BeautifulSoup
import json

OUTFILE = "events.json"
URL = "https://www.journee-mondiale.com/les-journees-mondiales.htm"

def format_date(datetime):
    mounths = ["janvier", "février", "mars", "avril", "mai", "juin",
              "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    
    day, mounth = datetime.split(" ")
    
    if day == "1er": day = "1"
    day = int(day)

    mounth = mounths.index(mounth) + 1

    return day, mounth

def scrap():
    events = {}
    soup = BeautifulSoup(requests.get(URL).content, "html.parser")
    articles = soup.find_all('article')
    for month in articles:
        month_events = month.find_all('a')
        for day_event in month_events:
            date, event = day_event.contents
            event = event[3:]
            day, month = format_date(date.get("datetime"))

            if not month in events: events[month] = {}
            if not day in events[month]: events[month][day] = []
            
            events[month][day].append(event)
            
    with open(OUTFILE, "w") as outfile:
        json.dump(events, outfile)

if __name__ == "__main__":
    scrap()