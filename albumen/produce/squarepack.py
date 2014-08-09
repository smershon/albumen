from optparse import OptionParser
import random

import Image

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
                for jp in range(4):
                    if self.get_block(i+3, j + jp)[0] == -1:
                        self.one.add((i+3, j + jp))
                for ip in range(4):
                    if self.get_block(i + ip, j+3)[0] == -1:
                        self.one.add((i + ip, j+3))
                self.three.add((i,j))
                return True
        return False

def build_image(xpx, ypx, n, attr, test=False):
    x, y, sqsize = gen_spec(xpx, ypx, n)
    print x, y, sqsize
    grid = ImGrid(x, y)
    print grid.size()
    while grid.size() > n:
        print grid.size()
        if not grid.newtwo():
            if not grid.newthree():
                print 'bailing out'
                break
    print '--%d' % grid.size()
    if test:
        img_src = test_img_src()
    else:
        img_src = db_img_src(attr)
    ret_img = Image.new('RGB', (xpx, ypx))
    for c, size in grid.cells_by_size():
        new_img = img_src.next().resize((size*sqsize, size*sqsize), Image.ANTIALIAS)
        box = ( sqsize*c[0],
                sqsize*c[1] )
        ret_img.paste(new_img, box)
    return ret_img
        
def db_img_src(attr):
    for img in analysis_cache.get_images(sort_field=attr):
        yield Image.open('samples/%s' % img.meta['filename']).resize(
        (cell*spec[0], cell*spec[0]), Image.ANTIALIAS)
        
def test_img_src():
    def random_color():
        return (random.randint(0, 255), 
                random.randint(0, 255), 
                random.randint(0, 255) )
    
    while True:
        yield Image.new('RGB', (100, 100), random_color())

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
    img = build_image(x, y, options.num, options.attr, options.test)
    img.show()


if __name__ == '__main__':
    main()
