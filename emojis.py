import requests
from bs4 import BeautifulSoup

SITE = "https://getemoji.com/"

soup = BeautifulSoup(requests.get(SITE).content, "html.parser")

ps = soup.find_all('p')

for p in ps:
    if p.has_attr('style'):
        if "Segoe UI Emoji" in p['style']:
            for e in list(filter(lambda x: x != "", p.text.split('\n'))):
                print(e, end=" ")
