import requests
from bs4 import BeautifulSoup

SITE = "https://www.journee-mondiale.com/"
        
def get_today_events():

    soup = BeautifulSoup(requests.get(SITE).content, "html.parser")

    container = soup.find("div", {"id": "journeesDuJour"})

    potentials = container.find_all('h2')

    events = []

    for p in potentials:
        if p.has_attr('itemprop'):
            events.append(p.text)

    return events
