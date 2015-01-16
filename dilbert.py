#!/usr/bin/env python3

"""
Dilbert RSS Feed Generator
Requirements: BeautifulSoup4, PyRSS2Gen
http://github.com/derintendant/dilbert-rss

"""

import urllib3, datetime, sys, PyRSS2Gen
from bs4 import BeautifulSoup

http = urllib3.PoolManager()


outfile = "dilbert.xml"
stripcount = 10

if len(sys.argv) > 1:
	outfile = sys.argv[1]
	if len(sys.argv) > 2:
		try:
			stripcount = int(sys.argv[2])
		except ValueError:
			sys.exit("ERROR: stripcount must be an integer")
		

now = datetime.datetime.today()
year = now.year
month = now.month
day = now.day

strips = []

for i in range(0, stripcount):
	timedelta = datetime.timedelta(days=i)
	currentDate = (now - timedelta)
	currentDay = currentDate.day
	currentMonth = currentDate.month
	currentYear = currentDate.year

	url = "http://dilbert.com/strip/" + str(year) + "-" + str(month) + "-" + str(currentDay)
	request = http.request("GET", url)

	if request.status == 200:
		page = request.data
		soup = BeautifulSoup(page)

		imageURL = soup.find_all('img', {'class':'img-comic'}, limit=1)[0]['src']

		item = PyRSS2Gen.RSSItem(
			title = 'Comic for ' + str(currentYear) + '/' + str(currentMonth) + '/' + str(currentDay),
			description = "<a href='" + url + "'><img src='" + imageURL + "' /></a>",
			pubDate = currentDate,
			link = url,
			guid = PyRSS2Gen.Guid(url)
		)
		strips.append(item)
		progress= (i/stripcount) + (1 / stripcount)
		print("{:.0%}".format(progress))
	else:
		sys.exit("ERROR: dilbert.com could not be contacted")

	# Construct RSS
	rss = PyRSS2Gen.RSS2(
		title = "Dilbert Daily Strip",
		link = "http://dilbert.com",
		description = "An unofficial RSS feed for dilbert.com.",
		lastBuildDate = now,
		items = strips)

	rss.write_xml(open(outfile, "w"))
