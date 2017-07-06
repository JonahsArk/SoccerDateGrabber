from lxml import html
from bs4 import BeautifulSoup
import re
import requests

page = requests.get('')
data = page.text
soup = BeautifulSoup(data, "lxml")
pattern = "([A-Z])\w+ [0-9]{1,2}[/][0-9]{1,2}"
matcher = re.compile(pattern)

try:
	for span in soup.find_all('span'):
		
		m = matcher.match(span.get_text())
		if m:	
			print span.get_text() 
			print m.group() 
except:
	print("Couldn't parse")
