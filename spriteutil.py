#!/usr/bin/python3

from PIL import Image


def find_most_common_color(img):
    colors = img.getcolors(maxcolors=1000000)
    return max(colors, key=lambda item: item[0])[1]


