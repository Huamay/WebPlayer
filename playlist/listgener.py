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


class EndParserError(Exception):
    def __init__(self, value):
        self.value = value


class MainHTMLParser(HTMLParser):
    def __init__(self, item, level):
        HTMLParser.__init__(self)
        self.item = item
        self.level = level
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
        elif self.sta1 == 2 and tag == 'img' and self.level != 0:
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
            if self.level == 0:
                raise EndParserError(self.item.title)
        elif self.sta2 == 2 and tag.lower() == 'script':
            self.sta2 -= 2

    def handle_data(self, data):
        if self.sta1 == 2:
            self.item.setTitle(data)
        elif self.sta2 == 2:
            self.handle_script(data)


def getPages(contents, keyword):
    f = codecs.open(contents, 'r', 'utf-8')
    lines = f.readlines()
    f.close()
    pages = []
    for line in lines:
        page = line.split(' -> ')
        if keyword in page[1].lower():
            pages.append(page)
    return pages

def listgener(contents):
    keyword = 'PRESTIGE'
    rssDoc = RSSDoc()
    rssDoc.createChannel(keyword, 'http:/carboncook.github.io/WebPlayer', '@' + keyword)
    keyword = keyword.lower()

    pages = getPages(contents, keyword);
    count = 80; stime = time.time()
    print 'begin parsing...', time.time() - stime
    for page in pages[count:]:
        req = urllib.Request(page[0])
        htmlDoc = urllib.urlopen(req).read().decode('utf-8')
        item = MediaItem()
        #item.setTitle(page[1])
        mhp = MainHTMLParser(item, 1)
        mhp.feed(htmlDoc)
        rssDoc.addItem(item)
        count += 1
        if count % 10 == 0:
            rssDoc.save(keyword + '_' + str(count) + '.rss')
            print count, time.time() - stime
        #break

    rssDoc.save(keyword + '.rss')

def contgener(filename):
    f = codecs.open(filename, 'a', 'utf-8')

    index = 1; stime = time.time()
    tempItem = MediaItem()
    while True:
        url = 'http://18av.mm-cg.com/di/' + str(index) + '.html'
        req = urllib.Request(url)
        html = urllib.urlopen(req).read().decode('utf-8')
        tempItem.setTitle(None)
        mhp = MainHTMLParser(tempItem, 0)
        try:
            mhp.feed(html)
        except EndParserError as e:
            if e.value is None:
                break
            f.write(url + ' -> ' + e.value + '\n')
        if index % 100 == 0:
            print index, time.time() - stime
        index += 1
    print index

    f.close()

if __name__ == '__main__':
    listgener('18av.conts')
    #contgener('di.conts')