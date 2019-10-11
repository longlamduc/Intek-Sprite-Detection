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
        self.label = args[0]
        self.x1 = args[1]
        self.y1 = args[2]
        self.x2 = args[3]
        self.y2 = args[4]

    @property
    def label(self):
        return self.label 

    @property
    def top_left(self):
        return (self.x1, self.y1)

    @property
    def bottom_right(self):
        return (self.x2, self.y2)

    @property
    def width(self) :
        return self.x2 - self.x1 + 1

    @property
    def height(self):
        return self.y2 - self.y1 + 1