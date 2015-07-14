import requests
from collections import defaultdict

BASE_URL = 'http://bs-solr.spotify.net/solr/tracks/select/?q=track_uri:"%s"&rows=1&wt=json&fl=album_uri'

def track2album(track):
    resp = requests.get(BASE_URL % track)
    doc = resp.json()
    if doc['response'].get('docs'):
        return doc['response']['docs'][0].get('album_uri')

# IN: [track_uri, track_uri...]
# OUT: { album_uri: [(0, track_uri), (6, track_uri)], 'album_uri: ... }
def tracks2albums(tracks):
    results = defaultdict(list)
    for i,track in enumerate(tracks):
        album = track2album(track)
        if album:
            results[album].append((i, track))
    return results

