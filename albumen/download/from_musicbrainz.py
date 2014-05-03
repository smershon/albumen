import logging
import urllib2
import simplejson as json
import StringIO
from PIL import Image

log = logging.getLogger(__name__)

def _as_list(x):
    if isinstance(x, (list, tuple)):
        return x
    return [x]

def get(mbid):
    url = 'http://coverartarchive.org/release/%s' % mbid

    try:
        response = urllib2.urlopen(url)
    except:
        return
    
    doc = json.loads(response.read())
    for image in doc['images']:
        image_url = image['image']
        try:
            response = urllib2.urlopen(image_url)
            yield Image.open(StringIO.StringIO(response.read()))
        except Exception, e:
            log.error(e)

def image_urls(mbids):
    mbids = _as_list(mbids)
    for mbid in mbids:
        url = 'http://coverartarchive.org/release/%s' % mbid
        log.info('Fetching %s', url)

        try:
            response = urllib2.urlopen(url)
        except:
            log.error('Fetch from %s failed', url)
            continue

        for image_obj in json.loads(response.read())['images']:
            log.info('Image url %s found', image_obj)
            yield image_obj['image']

def from_url(url):
    try:
        request = urllib2.Request(url, headers={'User-Agent': 'Albumen'})
        response = urllib2.urlopen(request)
        return Image.open(StringIO.StringIO(response.read()))
    except Exception, e:
        log.error(e)

def to_dir(img, filepath, width=600, height=600):
    img2 = img.resize((width, height), Image.ANTIALIAS)
    img2.save(filepath)
    img2.filename = filepath
    return img2
