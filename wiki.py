import requests
import string
from bs4 import BeautifulSoup



def wikibot(words):
    msg = ""
    url = "https://en.wikipedia.org/wiki/"+words
    url_open = requests.get(url)
    soup = BeautifulSoup(url_open.content, 'html.parser')
    #print(soup)
    details = soup('table', {'class':'infobox'})
    for i in details:
        h = i.find_all('tr')
        for j in h:
            heading = j.find_all('th')
            detail = j.find_all('td')
            if heading is not None and detail is not None:
                for x,y in zip(heading, detail):
                    msg = msg + "*{}*  :: {}".format(x.text, y.text)+"\n"
                    #print("{}  :: {}".format(x.text, y.text))
                    msg = msg + "-------------------\n"
                    #print("---------------------")
    
    for i in range(1,3):
        try:
            msg = msg + "\n*"+ soup('h2')[i].text +"*\n"
            msg = msg + soup('p')[i].text
            #print(soup('h2')[i].text)
            #print(soup('p')[i].text)
            return msg
        except IndexError:
            return "*ERROR -* Please be specific, do you need a quotation or find nearest branch? make sure u involve those words or closely related words."

    

