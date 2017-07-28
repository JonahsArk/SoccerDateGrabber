from lxml import html
from bs4 import BeautifulSoup
from dateutil import parser
import re
import requests
import sys
import getopt
import csv

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
    timepattern = "\d{1}:\d{2} (?:AM|PM)"
    matcher = re.compile(pattern)
    timematcher = re.compile(timepattern)

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
                    info = cell.find('span', text=matcher)                

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
        
        print'Writing...'
        write_output_file(games)
        print 'Wrote to output.csv successfully' 

    except:
        print("Couldn't parse")

def get_valid_string(date):
    newdate = parser.parse(date)
    return newdate 

def write_output_file(games):
    datepattern = "([A-Z])\w+ [0-9]{1,2}[/][0-9]{1,2}"
    timepattern = "\d{1}:\d{2} (?:AM|PM)"
    datematcher = re.compile(datepattern)
    timematcher = re.compile(timepattern)

    with open('output.csv', 'wb') as myfile:
        writer = csv.writer(myfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Subject', 'Start Date', 'Start Time',
                                'Description', 'Location'])

        for item in games:
            date = [x for x in item if datematcher.match(x)]
            time = [x for x in item if timematcher.match(x)]
            combined = ''.join('%s %s' % x for x in zip(date, time))
            gametime = get_valid_string(combined)
            teams = item[2] + ' vs. ' + item[3] 
            writer.writerow(['Soccer', gametime.date(), item[1],
                                teams, item[4]]) 


if __name__ == "__main__":
    main(sys.argv[1:])
