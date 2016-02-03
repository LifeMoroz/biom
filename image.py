import os
from const import GABOR_RECOMMEND_HEIGHT_BLOCKS_COUNT
from crossing_number import calculate_minutiaes
from gabor import gabor
from thining import make_thin
import utils
from PIL import Image as PIL_Image


class Image(object):
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = PIL_Image.open(image_path)
        self._convert_color()
        self.block_size = None  # Gabor blocks

    def _convert_color(self):
        self.image = self.image.convert("L")

    def crop_image(self):
        w, h = self.image.size
        self.block_size = w // GABOR_RECOMMEND_HEIGHT_BLOCKS_COUNT
        rh = h % self.block_size
        rw = w % self.block_size
        self.image = self.image.crop((0, 0, w - rw, h - rh))

    def apply_gabor_filter(self):
        f = lambda x, y: 2 * x * y
        g = lambda x, y: x ** 2 - y ** 2

        angles = utils.calculate_angles(self.image, self.block_size, f, g)
        print("calculating orientation done")  # Todo: Doesnt work

        angles = utils.smooth_angles(angles)
        print("smoothing angles done")

        self.image = gabor(self.image, self.block_size, angles)

    def thin_lines(self):  # TODO: too slow
        make_thin(self.image)

    def calculate_minutiases(self):
        self.image = calculate_minutiaes(self.image)
        self.image.show()

    def save_to_disk(self):
        base_image_name = os.path.splitext(os.path.basename(self.image_path))[0]
        self.image.save(base_image_name + "_result.jpeg", "JPEG")

    def save_to_db(self):
        # TODO: db model
        pass
