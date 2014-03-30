import logging
from optparse import OptionParser
import os
import simplejson as json
import collect
import image_analysis

logging.basicConfig(level=logging.INFO)

def write_meta(meta, filename):
    res = {}
    for val in ('red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'saturation', 'lightness', 'complexity'):
        res[val] = sorted([(os.path.split(k)[-1], getattr(v, val)) for k, v in meta.iteritems()], 
                          key=lambda x: x[1], reverse=True)
    filename.write('%s\n' % json.dumps(res))
        

def main():
    parser = OptionParser()
    parser.add_option('-d', '--image-dir', action='append', dest='image_dirs')
    parser.add_option('-m', '--meta-output', dest='meta_output')
    
    options, args = parser.parse_args()

    ic = collect.ImageCollection()
    for image_dir in options.image_dirs or []:
        ic.add_from_directory(image_dir)

    results = image_analysis.analyze_collection(ic)
    
    if options.meta_output:
        with open(options.meta_output, 'wb') as f:
            write_meta(results, f)

if __name__ == '__main__':
    main()
