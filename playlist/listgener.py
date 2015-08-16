import xml.etree.ElementTree as ET
import xml.dom.minidom as mdom
import urllib2 as urllib
from HTMLParser import HTMLParser
import codecs, re, time

class MediaItem:
    def __init__(self):
        self.title = None
        self.description = '...'
        self.image = None
        self.sources = []
        self.tracks = []
        self.previews = []

    def setTitle(self, title):
        self.title = title

    def setDescription(self, description):
        self.description = description

    def setImage(self, url):
        self.image = url

    def addSource(self, url, type = None, label = None, default = False):
        self.sources.append(dict(file = url, type = type, label = label, default = default))

    def addTrack(self, url, kind = '', label = None, default = False):
        self.tracks.append(dict(file = url, kind = kind, label = label, default = default))

    def addPreview(self, url):
        self.previews.append(url)


class RSSDoc:
    def __init__(self):
        #ET.register_namespace('jwplayer',"http://rss.jwpcdn.com/")
        root_attrs = {
            'version': '2.0',
            #'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
            'xmlns:jwplayer': 'http://rss.jwpcdn.com/'
        }
        self.root = ET.Element('rss', root_attrs)
        self.etree = ET.ElementTree(self.root)
        self.channel = None

    def save(self, filename):
        reparsed = mdom.parseString(ET.tostring(self.root, 'utf-8'))
        f = codecs.open(filename, 'w', 'utf-8')
        reparsed.documentElement.writexml(f, addindent = '  ', newl = '\n')
        f.close()

    def createChannel(self, title = '', link = '', description = '', extra = {}):
        if self.channel is not None:
            return self.channel
        self.channel = ET.SubElement(self.root, 'channel')
        ET.SubElement(self.channel, 'title').text = title
        ET.SubElement(self.channel, 'link').text = link
        ET.SubElement(self.channel, 'description').text = description
        for item in extra.items():
            print item[0], item[1]
            ET.SubElement(self.channel, item[0]).text = item[1]
        return self.channel

    def addItem(self, mitem):
        if self.channel is None:
            self.createChannel()
        item = ET.SubElement(self.channel, 'item')
        ET.SubElement(item, 'jwplayer:title').text = mitem.title
        ET.SubElement(item, 'jwplayer:description').text = mitem.description
        if mitem.image is not None:
            ET.SubElement(item, 'jwplayer:image').text = mitem.image
        for source in mitem.sources:
            ET.SubElement(item, 'jwplayer:source', file=source['file'], label=source['label'])
        for track in mitem.tracks:
            ET.SubElement(item, 'jwplayer:track', file=track['file'], kind=track['kind'])
        for preview in mitem.previews:
            ET.SubElement(item, 'preview').text = preview


class InnerHTMLParser(HTMLParser):
    def __init__(self, item):
        HTMLParser.__init__(self)
        self.item = item
        self.sta1 = 0 #for iframe
        self.count = 0 #count iframes

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.item.addPreview(attr[1])
        elif tag == 'iframe':
            for attr in attrs:
                if attr[0] == 'src':
                    self.handle_embedded(attr[1])

    def handle_embedded(self, link):
        req = urllib.Request(link)
        html = urllib.urlopen(req).read().decode('utf-8')
        searcher = re.compile(r'Component\("(.*)"\)')
        match = searcher.search(html)
        self.count += 1
        if match is None:
            print 'No file link found', self.item.title, link
            return
        self.item.addSource(match.groups()[0], label = 'Part ' + str(self.count))


class NoKeywordFoundError(Exception):
    def __init__(self, value):
        self.value = value


class MainHTMLParser(HTMLParser):
    def __init__(self, item, keyword):
        HTMLParser.__init__(self)
        self.item = item
        self.keyword = keyword
        self.sta1 = 0; self.sta2 = 0 #for title and inner html

    def handle_script(self, script):
        inner_html = ''
        try:
            start = script.index('\'<') + 1
            end = script.index('\'', start)
            inner_html = script[start:end]
        except ValueError:
            print self.item.title
            return
        InnerHTMLParser(self.item).feed(inner_html)

    def handle_starttag(self, tag, attrs):
        if tag == 'h1' and len(attrs) == 0:
            self.sta1 += 1
        elif self.sta1 == 1 and tag == 'a':
            self.sta1 += 1
        elif self.sta1 == 2 and tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.item.setImage(attr[1])
        elif tag.lower() == 'span':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == 'main':
                    self.sta2 += 1
                    return
        elif self.sta2 == 1 and tag.lower() == 'script':
            self.sta2 += 1

    def handle_endtag(self, tag):
        if tag == 'h1' and self.sta1 == 1:
            self.sta1 -= 1
        elif self.sta1 == 2 and tag == 'a':
            self.sta1 -= 1
            if self.item.title is None or self.item.title.lower().find(self.keyword) == -1:
                raise NoKeywordFoundError(self.item.title)
        elif self.sta2 == 2 and tag.lower() == 'script':
            self.sta2 -= 2

    def handle_data(self, data):
        if self.sta1 == 2:
            self.item.setTitle(data)
        elif self.sta2 == 2:
            self.handle_script(data)


def listgener():
    keyword = 'PRESTIGE'
    rssDoc = RSSDoc()
    rssDoc.createChannel(keyword, 'http:/carboncook.github.io/WebPlayer', '@' + keyword)
    keyword = keyword.lower()

    index = 6799; count = 0; stime = time.time()
    while True:
        req = urllib.Request('http://18av.mm-cg.com/18av/' + str(index) + '.html')
        htmlDoc = urllib.urlopen(req).read().decode('utf-8')
        item = MediaItem()
        mhp = MainHTMLParser(item, keyword)
        try:
            mhp.feed(htmlDoc)
        except NoKeywordFoundError:
            if item.title is None:
                break
        if item.title.lower().find(keyword) >= 0:
            rssDoc.addItem(item)
            count += 1
            if count % 10 == 0:
                rssDoc.save(keyword + '_' + str(count) + '.rss')
        if index % 100 == 0:
            print index, count, time.time() - stime
        index += 1
        break

    rssDoc.save(keyword + '.rss')

if __name__ == '__main__':
    listgener()