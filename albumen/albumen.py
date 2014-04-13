import logging
from optparse import OptionParser
import os
import simplejson as json
import collect
import image_analysis
import analysis_cache

logging.basicConfig(level=logging.INFO)

def main():
    parser = OptionParser()
    parser.add_option('-d', '--image-dir', action='append', dest='image_dirs')
    
    options, args = parser.parse_args()

    ic = collect.ImageCollection()
    for image_dir in options.image_dirs or []:
        ic.add_from_directory(image_dir)

    results = image_analysis.analyze_collection(ic)
    
    analysis_cache.cache_data(results)

if __name__ == '__main__':
    main()
