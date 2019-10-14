#!/usr/bin/python3

from PIL import Image
import numpy as np
import sys
import pprint
import random

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


def is_background(point, background_color):
    if background_color is None:
        if point[3] == 0:
            return True
        else: 
            return False
    elif list(point) == list(background_color):
        return True
    else:
        return False
import pprint

def find_whole_sprite(label_map, lst_pixel, checked, r_idx, c_idx, label, background_color):
    way = [(r_idx, c_idx)]
    while len(way) > 0:
        row, col = way.pop(0)
        label_map[row][col] = label 
        for x, y in [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col - 1), (row, col + 1), (row + 1, col-1), (row + 1, col), (row + 1, col + 1)]:
            if 0 <= x <= len(lst_pixel) - 1 and 0 <= y <= len(lst_pixel[0]) - 1 and not checked[x][y] and not is_background(lst_pixel[row][col], background_color):
                checked[x][y] = True
                way.append((x, y))



def find_sprites(image, background_color=None):
    lst_pixel = np.asarray(image)
    checked = [[False for col in row] for row in lst_pixel]
    label = 0
    sprites = {}
    label_map = [[0 for col in row] for row in lst_pixel]
    if not background_color and image.mode != 'RGBA':
        background_color = find_most_common_color(image)
    print(background_color)
    for row_idx, row in enumerate(lst_pixel):
        for col_idx, point in enumerate(row):   
            if not is_background(point, background_color) and not checked[row_idx][col_idx]: 
                # print(row_idx, col_idx)
                label += 1
                checked[row_idx][col_idx] = True
                find_whole_sprite(label_map, lst_pixel, checked, row_idx, col_idx, label, background_color)
                sprite = {'label': label, 'x1': row_idx, 'y1': col_idx, 'x2': row_idx, 'y2': col_idx}
                pos = np.array(label_map, dtype=np.int64)
                pos = np.argwhere(pos==label)
                sprite['x1'] = min([x[0] for x in pos])
                sprite['x2'] = max([x[0] for x in pos])
                sprite['y1'] = min([x[1] for x in pos])
                sprite['y2'] = max([x[1] for x in pos])
                sprites[label] = Sprite(sprite['label'], sprite['x1'], sprite['y1'], sprite['x2'], sprite['y2'])
    # label_map1 = np.array(label_map, dtype=np.int64)
    # label_map1[label_map1>1] = 1
    # np.savetxt('test', label_map1 , delimiter = ' ', fmt="%d")
    # print(*label_map, sep='\n')
    return (sprites, label_map)


def create_sprite_labels_image(sprites, label_map, background_color=None):
    if not background_color:
        background_color = (255, 255, 255)
    if len(background_color) == 3:
        mode = 'RGB'
    else: 
        mode = 'RGBA'
    mask = Image.new(mode, (len(label_map[0]), len(label_map)), background_color)
    sprite_colors = {'0': background_color}
    for label in sprites.keys():
        while True:
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            if not (red, green, blue) in [sprite_colors[key] for key in sprite_colors.keys()]:
                sprite_colors[label] = (red, green, blue, 255) if mode == 'RGBA' else (red, green, blue)
                break 
    print(mask.size)
    print(len(label_map[0]), len(label_map))
    width, height = mask.size
    for x in range(width):
        for y in range(height):
            if label_map[y][x] != 0:
                mask.putpixel((x, y), sprite_colors[label_map[y][x]])
    for label in sprites.keys():
        sprite = sprites[label]
        for x in range(sprite.top_left[0], sprite.bottom_right[0] + 1):
            mask.putpixel((sprite.top_left[1], x), sprite_colors[sprite.label])
        for x in range(sprite.top_left[1], sprite.bottom_right[1] + 1):
            mask.putpixel((x, sprite.top_left[0]), sprite_colors[sprite.label])
        for x in range(sprite.top_left[1], sprite.bottom_right[1] + 1):
            mask.putpixel((x, sprite.bottom_right[0]), sprite_colors[sprite.label])
        for x in range(sprite.top_left[0], sprite.bottom_right[0] + 1):
            mask.putpixel((sprite.bottom_right[1], x), sprite_colors[sprite.label])
    return mask


# test
image = Image.open('metal_slug_sprite_sheet_large.png')
print(image.size)
# image = Image.open('islands.png')
print(find_most_common_color(image))
# sprites, label_map = find_sprites(image, background_color=(255, 255, 255))  # meta_slug
# sprites, label_map = find_sprites(image, background_color=(0, 221, 204, 255))  # islands

sprites, label_map = find_sprites(image)
# print(image.mode)
# for label, sprite in sprites.items():
#     print(f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")
#     cropped_example = image.crop((sprite.top_left[1], sprite.top_left[0], sprite.bottom_right[1], sprite.bottom_right[0]))
#     cropped_example.show()
# 

# pprint.pprint(label_map, width=120)

sprite_label_image = create_sprite_labels_image(sprites, label_map)
# sprite_label_image = create_sprite_labels_image({}, {})
sprite_label_image.save('test.png')