#!/usr/bin/env python3

"""
Dilbert RSS Feed Generator
Requirements: BeautifulSoup4, PyRSS2Gen
https://github.com/derintendant/dilbert-rss

"""

import urllib3, datetime, sys, PyRSS2Gen, argparse
from bs4 import BeautifulSoup

urllib3.disable_warnings()
http = urllib3.PoolManager()
parser = argparse.ArgumentParser()

parser.add_argument("outfile", nargs="?", default="dilbert.xml", help="Write the RSS output to this file")
parser.add_argument("stripcount", type=int, nargs="?", default="10", help="Number of days to parse")
parser.add_argument("--debug", action="store_true", help="Turn on debug mode")
args = parser.parse_args()

debug = args.debug
outfile = args.outfile
stripcount = args.stripcount

if debug:
	print("Will fetch {:d} comics and store in {:s}".format(stripcount,outfile))

now = datetime.datetime.today()

strips = []

for i in range(0, stripcount):
	timedelta = datetime.timedelta(days=i)
	currentDate = (now - timedelta)

	url = "https://dilbert.com/strip/" + currentDate.strftime("%Y-%m-%d")
	request = http.request("GET", url)

	if request.status == 200:
		page = request.data
		soup = BeautifulSoup(page, "html5lib")

		imageURL = soup.find_all('img', {'class':'img-comic'}, limit=1)[0]['src']
 		if currentDate.weekday() == 6:
 			img_type = ".jpg"
 		else:
 			img_type = ""

		item = PyRSS2Gen.RSSItem(
			title = 'Comic for ' + currentDate.strftime("%B %d, %Y"),
			description = "<a href='" + url + "'><img src='" + imageURL + img_type + "' /></a>",
			pubDate = currentDate.strftime("%B %d, %Y"),
			link = url,
			guid = PyRSS2Gen.Guid(url)
		)
		strips.append(item)
		if debug:
			progress = (float(i)/float(stripcount) + 1.0/float(stripcount)) * 100.0
			print("{:.0f}%".format(progress))
	else:
		sys.exit("ERROR: dilbert.com could not be contacted")

	# Construct RSS
	rss = PyRSS2Gen.RSS2(
		title = "Dilbert Daily Strip",
		link = "https://dilbert.com",
		description = "An unofficial RSS feed for dilbert.com.",
		lastBuildDate = now,
		items = strips)

	rss.write_xml(open(outfile, "w"))
