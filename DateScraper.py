from lxml import html
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
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
        rows = soup.find_all('tr') 

        print 'Website successfully processed'

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
    formatpattern = "%I:%M %p"
    datepattern = "([A-Z])\w+ [0-9]{1,2}[/][0-9]{1,2}"
    timepattern = "\d{1}:\d{2} (?:AM|PM)"
    datematcher = re.compile(datepattern)
    timematcher = re.compile(timepattern)

    with open('output.csv', 'wb') as myfile:
        writer = csv.writer(myfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Subject', 
                            'Start Date', 
                            'Start Time',
                            'End Date',
                       	    'End Time', 
                            'Description', 
                            'Location'])

        for item in games:
            date = [x for x in item if datematcher.match(x)]
            time = [x for x in item if timematcher.match(x)]
            combined = ''.join('%s %s' % x for x in zip(date, time))
            gametime = get_valid_string(combined)
            teams = item[2] + ' vs. ' + item[3] 
            
            oneHourAdded = gametime + relativedelta(hours=+1)	

            writer.writerow(['Soccer', 
                                gametime.date(),
                                gametime.strftime(formatpattern),
                                gametime.date(),
                                oneHourAdded.strftime(formatpattern),
                                teams, 
                                item[4]]) 

if __name__ == "__main__":
    main(sys.argv[1:])
