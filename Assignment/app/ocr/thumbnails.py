#thumbnail
#from PIL import Image
from wand.image import Image

def thumbnails(path):
    name = path.split("/")[-1]
    thumbnails_path = path.replace(name, 'thumbnails_' + name)
    with Image(filename=path) as img:
        with img.clone() as thumb:
            size = thumb.width if thumb.width < thumb.height else thumb.height
            thumb.crop(width=size, height=size, gravity='center')
            thumb.resize(128, 128)
            thumb.save(filename=thumbnails_path)
    