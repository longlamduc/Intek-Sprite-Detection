#!/usr/bin/python3

from PIL import Image
import numpy as np
import sys

def find_most_common_color(img):
    colors = img.getcolors(maxcolors=1000000)
    return max(colors, key=lambda item: item[0])[1]


class Sprite:
    def __init__(self, *args):
        if any(x < 0 for x in args):
            raise ValueError('Invalid coordinates')
        if args[1] > args[3] or args[2] > args[4]:
            raise ValueError('Invalid coordinates')
        self.__label = args[0]
        self.x1 = args[1]
        self.y1 = args[2]
        self.x2 = args[3]
        self.y2 = args[4]

    @property
    def label(self):
        return self.__label 

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
        return self.y2 -  self.y1 + 1


def is_background(point, background_color):
    if list(point) == list(background_color):
        return True
    elif len(point) == 4 and point[3] == 0:
        return True


def find_whole_sprite(label_map, lst_pixel, checked, r_idx, c_idx, label, background_color):
    pos = {'label': label, 'x1': r_idx, 'y1': c_idx, 'x2': r_idx, 'y2': c_idx}
    way = [(r_idx - 1, c_idx - 1), (r_idx - 1, c_idx), (r_idx - 1, c_idx + 1), (r_idx, c_idx - 1), (r_idx, c_idx + 1), (r_idx + 1, c_idx-1), (r_idx + 1, c_idx), (r_idx + 1, c_idx + 1)]
    while len(way) > 0:
        row, col = way.pop(0)
        if 0 <= row <= len(lst_pixel) - 1 and 0 <= col <= len(lst_pixel[0]) - 1:
            if not(checked[row][col] or is_background(lst_pixel[row][col], background_color)):
                checked[row][col] = True
                label_map[row][col] = label 
                for x, y in [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col - 1), (row, col + 1), (row + 1, col-1), (row + 1, col), (row + 1, col + 1)]:
                    way.append((x, y))
                if pos['x1'] > col:
                    pos['x1'] = col
                if pos['x2'] < col:
                    pos['x2'] = col 
                if pos['y1'] > row:
                    pos['y1'] = row 
                if pos['y2'] < row:
                    pos['y2'] = row
    return pos, label_map



def find_sprites(image, background_color=None):
    lst_pixel = np.asarray(image)
    checked = [[False for col in row] for row in lst_pixel]
    label = 0
    sprites = {}
    label_map = [[0 for col in row] for row in lst_pixel]
    if not background_color and image.mode != 'RGBA':
        background_color = find_most_common_color(image)
    for row_idx, row in enumerate(lst_pixel):
        for col_idx, point in enumerate(row):   
            if not is_background(point, background_color) and not checked[row_idx][col_idx]: 
                # print(row_idx, col_idx)
                label += 1
                checked[row_idx][col_idx] = True
                sprite, label_map = find_whole_sprite(label_map, lst_pixel, checked, row_idx, col_idx, label, background_color)
                # print(sprite)
                sprites[label] = Sprite(sprite['label'], sprite['x1'], sprite['y1'], sprite['x2'], sprite['y2'])
    return (sprites, label_map)

image = Image.open('islands.png')
print(find_most_common_color(image))
sprites, label_map = find_sprites(image, background_color=(0, 221, 204, 255))
print(image.mode)
for label, sprite in sprites.items():
    print(f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")
# import pprint
# pprint.pprint(label_map, width=120)


# img = Image.open('islands.png')
# img = img.convert('L')
# a = np.asarray(img)
# b = Image.fromarray(a)
# b.save('test.png')
# print(img.mode)
# print(a)
# print(tuple(a[800][700]))
# for x in a[800][700]:
#     print(x)