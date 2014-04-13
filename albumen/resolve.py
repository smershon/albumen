import urllib2
import xml.etree.ElementTree as ET

def search(artist, title):
    url = 'http://musicbrainz.org/ws/2/release/?query=artist:"%s" AND release:"%s"' % (artist, title)
    url = url.replace(' ', '%20')
    try:
        response = urllib2.urlopen(url)
        doc = ET.fromstring(response.read())
        return [rel.attrib['id'] for child in doc for rel in child]
    except Exception, e:
        print e
        return []

