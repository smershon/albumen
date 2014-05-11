import os
import unittest

from albumen import util

class TestAlbumenUtil(unittest.TestCase):

    def test_unicode_scrub(self):
        a1 = u'Queensr\xffche'
        a2 = u'Mot\xf6rhead'
        a3 = u'Beyonc\xe9'

        r1 = util.scrub(a1)
        r2 = util.scrub(a2)
        r3 = util.scrub(a3)

        self.assertEqual(r1, 'queensr\xc3\xbfche')
        self.assertEqual(r2, 'mot\xc3\xb6rhead')
        self.assertEqual(r3, 'beyonc\xc3\xa9')

        self.assertEqual(os.system('touch %s' % r1), 0)
        self.assertEqual(os.system('touch %s' % r2), 0)
        self.assertEqual(os.system('touch %s' % r3), 0)

        for r in (r1, r2, r3):
            os.system('rm -f %s' % r)
