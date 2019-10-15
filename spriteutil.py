#!/usr/bin/python3

from PIL import Image


def find_most_common_color(img):
    """Find the most commonly used color in the image
    
    Arguments:
        img {Image} -- PIL Image object
    
    Returns:
        tuple or int -- The most commly used color of image, tuple or int based on type
    """
    colors = img.getcolors(maxcolors=1000000)
    return max(colors, key=lambda item: item[0])[1]


