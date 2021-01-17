from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
import requests
import time
import os

# Environment Variables: Use your own secret keys
chat_id = os.environ['CHAT_ID']
api_key = os.environ['API_KEY']

biathlon_infos = "https://www.sport.de/biathlon/kalender/"
dict_parsed = {}

# opening connection, grabbing page content and closing connection
uClient = uReq(biathlon_infos)
page_content = uClient.read()
uClient.close()

# html parser
page_soup = soup(page_content, "html.parser")

# get all events
container = (page_soup.find_all("tr"))

for entry in container:

    if entry.find("td", {"class": "hs-date-breaker-col"}):
        date = entry.find("td", {"class": "hs-date-breaker-col"}).text
    else:
        gender = 'Männer' if 'male' in (entry['class']) else 'Frauen'
        mytime = entry.find("td", {"class": "calendar-date"}).text
        try:
            country = entry.find("td", {"class": "country-flag"}).img['alt']
        except AttributeError:
            country = "-"
        region = entry.find("td", {"class": "calendar-competition-name"}).text
        event = entry.find("td", {"class": "calendar-event"}).text

        # add new node
        if date not in dict_parsed:
            dict_parsed[date] = [
                {'Uhrzeit': mytime, 'Land': country, 'Region': region, 'Event': event, 'Geschlecht': gender}]
        # if node already exists
        else:
            dict_parsed[date].append(
                {'Uhrzeit': mytime, 'Land': country, 'Region': region, 'Event': event, 'Geschlecht': gender})

# sending notification on telegram
print("Das Programm ist aktiv...")
while True:
    date = datetime.now().strftime('%d.%m.%Y')
    now = str(datetime.now().strftime('%H:%M')) + "h"
    if date in dict_parsed:
        events = dict_parsed[date]
        for event in events:
            if event['Uhrzeit'] == now:
                message = "Jetzt " + event['Event'] + " der " + event['Geschlecht'] + " in " + event['Region'] + " (" + \
                          event['Land'] + ")"
                raw_url = 'https://api.telegram.org/bot' + api_key + '/' \
                          'sendMessage?chat_id=' + str(chat_id) + '&text="{}"'.format(message)
                requests.get(raw_url)
    time.sleep(600)
