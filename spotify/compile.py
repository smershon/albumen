import sys
import playlist
import track2album
import albumimages
import simplejson as json
from optparse import OptionParser
import logging
import datetime

import requests
from PIL import Image
import StringIO

from albumen.produce import squarepack

log = logging.getLogger(__name__)

def album_sort(d):
    def score(row):
        return (len(row), -sum([x[0] for x in row])/float(len(row)), -min([x[0] for x in row]))
    for k,v in sorted(d.items(), key=lambda x: score(x[1]), reverse=True):
        yield k


def images(dd):
    done, skipped = 0, 0
    for album_uri in album_sort(dd):
        image_url = albumimages.get_image(album_uri)
        log.info('Getting %s', image_url)
        if image_url:
            resp = requests.get(image_url)
            try: 
                img = Image.open(StringIO.StringIO(resp.content))
                yield img
                done += 1
                log.info('%d images returned', done)
            except:
                skipped += 1
                log.info('%d images skipped', skipped)
        else:
            skipped += 1
            log.info('%d images skipped', skipped)

def compile(playlist_uri, x, y, n):
    title, tracks = playlist.get_tracks(playlist_uri)
    dd = track2album.tracks2albums(tracks)
    img_src = images(dd) 
    num = len(dd) if not n else min(n, len(dd))
    log.info('Building composite of %d images', num)
    return title, squarepack.build_image(x, y, num, img_src)

def main():
    parser = OptionParser()
    parser.add_option('--size', dest='size', default='2560x1440')
    parser.add_option('--uri', dest='uri')
    parser.add_option('--num', dest='num', type='int')

    options, _ = parser.parse_args()
    if not all([options.size, options.uri]):
        print 'wrong'
        exit()

    strx, stry = options.size.split('x')
    x, y = int(strx), int(stry)

    title, img = compile(options.uri, x, y, options.num)
    user = options.uri.split(':')[2]
    uniq = options.uri.split(':')[-1]
    web_path = 'static/images/%s_%s.png' % (uniq, options.size)
    icon_web_path = 'static/images/%s_%s_small.png' % (uniq, options.size)
    write_path = 'webapp/%s' % web_path
    icon_write_path = 'webapp/%s' % icon_web_path
    metapath = 'webapp/static/meta/%s_%s.json' % (uniq, options.size)
    link = 'https://open.spotify.com/user/%s/playlist/%s' % (user, uniq)
    timestamp = datetime.datetime.now().isoformat()
    doc = {
        'image': web_path,
        'icon': icon_web_path,
        'uri': options.uri,
        'link': link,
        'name': title,
        'owner': user,
        'timestamp': timestamp,
        'size': options.size
    }
    img.save(write_path)
    newsize = (img.size[0]*5/32, img.size[1]*5/32)
    img.thumbnail(newsize, Image.ANTIALIAS)
    img.save(icon_write_path)
    with open(metapath, 'wb') as f:
        f.write(json.dumps(doc))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
