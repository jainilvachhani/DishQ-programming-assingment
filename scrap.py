import urllib2
from bs4 import BeautifulSoup
import json
from HTMLParser import HTMLParser
import sqlite3

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			for rest_name in attrs:
				if rest_name[0] == 'data-url':
					print(rest_name[1])
					urls.add('https://www.dineout.co.in' + rest_name[1])
					return attrs

def createTable():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS food 
             (name text, url text, latitude real, longitude real, ratings real)''')
	conn.commit()
	conn.close()

def insert(food):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute('INSERT INTO food VALUES (?,?,?,?,?)',food)
	conn.commit()
	conn.close()

def selectAll():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	for row in c.execute('SELECT * FROM food'):
		print row
	conn.commit()
	conn.close()


quote_page = 'https://www.dineout.co.in/bangalore-restaurants?search_str='
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
urls = set([])
i=0
while(True):
	print(i)
	restaurant = soup.find('div', attrs={'class':'listing-card-wrap', 'index': i})
	if(restaurant==None):
		break
	i+=1
	parser = MyHTMLParser()
	parser.feed(str(restaurant))
	print()
print("done first part")
createTable()
for url in urls:
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	print(url) 
	restaurant_details = (soup.find('script', attrs={'type':'application/ld+json'}))
	restaurant_details_json = json.loads(restaurant_details.contents[0])
	name = restaurant_details_json['name']
	url = restaurant_details_json['url']
	latitude = restaurant_details_json['geo']['latitude']
	longitude = restaurant_details_json['geo']['longitude']
	ratings = restaurant_details_json['aggregateRating']['ratingValue']
	food = []
	food.append(name)
	food.append(url)
	food.append(latitude)
	food.append(longitude)
	food.append(ratings)
	insert(food)
selectAll()
