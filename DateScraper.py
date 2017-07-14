from lxml import html
from bs4 import BeautifulSoup
import re
import requests
import sys
import getopt

def main(argv):
    team = ''
    website = ''

    print "reading input..."

    try:
        #supports one word teams only
        #just needs a unique team string
        opts, args = getopt.getopt(argv, "t:w:") 

    except getopt.GetoptError:
        print "error with input"
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-t':
            team = arg
        elif opt == '-w':
            website = arg
    

    print 'parsed team: ' + team + " website: " + website
    scrape_site(team, website)

def scrape_site(team, website):
    games = []
    pattern = "([A-Z])\w+ [0-9]{1,2}[/][0-9]{1,2}"

    try:
        page = requests.get(website)
        data = page.text
        soup = BeautifulSoup(data, 'lxml')
        tables = soup.find_all('table') 

        print 'Website successfully processed'

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
                            print 'Found matching row'
                            isTeam = True

                    if isTeam is not None:
                        games.append(game)
                
        print games 
    except:
        print("Couldn't parse")

if __name__ == "__main__":
    main(sys.argv[1:])
