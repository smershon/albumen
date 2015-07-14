import sys
import requests

BASE_URL = 'https://api.spotify.com/v1/albums/%s'

def get_image(album_uri):
    resp = requests.get(BASE_URL % album_uri.split(':')[-1])
    doc = resp.json()
    if doc['images']:
        biggest = max(doc['images'], key=lambda x: x['height'])
        return biggest['url']

if __name__ == '__main__':
    print get_image(sys.argv[1])
