import unittest

from albumen.produce import squarepack

class TestSquarePack(unittest.TestCase):

    def test_gen_spec(self):
        schedule = [
            ((100, 100, 4), (2, 2, 50)),
            ((100, 100, 5), (4, 4, 25)),
            ((500, 400, 1), (5, 4, 100)),
            ((500, 400, 20), (5, 4, 100)),
            ((500, 400, 21), (10, 8, 50)),
            ((500, 400, 100), (20, 16, 25)),
            ((1440, 900, 39), (8, 5, 180)),
            ((1440, 900, 40), (8, 5, 180)),
            ((1440, 900, 41), (16, 10, 90)),
            ((1440, 900, 200), (24, 15, 60)),
            ((1920, 1080, 1), (16, 9, 120)),
            ((1920, 1080, 143), (16, 9, 120)), 
            ((1920, 1080, 144), (16, 9, 120)),
            ((1920, 1080, 145), (32, 18, 60))
        ]

        for test_in, expected in schedule:
            self.assertEqual(squarepack.gen_spec(*test_in), expected)

    def test_basic_grid(self):
        success_schedule = [
            ((2, 2, 3), 1),
            ((2, 2, 4), 4),
            ((2, 2, 5), 4),
            ((3, 3, 8), 6),
            ((3, 3, 9), 9),
            ((3, 3, 10), 9),
            #((8, 5, 16), 16),
            ((8, 5, 20), 19),
            ((8, 5, 35), 34),
            #((16, 9, 90), 90),
        ]

        for test_in, expected in success_schedule:
            g = squarepack.gen_grid(*test_in)
            self.assertEqual(g.size, expected, '%r: %d' % (test_in, expected))

        failures = [
            (3, 3, 5),
            (8, 5, 15),
        ]

        for test_in in failures:
            self.assertEqual(squarepack.gen_grid(*test_in), None)
