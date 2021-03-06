from optparse import OptionParser
import random

import Image

from albumen import analysis_cache

class ImGrid(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.one = set()
        self.two = set()
        self.three = set()
        for xcoord in xrange(x):
            for ycoord in xrange(y):
                self.one.add((xcoord, ycoord))
    
    def size(self):
        return len(self.one) + len(self.two) + len(self.three) 
    
    def cells_by_size(self):
        for c in random.sample(self.three, len(self.three)):
            yield (c, 3)
        for c in random.sample(self.two, len(self.two)):
            yield (c, 2)
        for c in random.sample(self.one, len(self.one)):
            yield (c, 1)
   
    def edge_cells(self, inner=False):
        blocks = set()
        for i in range(self.x):
            blocks.add(self.get_block(i, 0))
            blocks.add(self.get_block(i, self.y-1))
        for j in range(self.y):
            blocks.add(self.get_block(0, j))
            blocks.add(self.get_block(self.x-1, j))
        if not inner:
            for b in sorted(list(blocks), key=lambda x: x[1], reverse=True):
                yield (b[1], b[0])
        else:
            coords = set([b[1] for b in blocks])
            for c in self.three - coords:
                yield (c, 3)
            for c in self.two - coords:
                yield (c, 2)
            for c in self.one - coords:
                yield (c, 1)

    def get_block(self, i, j):
        """
            Return (size, (x, y)),
            where size is the size of the block coord(i, j) is in,
            and (x, y) is the upper left coord of that block.
            
            If (i, j) is outside the grid, return (0, (None, None)).
        """
        if any([i < 0, i >= self.x, j < 0, j >= self.y]):
            return (0, (None, None))
        elif (i, j) in self.one:
            return (1, (i, j))
        elif (i, j) in self.two:
            return (2, (i, j))
        elif (i, j) in self.three:
            return (3, (i, j))
        
        for c in [(i-1, j), (i, j-1), (i-1, j-1)]:
            if c in self.two:
                return (2, c)
                
        for c in [(i, j-1), (i, j-2), (i-1, j), (i-1, j-1),
            (i-1, j-2), (i-2, j), (i-2, j-1), (i-2, j-2)]:
            if c in self.three:
                return (3, c)
                
        return (-1, (i, j))

    def _missing_blocks(self):
        missing = []
        for i in xrange(self.x):
            for j in xrange(self.y):
                block = self.get_block(i, j)
                if block[0] <= 0:
                    missing.append(block)
        return missing

    def _get_n_blocks(self, i, j, n):
        blocks = []
        for ip in range(n):
            for jp in range(n):
                blocks.append(self.get_block(i+ip, j+jp))
        return blocks

    def _del_block(self, c, field):
        if c in field:
            field.remove(c)

    def newtwo(self):
        for i,j in random.sample(self.one, len(self.one)):
            blocks = self._get_n_blocks(i, j, 2)
            if all([b[0] == 1 for b in blocks]):
                for b in blocks:
                    self._del_block(b[1], self.one)
                self.two.add((i,j))
                return True
        return False

    def newthree(self):
        choices = self.one | self.two
        for i,j, in random.sample(choices, len(choices)):
            blocks = self._get_n_blocks(i, j, 3)
            if all([b[0] in [1,2] for b in blocks]):
                for b in blocks:
                    self._del_block(b[1], self.one)
                    self._del_block(b[1], self.two)
                self.three.add((i,j))
                for block in self._missing_blocks():
                    self.one.add(block[1])
                return True
        return False

def build_image(xpx, ypx, n, img_src):
    x, y, sqsize = gen_spec(xpx, ypx, n)
    grid = ImGrid(x, y)
    
    while grid.size() > n:
        if not grid.newtwo():
            if not grid.newthree():
                print 'bailing out'
                break
                
    ret_img = Image.new('RGB', (xpx, ypx))
    
    for c, size in grid.cells_by_size():
        new_img = img_src.next().resize((size*sqsize, size*sqsize), Image.ANTIALIAS)
        box = ( sqsize*c[0],
                sqsize*c[1] )
        ret_img.paste(new_img, box)
        
    return ret_img
        
def db_img_src(attr):
    for img in analysis_cache.get_images(sort_field=attr):
        yield Image.open('samples/%s' % img.meta['filename'])
        
def test_img_src():
    def random_color():
        return (random.randint(200, 255), 
                random.randint(200, 255), 
                random.randint(200, 255) )
    
    while True:
        yield Image.new('RGB', (100, 100), random_color())

def gen_spec(xpx, ypx, n):
    """
        in: xpx, ypx, n
        out: xcells, ycells, cellsize

        Given a width <xpx> and height <ypx> in pixels, calculate the minimum number of squares
        it takes to fill that space. Given a minimum number of squares to place, return how
        many on each side are needed to accomodate the min, plus how may pixels/square.

        ex.10q, 100, 4 -> 2, 2, 50
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

def main():
    parser = OptionParser()
    parser.add_option('--size', dest='size')
    parser.add_option('-n', '--num', dest='num', type='int')
    parser.add_option('-a', '--attr', dest='attr')
    parser.add_option('--test', dest='test', action='store_true', default=False)

    options, _ = parser.parse_args()
    if not all([options.size, options.num, options.attr]):
        print 'wrong'
        exit()

    try:
        strx, stry = options.size.split('x')
        x, y = int(strx), int(stry)
    except:
        print 'also wrong'
        exit()

    print options

    if options.test:
        img_src = test_img_src()
    else:
        img_src = db_img_src(options.attr)

    img = build_image(x, y, options.num, img_src)
    img.show()


if __name__ == '__main__':
    main()
