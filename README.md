PriceChecker
============

A Python program meant to deploy a web server that checks web pages for changes (e.g. changes in price of an item), and serves rss/email/sms to notify users upon a change. Written as part of HackTX hackathon. Currently unfinished. Requires [web.py](http://webpy.org/) and [Requests](http://docs.python-requests.org/en/latest/) to run.

Originally meant to check amazon.com for price changes, but I ran into difficulties, and from what I understand this is because Amazon has deployed measures to defend agains bots scraping their site. Monitoring Google Play has been more successful.

Several things remain to be done here, so see issues to see what needs to be done (though the issues are not necessarily comprehensive). 
