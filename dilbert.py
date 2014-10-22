#!/usr/bin/env python

"""
Dilbert RSS Feed Generator
Requirements: BeautifulSoup4, PyRSS2Gen
http://github.com/derintendant/dilbert-rss

"""

import urllib3, datetime, sys, PyRSS2Gen
from bs4 import BeautifulSoup

http = urllib3.PoolManager()

def getDetails(url, baseURL):
    request = http.request("GET", url)
    if request.status == 200:
        page = request.data
        soup = BeautifulSoup(page)
        date = soup.findAll('div', {'class': 'STR_DateStrip'})[0].text
        img = soup.findAll('div', {'class': 'STR_Image' })[0].find('img')['src'].replace('sunday.','').replace('strip.gif','strip.zoom.gif')
        results = {}
        results['item'] = PyRSS2Gen.RSSItem(
            title = 'Comic for ' + date,
            description = "<a href='" + url + "'><img src='" + baseURL + str(img) + "' /></a>",
            pubDate = datetime.datetime.strptime(date,"%B %d, %Y"),
            link = url,
            guid = PyRSS2Gen.Guid(url)
        )
        results['prev_href'] = soup.findAll('span', text='Previous')[0].parent['href']
        return results
    else:
        sys.exit(1)

url = 'http://dilbert.com'
request = http.request("GET", url)
if request.status == 200:
    page = request.data
    soup = BeautifulSoup(page)
    nextUrl = url + soup.findAll('div', {'class': 'STR_Image' })[0].find('a')['href']
    strips = []

    for i in range(0,10):
        details = getDetails(nextUrl,url)
        strips.append(details['item'])
        nextUrl = url + details['prev_href']

    # Construct RSS
    rss = PyRSS2Gen.RSS2(
        title = "Dilbert Daily Strip",
        link = "http://dilbert.com",
        description = "An unofficial RSS feed for dilbert.com.",
        lastBuildDate = datetime.datetime.now(),
        items = strips)

    if len(sys.argv) > 1:
        outfile = sys.argv[1]
    else:
        outfile = "dilbert.xml"
    rss.write_xml(open(outfile, "w"))
else:
    sys.exit(1)