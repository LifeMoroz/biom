#!/usr/bin/env python3
# coding=utf-8
import argparse

from image import Image


def main(image_path):
    di = Image(image_path)
    di.crop_image()
    di.apply_gabor_filter()
    di.thin_lines()
    di.calculate_minutiases()

    if args.save:
        di.save_to_disk()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Biometrics")
    parser.add_argument("image", nargs=1, help="Path to image")
    parser.add_argument("--save", action='store_true', help="Save result image as src_image_result.jpeg")
    args = parser.parse_args()

    main(args.image[0])
