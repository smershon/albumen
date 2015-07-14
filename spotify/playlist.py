# This is to use the playlist4 service to turn a playlist uri into a list of track uris
import sys
import time
import simplejson as json
from spotify.playlist4.jsonclient import Client

MAX_RETRIES = 5

username = 'stuartmershon'
client = Client('lon', sender='stuart-hackday')

def get_tracks(uri):
    data = None
    for _ in range(MAX_RETRIES):
        try:
            data = client.get_list(uri, username, decorate='attributes')
        except:
            time.sleep(1)
        else:
            break
    if not data:
        return []
    else:
        doc = json.loads(data)
        return doc['attributes'].get('name', 'unknown'), [str(x['uri']) for x in doc['contents'].get('items', [])]

if __name__ == '__main__':
    for track_uri in get_tracks(sys.argv[1]):
        print track_uri
