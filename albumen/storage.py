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
                    title       TEXT, 
                    artist      TEXT,
                    has_image   INTEGER )
                """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    md5         TEXT PRIMARY KEY,
                    path        TEXT,
                    album_fk    INTEGER,
                    width       INTEGER,
                    height      INTEGER,
                    red         FLOAT, 
                    green       FLOAT, 
                    blue        FLOAT, 
                    lightness   FLOAT, 
                    saturation  FLOAT, 
                    complexity  FLOAT,
                    FOREIGN KEY(album_fk) REFERENCES albums(pk) )
                """)

    def db_conn(self):
        return sqlite3.connect('%s/albumen.db' % self.folder)

    def album_pk(self, artist, title):
        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT pk FROM albums
                WHERE artist = ? AND title = ?""",
                (artist, title))
            row = c.fetchone()
        if row:
            return row[0]
        return None

    def get_album(self, artist, title):
        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT artist, title, has_mbid FROM albums
                WHERE artist = ? AND title = ?""",
                (artist, title))
            row = c.fetchone()
        if row:
            return {
                'artist': row[0],
                'album': row[1],
                'has_mbid': row[2]
            }
        return None

    def update_album(self, artist, title, has_image=True):
        pk = self.album_pk(artist, title)
        if pk:
            with self.db_conn() as conn:
                c = conn.cursor()
                c.execute("""
                    UPDATE albums SET
                        title=?, artist=?, has_image=?
                    WHERE pk = ?""",
                    (title, artist, int(has_image), pk))
        else:
            with self.db_conn() as conn:
                c = conn.cursor()
                c.execute("""
                    INSERT INTO albums
                        (title, artist, has_image)
                    VALUES (?, ?, ?)""",
                    (title, artist, int(has_image)))

    def get_images_for_album(self, artist, title):
        pk = self.album_pk(artist, title)
        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT path, width, height FROM images
                WHERE album_fk = ?""",
                (pk,))
            rows = c.fetchall()
        return [{'path': r[0], 'width': r[1], 'height': r[2]} for r in rows]

    def get_image_by_path(self, path):
        with open(path, 'rb') as f:
            file_md5 = md5.new(f.read()).hexdigest()

        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT path, width, height FROM images
                WHERE md5 = ?""", (file_md5,))
            row = c.fetchone()
        if row:
            return {'path': row[0], 'width': row[1], 'height': row[2]}
        return None

    def update_image(self, artist, title, img, analysis=None):
        with open(img.filename, 'rb') as f:
            file_md5 = md5.new(f.read()).hexdigest() 

        pk = self.album_pk(artist, title)

        if not pk:
            self.update_album(artist, title)
            pk = self.album_pk(artist, title)

        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE into images
                    (md5, path, album_fk, width, height)
                VALUES (?, ?, ?, ?, ?)""",
                (file_md5, img.filename, pk, img.size[0], img.size[1]))

    def all_albums(self):
        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT artist, title, has_image FROM albums""")
            rows = c.fetchall()
        return rows

    def all_images(self):
        with self.db_conn() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT md5, path, album_fk, width, height FROM images""")
            rows = c.fetchall()
        return rows
