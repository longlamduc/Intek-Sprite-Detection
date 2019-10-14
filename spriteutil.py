#!/usr/bin/python3

from PIL import Image


def find_most_common_color(img):
    colors = img.getcolors(maxcolors=1000000)
    return max(colors, key=lambda item: item[0])[1]


class Sprite():
    def __init__(self, *args):
        if any(x < 0 for x in args):
            raise ValueError('Invalid coordinates')
        if args[1] > args[3] or args[2] > args[4]:
            raise ValueError('Invalid coordinates')
        self.__label = args[0]
        self.__x1 = args[1]
        self.__y1 = args[2]
        self.__x2 = args[3]
        self.__y2 = args[4]

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
        return self.__x2 - self.__x1 + 1

    @property
    def height(self):
        return self.__y2 -  self.__y1 + 1