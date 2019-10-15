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


class Sprite():
    """
        Create a sprite object wihth label and position
    """
    def __init__(self, label, x1, y1, x2, y2):
        """
        Arguments:
            label {int} -- Sprite label
            x1 {int} -- left position of sprite
            y1 {int } -- top position of sprite
            x2 {int} -- right position of sprite
            y2 {int} -- bottom position of sprite
        
        Raises:
            ValueError: Arguments is not type int
            ValueError: Arguments contains negative number
            ValueError: x1 < x2 or y1 < y2
        """
        if not all(isinstance(x, int) for x in [label, x1, y1, x2, y2]):
            raise ValueError('Invalid coordinates')
        if any(x < 0 for x in [label, x1, y1, x2, y2]):
            raise ValueError('Invalid coordinates')
        if x1 > x2 or y1 > y2:
            raise ValueError('Invalid coordinates')
        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__width = self.__x2 - self.__x1 + 1
        self.__height = self.__y2 -  self.__y1 + 1

    @property
    def label(self):
        return self.__label 

    @property
    def top_left(self):
        return (self.__x1, self.__y1)

    @property
    def bottom_right(self):
        return (self.__x2, self.__y2)

    @property
    def width(self) :
        return self.__width

    @property
    def height(self):
        return self.__height


