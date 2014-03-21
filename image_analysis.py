import sys
import Image

def colorsum(hist):
    return sum([i*v for (i,v) in enumerate(hist)])

def normalize(bands):
    return dict([(k, float(v)/max(bands.values())) for k,v in bands.iteritems()])

def main(filename):
    im = Image.open(filename)
    print dir(im)

    hist = im.histogram()
    bands = {}

    offset = 0   
    for band in im.getbands():
        bands[band] = colorsum(hist[offset:(offset+256)])
        offset += 256

    if 'A' in bands:
        del bands['A']
    
    print normalize(bands)
    print im.info

if __name__ == '__main__':
    main(sys.argv[1])
