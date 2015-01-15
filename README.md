dilbert-rss
===========

// Updated to work with new site (2015/01/15)//

Scrapes dilbert.com and generates an RSS feed.

Since dilbert.com nerfed their own RSS feed, I created a tool to replicate the old functionality. This is designed to be used on your own server, using `cron` to update it. I don't plan on hosting a replacement feed myself.

You will need to install `BeautifulSoup` and `PyRSS2Gen` using `pip` or otherwise to run this script.

You can run the script by making it executable or by running `python3 dilbert.py`. It takes up to two arguments: The path where the .xml file will be saved, and the number of days to fetch for the feed. By default, the feed is saved in the working directory with ten items.