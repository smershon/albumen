import md5
import sqlite3

class Storage(object):
    def __init__(self, folder):
        self.folder = folder

    def create_db(self):
        with sqlite3.connect('%s/albumen.db' % self.folder) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS albums (
                    pk          INTEGER PRIMARY KEY,
                    md5         TEXT,
                    mbid        TEXT, 
                    title       TEXT, 
                    artist_name TEXT,
                    path        TEXT )
                """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    md5         TEXT PRIMARY KEY,
                    red         FLOAT, 
                    green       FLOAT, 
                    blue        FLOAT, 
                    lightness   FLOAT, 
                    saturation  FLOAT, 
                    complexity  FLOAT )
                """)

    def db_conn(self):
        return sqlite3.connect('%s/albumen.db' % self.folder)

    def insert_album(self, artist, title, path=None, mbid=None):
        if path is None:
            file_md5 = None
        else:
            with open(path, 'rb') as f:
                file_md5 = md5.new(f.read()).hexdigest()

        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO albums
                    (md5, mbid, title, artist_name, path)
                VALUES (?, ?, ?, ?, ?)""",
                (file_md5, mbid, title, artist, path))

