#!/usr/bin/env python3
# coding=utf-8
from thining import make_thin
from crossing_number import calculate_minutiaes
import argparse
from PIL import Image
import os
from gabor import gabor
import utils

GABOR_RECOMMEND_HEIGHT_BLOCKS_COUNT = 23

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Biometrics")
    parser.add_argument("image", nargs=1, help="Path to image")
    parser.add_argument("--save", action='store_true', help="Save result image as src_image_result.jpeg")
    args = parser.parse_args()
    ################ Opening ###################
    im = Image.open(args.image[0])
    im.show()
    im = im.convert("L")  # Приведение изображения к оттенкам серого
    ############# Cropping #####################
    w, h = im.size
    block_size = w // GABOR_RECOMMEND_HEIGHT_BLOCKS_COUNT
    rh = h % block_size
    rw = w % block_size
    im = im.crop((0, 0, w - rw, h - rh))
    ############### Gabor ######################

    f = lambda x, y: 2 * x * y
    g = lambda x, y: x ** 2 - y ** 2

    angles = utils.calculate_angles(im, block_size, f, g)
    print("calculating orientation done")

    angles = utils.smooth_angles(angles)
    print("smoothing angles done")

    im = gabor(im, block_size, angles)
    im.show()
    ################## Thining ####################
    make_thin(im)
    im = calculate_minutiaes(im)
    im.show()

    if args.save:
        base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
        im.save(base_image_name + "_result.jpeg", "JPEG")
