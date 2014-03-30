import colorsys
import functools
import logging
import math

import Image

log = logging.getLogger(__name__)

HUE_RED = 0.0
HUE_GREEN = 1.0/3.0
HUE_BLUE = 2.0/3.0

def huesim(hls, tgt):
    return hls[2]*math.cos(2*math.pi*abs(hls[0] - tgt))

class ImageAnalysis(object):
    def __init__(self):
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
        self.total_saturation += hls[2]
        self.total_lightness += hls[1]
        if self.last is not None:
            self.total_complexity += abs(hls[1] - self.last)
            #self.total_complexity += abs(p[0] - self.last[0]) + abs(p[1] - self.last[1]) + abs(p[2] - self.last[2])
        self.last = hls[1]

    @property
    def red(self):
        return self.total_red/self.pixels

    @property
    def cyan(self):
        return -self.red

    @property
    def green(self):
        return self.total_green/self.pixels

    @property
    def magenta(self):
        return -self.green

    @property
    def blue(self): 
        return self.total_blue/self.pixels

    @property
    def yellow(self):
        return -self.blue
        
    @property
    def saturation(self):
        return self.total_saturation/self.pixels

    @property
    def lightness(self):
        return self.total_lightness/self.pixels

    @property
    def complexity(self):
        return self.total_complexity/self.pixels

def huesim(p, tgt):
    return p[2]*math.cos(2*math.pi*abs(p[0] - tgt))

def analyze(filename):
    im = Image.open(filename)
    analysis = ImageAnalysis()
    for p in im.getdata():
        analysis.add_pixel(p)
    return analysis

def analyze_collection(ic):
    results = {}
    for filename in ic.images:
        log.info('Analyzing %s', filename)
        results[filename] = analyze(filename)
    return results

