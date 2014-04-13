import urllib2
import simplejson as json
import StringIO
import Image

def get(mbid):
    url = 'http://coverartarchive.org/release/%s' % mbid

    try:
        response = urllib2.urlopen(url)
    except:
        return None
    
    doc = json.loads(response.read())
    image_url = doc['images'][0]['image']
    print image_url
    try:
        response = urllib2.urlopen(image_url)
        return Image.open(StringIO.StringIO(response.read()))
    except Exception, e:
        print e
        return None
