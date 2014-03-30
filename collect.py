import os

def image_suffix(filename):
    for suffix in ['png']:
        if filename.endswith(suffix):
            return True
    return False

class ImageCollection(object):
    def __init__(self):
        self.images = set()

    def add_from_directory(self, image_dir):
        for filename in os.listdir(image_dir):
            if image_suffix(filename):
                self.images.add(os.path.join(image_dir, filename))
