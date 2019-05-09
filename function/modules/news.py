import feedparser
import datetime

words = ["news", "headlines", "trending"]

def parseRSS( rss_url ):
	return feedparser.parse( rss_url ) 
	
def getHeadlines( rss_url ):
	headlines = []
	
	feed = parseRSS( rss_url )
	for newsitem in feed['items']:
		headlines.append(newsitem['title'])
	
	return headlines

def handle(text, ai):
	allheadlines = []
	newsurls = {
		#'apnews':           'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909',
		#'googlenews':       'https://news.google.com/news?ned=us&output=rss',
		'yahoonews':        'http://in.news.yahoo.com/rss',
	}

	for key,url in newsurls.items():
		allheadlines.extend( getHeadlines( url ) )
 	
	ai.text = ""

	for hl in allheadlines[0:10]:
		ai.text +="<br/>"
		print(hl)
		ai.text += hl

def isValid(text):
	keymatch = 0;
	for w in words:
		for t in text:
			if t == w:
				keymatch = keymatch + 1
	return keymatch