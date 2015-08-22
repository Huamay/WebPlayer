import urllib2 as urllib
import codecs, re, time
from pyquery import PyQuery as pq
#from lxml import etree
from listgener import MediaItem, RSSDoc

def listgener2():
	doc = pq(url = 'http://carboncook.github.io/WebPlayer/', opener = lambda url, **kw: urllib.urlopen(url).read())
	print doc("title").html()

if __name__ == '__main__':
	listgener2()