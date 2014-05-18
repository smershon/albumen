import colorsys
from albumen import image_analysis

def redness(hls):
    if hls[0] > 0.95 or hls[0] < 0.5:
        return image_analysis.color(hls)
    return 0.0

def greenness(hls):
    if 0.28 < hls[0] < 0.38:
        return image_analysis.color(hls)
    return 0.0

def blueness(hls):
    if 0.62 < hls[0] < 0.72:
        return image_analysis.color(hls)
    return 0.0

class ImageAnalysisV2(image_analysis.ImageAnalysis):

    def add_pixel(self, p):
        hls = colorsys.rgb_to_hls(p[0]/255.0, p[1]/255.0, p[2]/255.0)
        self.pixels += 1
        self.total_red += redness(hls)
        self.total_green += greenness(hls)
        self.total_blue += blueness(hls)
        self.total_saturation += image_analysis.color(hls)
        self.total_lightness += hls[1]
        if self.last is not None:
            self.total_complexity += abs(hls[1] - self.last)
        self.last = hls[1]

