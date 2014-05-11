import os
import unittest

from albumen import storage

TD = 'albumen_test'

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        # Create directory for testing
        os.system('mkdir -p %s' % TD)

    def tearDown(self):
        # Delete directory
        os.system('rm -rf %s' % TD)

    def test_create_db(self):
        s = storage.Storage(TD)
        s.create_db()

        with s.db_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = sorted([x[0] for x in c.fetchall()])

        self.assertEqual(tables, ['albums', 'images'])
