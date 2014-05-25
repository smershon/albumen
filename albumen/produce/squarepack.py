import math
import random
import sys
import os

import Image

from pprint import pprint

from albumen import analysis_cache

def random_iterate(src):
    new_src = list(src)
    for _ in range(len(new_src)):
        x = random.choice(new_src)
        yield x
        new_src.remove(x)

class ImageGrid(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = self.x * self.y
        self.data = {}
        for i in range(self.x):
            for j in range(self.y):
                self.data[(i,j)] = [1, ''] 

    def join(self, i, j):
        self.data[(i,j)][0] += 1
        del self.data[(i+1, j)]
        del self.data[(i, j+1)]
        del self.data[(i+1, j+1)]
        self.size -= 3

    def unjoin(self, i, j):
        if (i, j) not in self.data or self.data[(i,j)][0] == 1:
            return
        self.data[(i,j)][0] -= 1
        self.data[(i+1, j)] = [1, '']
        self.data[(i, j+1)] = [1, '']
        self.data[(i+1, j+1)] = [1, '']
        self.size += 3

    def possible_joins(self):
        candidates = []
        for i in range(self.x - 1):
            for j in range(self.y - 1):
                if self._can_join(i,j):
                    candidates.append((i,j))
        return candidates

    def _can_join(self, i, j):
        for coords in ((i,j), (i+1,j), (i,j+1), (i+1,j+1)):
            if coords not in self.data:
                return False
            if self.data[coords][0] != 1:
                return False
        return True       

    def cells_by_size(self):
        for cell in sorted(self.data.items(), key=lambda x: x[1][0], reverse=True):
            yield cell

def gen_grid(x, y, n):
    """
        x - max number of cells horizontally
        y - max number of cells vertically
        n - number of images to fit (if n >= x*y, return x*y)
    """
    g = ImageGrid(x, y)

    if n < (x*y - 3*((x/2) * (y/2))):
        # Dirty hack so impossible reductions don't take forever
        return None

    if not grid_reduce(g, n):
        return None
    return g    

def grid_reduce(g, n):
    if g.size <= n:
        return True
    candidates = g.possible_joins()
    if not candidates:
        return False
    for coord in random_iterate(candidates):
        g.join(*coord)
        if grid_reduce(g, n):
            return True
        else:  
            g.unjoin(*coord)
    return False

def gen_image(g, attr, cell=100):
    img = Image.new('RGBA', (cell*g.x, cell*g.y))
    sources = [x.meta['filename'] for x in analysis_cache.get_images(sort_field=attr)]
    for coord, spec in g.cells_by_size():
        src = sources.pop(0)
        src_img = Image.open('samples/%s' % src).resize((cell*spec[0], cell*spec[0]), Image.ANTIALIAS)
        box = (cell*coord[0], cell*coord[1], cell*(coord[0] + spec[0]), cell*(coord[1] + spec[0]))
        img.paste(src_img, box)
    return img

def gen_spec(xpx, ypx, n):
    """
        in: xpx, ypx, n
        out: xcells, ycells, cellsize

        Given a width <xpx> and height <ypx> in pixels, calculate the minimum number of squares
        it takes to fill that space. Given a minimum number of squares to place, return how
        many on each side are needed to accomodate the min, plus how may pixels/square.

        ex. 100, 100, 4 -> 2, 2, 50
            100, 150, 6 -> 2, 3, 50
            100, 150, 15 -> 4, 6, 25
    """ 
    best = 1
    for sq_size in xrange(2, max(xpx,ypx) + 1):
        if (xpx/sq_size) * (ypx/sq_size) < n:
            break
        if not xpx%sq_size and not ypx%sq_size:
            best = sq_size

    return xpx/best, ypx/best, best

def main(x,y,n, attr):
    xcell, ycell, cellsize = gen_spec(x, y, n)
    g = gen_grid(xcell, ycell, n)
    im = gen_image(g, attr=attr, cell=cellsize)
    im.save('bg_%s.png' % attr, format='PNG')
    im.show()

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
