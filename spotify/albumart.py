import os
from flask import Flask
from flask import render_template
import logging
import simplejson as json

log = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/albumart')
def albumart():
    metas = [x for x in os.listdir('static/meta') if x.endswith('.json')]
    docs = []
    for path in metas:
        with open('static/meta/%s' % path, 'rb') as f:
            doc = json.loads(''.join(f.readlines()))
            docs.append(doc)
    docs.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('albumart.html', docs=docs)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=9090)

