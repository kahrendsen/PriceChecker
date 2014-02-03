import unicodedata
import web
from decimal import Decimal
import time
from threading import Thread
import requests
from bs4 import BeautifulSoup
render=web.template.render('templates/')
urls = (
	'/','index'
)
db = web.database(dbn='mysql', user='root', pw = '', db = 'db')

counter = 0
class checker(Thread):
	terminate=False
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print("Began monitoring prices")
		while True:#not self.terminate:
			time.sleep(2.0)
			#global counter
			#print(counter)
			#counter+=1
			table = db.select('users',where='user=\'default\'')
			for row in table:
				r = requests.get(row.url)
				soup = BeautifulSoup(r.text)
				p = soup.find("meta", itemprop = 'price')['content'].replace("$","")
				newPrice=0
				if p != 'Free':
					newPrice = float(p)
				oldPrice = row.curprice
				basePrice= row.baseprice
				targetPrice = row.targetprice
				if newPrice < targetPrice and newPrice != oldPrice:
					print("Got it")
					#We'll eventually send emails/texts/rss here
					
				if newPrice != oldPrice:
					db.update('users',where = "id=" + str(row.id), curprice = newPrice)
			

	def terminate():
		self.terminate=True


class index:

	def POST(self):
		#Here we handle the form for more urls
		print("Got to POST")
		userData = web.input()
		r = requests.get(userData.inputurl)
		soup = BeautifulSoup(r.text)
		#f = open('lookhere.txt','w')
		#f.write(soup.prettify())
		
		itemName = soup.find("title").string[:len(soup.find("title").string)-30]#itemprop="name", class_ = "document-title").contents[0].string
		print("THE TITLE IS "+itemName)
		username = 'default'
		print soup.find("meta",itemprop="price")
		p = soup.find("meta",itemprop="price")['content'].replace("$","")
		curPrice=0
		if p != 'Free':
			curPrice = float(p)
		targetPrice = curPrice
		basePrice = curPrice
		db.insert('users',user=username,baseprice=basePrice,curprice=curPrice,targetprice=targetPrice,itemname=itemName, url=userData.inputurl)
		return render.index(db.select("users",where="user=\'default\'"))

		
		
		
	
	def GET(self):
		#figure out the user, render the page accordingly
		#todos = db.select('todo')
		
		print("Got to GET")
		#r = requests.get()	
		#page = r.text
		#print(page.find("actualPriceValue"))
		#print(page)
		#soup = BeautifulSoup(page)
		#print(soup.prettify())
		table = db.select('users',where='user=\'default\'')
		return render.index(table)
		#i=web.input(name=None)
		#return render.index(i.name)

	

		
	



if __name__ == "__main__":
	#r = requests.get("http://www.amazon.com/Google-Nexus-10-Wi-Fi-only/dp/B00ACVHKSC/ref=sr_1_1?ie=UTF8&qid=1384578904&sr=8-1&keywords=nexus+10")
	#soup = BeautifulSoup(r.text)
	
	#x = soup.prettify()
	#x = x.encode('ascii', 'ignore')
	#print x
	
	t = checker()
	t.start()
	app=web.application(urls,globals())
	app.run()
	
