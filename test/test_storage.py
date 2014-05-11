import os
import unittest

from albumen import image_analysis
from albumen import storage

TD = 'albumen_test'

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        # Create directory for testing
        os.system('mkdir -p %s' % TD)

    def tearDown(self):
        # Delete directory
        os.system('rm -rf %s' % TD)

    def _fake_analysis(self):
        os.system('echo "fake" > %s/fake.txt' % TD)
        img = image_analysis.ImageAnalysis({
            'filepath': '%s/fake.txt' % TD,
            'height': 100,
            'width': 100
        })
        img.pixels = 10000
        img.total_red = 1000.0
        img.total_green = -5000.0
        img.total_blue = 4000.0
        img.total_lightness = 4000.0
        img.total_saturation = 5000.0
        img.total_complexity = 6000.0
        return img

    def test_create_db(self):
        s = storage.Storage(TD)
        s.create_db()

        with s.db_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = sorted([x[0] for x in c.fetchall()])

        self.assertEqual(tables, ['albums', 'images'])

    def test_album_pk(self):
        s = storage.Storage(TD)
        s.create_db()

        s.update_album('Hawk Master', 'Flyte of the Khondor')
        self.assertEqual(s.album_pk('Hawk Master', 'Flyte of the Khondor'), 1)
        self.assertEqual(s.album_pk('DJ Poser', 'Fake Beats'), None)

    def test_get_album(self):
        s = storage.Storage(TD)
        s.create_db()

        s.update_album('Hawk Master', 'Flyte of the Khondor')
        s.update_album('Hawk Master', 'Falcon Star', has_image=True)

        expected = {
            'artist': 'Hawk Master',
            'album': 'Flyte of the Khondor',
            'has_image': False
        }

        self.assertEqual(s.get_album('Hawk Master', 'Flyte of the Khondor'), expected)

        expected = {
            'artist': 'Hawk Master',
            'album': 'Falcon Star',
            'has_image': True
        }
        
        self.assertEqual(s.get_album('Hawk Master', 'Falcon Star'), expected)
        self.assertEqual(s.get_album('DJ Poser', 'Fake Beats'), None)

    def test_update_album(self):
        s = storage.Storage(TD)
        s.create_db()

        s.update_album('Hawk Master', 'Flyte of the Khondor')
        s.update_album('Hawk Master', 'Falcon Star')
        s.update_album('Hawk Master', 'Flyte of the Khondor', has_image=True)

        expected = {
            'artist': 'Hawk Master',
            'album': 'Flyte of the Khondor',
            'has_image': True
        }

        self.assertEqual(s.get_album('Hawk Master', 'Flyte of the Khondor'), expected)

        expected = {
            'artist': 'Hawk Master',
            'album': 'Falcon Star',
            'has_image': False
        }

        self.assertEqual(s.get_album('Hawk Master', 'Falcon Star'), expected)

    def test_all_albums(self):
        s = storage.Storage(TD)
        s.create_db()

        s.update_album('Hawk Master', 'Flyte of the Khondor')
        s.update_album('Hawk Master', 'Falcon Star', has_image=True)

        expected = [
            ('Hawk Master', 'Flyte of the Khondor', 0),
            ('Hawk Master', 'Falcon Star', 1)
        ]

        self.assertEqual(s.all_albums(), expected)

    def test_update_image(self):
        s = storage.Storage(TD)
        s.create_db()

        s.update_album('Hawk Master', 'Falcon Star', has_image=True)

        img = self._fake_analysis()
        s.update_image('Hawk Master', 'Falcon Star', img) 
        
        expected = [{
            'blue': 0.4, 'width': 100, 'saturation': 0.5, 'green': -0.5, 
            'path': u'albumen_test/fake.txt', 'lightness': 0.4, 
            'complexity': 0.6, 'red': 0.1, 'height': 100
        }]

        self.assertEqual(s.get_images_for_album('Hawk Master', 'Falcon Star'), expected)




