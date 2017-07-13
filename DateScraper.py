from lxml import html
from bs4 import BeautifulSoup
import re
import requests

team = ''
games = []
page = requests.get('')
data = page.text
soup = BeautifulSoup(data, "lxml")
pattern = "([A-Z])\w+ [0-9]{1,2}[/][0-9]{1,2}"
matcher = re.compile(pattern)

try:
    tables = soup.findAll('table') 

    for table in tables:
        rows = table.findChildren('tr') 

        for row in rows:
            cell = row.find('td')
            info = None

            if cell is not None:
                info = cell.find('span', text=re.compile(pattern))                

            if info is not None:
                isTeam = None
                game = []
                game.append(info.text)

                for col in cell.find_next_siblings('td'):
                    game.append(col.find('span').text)

                    if isTeam is None and team in col.find('span').text:
                        isTeam = True

                if isTeam is not None:
                    games.append(game)
                
    print games 
except:
    print("Couldn't parse")
