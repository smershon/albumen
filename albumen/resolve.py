import logging
import urllib2
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)

def xml_get(element, path, prefix=''):
    cur = element
    for level in path:
        cur = cur.find('%s%s' % (prefix, level))
    return cur

def search(artist, title):
    url = 'http://musicbrainz.org/ws/2/release/?query=artist:"%s" AND release:"%s"' % (artist, title)
    url = url.replace(' ', '%20')
    log.info(url)
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        doc = ET.fromstring(data)
        data = []
        prefix = '{http://musicbrainz.org/ns/mmd-2.0#}'
        log.info(doc.attrib)
        log.info(doc.tag)
        for child in doc:
            for release in child:
                artist_name = xml_get(release, ['artist-credit', 'name-credit', 'artist', 'name'], prefix).text
                log.info(artist_name)
                album_name = xml_get(release, ['title'], prefix).text
                mbid = release.attrib['id']
                data.append((artist_name, album_name, mbid))
        return data
    except Exception, e:
        log.error(e)
        return []

