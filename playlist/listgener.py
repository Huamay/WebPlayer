import xml.etree.ElementTree as ET
import xml.dom.minidom as mdom

class MediaItem:
    def __init__(self):
        self.title = '(unknown)'
        self.description = '...'
        self.image = None
        self.sources = []
        self.tracks = []

    def setTitle(self, title):
        self.title = title

    def setDescription(self, description):
        self.description = description

    def setImage(self, url):
        self.image = url

    def addSource(self, url, type = 'video/mp4', label = None, default = False):
        self.sources.append(dict(file = url, type = type, label = label, default = default))

    def addTrack(self, url, kind = '', label = None, default = False):
        self.tracks.append(dict(file = url, kind = kind, label = label, default = default))

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
        f = open(filename, 'w')
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
        ET.SubElement(item, 'title').text = mitem.title
        ET.SubElement(item, 'description').text = mitem.description
        if mitem.image is not None:
            ET.SubElement(item, 'jwplayer:image').text = mitem.image
        for source in mitem.sources:
            ET.SubElement(item, 'jwplayer:source', file=source['file'], type=source['type'])
        for track in mitem.tracks:
            ET.SubElement(item, 'jwplayer:track', file=track['file'], kind=track['kind'])

def listgener():
    rssDoc = RSSDoc()
    rssDoc.createChannel('Sample', 'http:/carboncook.github.io/WebPlayer', '...')
    item = MediaItem()
    item.addSource('https://ph2dot.dl.openload.io/dl/l/3gdfWQ70_TU/heyzo0921.mp4')
    rssDoc.addItem(item)
    rssDoc.save('sample.rss')

if __name__ == '__main__':
    listgener()