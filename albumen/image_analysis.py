import colorsys
import functools
import logging
import math
import os

import Image

log = logging.getLogger(__name__)

VERSION = "1.0"

HUE_RED = 0.0
HUE_GREEN = 1.0/3.0
HUE_BLUE = 2.0/3.0

def huesim(hls, tgt):
    return math.cos(2*math.pi*abs(hls[0] - tgt))*color(hls)

def color(hls):
    return (1 - (2*hls[1] - 1)**2) * hls[2]

class ImageAnalysis(object):
    def __init__(self, meta=None):
        self.meta = meta or {}
        self.pixels = 0
        self.total_red = 0.0
        self.total_green = 0.0
        self.total_blue = 0.0
        self.total_saturation = 0.0
        self.total_lightness = 0.0
        self.total_complexity = 0.0
        self.last = None

    def add_pixel(self, p):
        hls = colorsys.rgb_to_hls(p[0]/255.0, p[1]/255.0, p[2]/255.0)
        self.pixels += 1
        self.total_red += huesim(hls, HUE_RED)          	
        self.total_green += huesim(hls, HUE_GREEN)
        self.total_blue += huesim(hls, HUE_BLUE)
        self.total_saturation += color(hls)
        self.total_lightness += hls[1]
        if self.last is not None:
            self.total_complexity += abs(hls[1] - self.last)
        self.last = hls[1]

    def get(self, prop, default=None):
        if not hasattr(self, prop):
            return default
        return getattr(self, prop)

    @property
    def red(self):
        return self.total_red/self.pixels if self.pixels else 0.0

    @property
    def cyan(self):
        return -self.red

    @property
    def green(self):
        return self.total_green/self.pixels if self.pixels else 0.0

    @property
    def magenta(self):
        return -self.green

    @property
    def blue(self): 
        return self.total_blue/self.pixels if self.pixels else 0.0

    @property
    def yellow(self):
        return -self.blue
        
    @property
    def saturation(self):
        return self.total_saturation/self.pixels if self.pixels else 0.0

    @property
    def lightness(self):
        return self.total_lightness/self.pixels if self.pixels else 0.0

    @property
    def complexity(self):
        return self.total_complexity/self.pixels if self.pixels else 0.0

def analyze_file(filename, analysis_class=ImageAnalysis):
    im = Image.open(filename)
    return analyze(im, analysis_class)

def analyze(img, analysis_class=ImageAnalysis):
    analysis = analysis_class(meta={
        'filename': os.path.split(img.filename)[-1],
        'filepath': img.filename,
        'width': img.size[0],
        'height': img.size[1]})
    for p in img.getdata():
        analysis.add_pixel(p)
    return analysis

def analyze_collection(ic):
    results = {}
    for filename in ic.images:
        log.info('Analyzing %s', filename)
        results[filename] = analyze(filename)
    return results

