#!/usr/bin/python3

from PIL import Image
import numpy as np


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


def is_background(point, background_color):
    """Check if an image pixel is background or not
    
    Arguments:
        point {tuple} -- Color of the pixel
        background_color {tuple} -- Color of the image backgrounf
    
    Returns:
        boolean -- Pixel is background or not
    """
    if background_color is None:
        if point[3] == 0:
            return True
        else: 
            return False
    elif list(point) == list(background_color):
        return True
    else:
        return False


def create_sprite(label, label_map):
    """Create a Sprite object with specified label and label_map
    
    Arguments:
        label {int} -- Sprite label
        label_map {2d list} -- Label map contains sprite label
    
    Returns:
        Sprite -- Sprite object with label argument
    """
    sprite = {'label': label}
    pos = np.array(label_map, dtype=np.int64)
    pos = np.argwhere(pos==label)
    sprite['x1'] = int(min([x[0] for x in pos]))
    sprite['x2'] = int(max([x[0] for x in pos]))
    sprite['y1'] = int(min([x[1] for x in pos]))
    sprite['y2'] = int(max([x[1] for x in pos]))
    return Sprite(sprite['label'], sprite['x1'], sprite['y1'], 
                    sprite['x2'], sprite['y2'])


def find_whole_sprite(label_map, lst_pixel, checked, r_idx, c_idx, label, background_color):
    """Check out whole sprite from specified spite pixel
    
    Arguments:
        label_map {2d list} -- List corresponding to sprite label in image
        lst_pixel {2d list} -- List of all pixel in the image
        checked {2d list} -- List of checked on in the label_map
        r_idx {int} -- Row index of found pixel
        c_idx {int} -- Col index of found pixel
        label {int} -- Label of the new sprite
        background_color {tuple} -- Background color of image
    """
    way = [(r_idx, c_idx)]
    while len(way) > 0:
        row, col = way.pop(0)
        label_map[row][col] = label 
        for x, y in [(row - 1, col), (row + 1, col),
                        (row, col - 1), (row, col + 1)]:
            if 0 <= x <= len(lst_pixel) - 1 and \
                0 <= y <= len(lst_pixel[0]) - 1 and \
                not checked[x][y] and \
                not is_background(lst_pixel[row][col], background_color):
                checked[x][y] = True
                way.append((x, y))


def find_sprites(image, background_color=None):
    """Get an image as argument and then find all sprites in that image 
    by checking each pixel's color
    
    Arguments:
        image {Image} -- Image to find sprites
    
    Keyword Arguments:
        background_color {tuple} -- background color of image (default: {None})
    
    Returns:
        tuple -- Dictionary of sprite information and label_map of 
            corresponding sprites found
    """
    if image.mode not in ['RGB', 'RGBA']:
        image = image.convert('RGB')
    lst_pixel = np.asarray(image)
    checked = [[False for col in row] for row in lst_pixel]
    label = 0
    sprites = {}
    label_map = [[0 for col in row] for row in lst_pixel]
    if not background_color and image.mode != 'RGBA':
        background_color = find_most_common_color(image)
    for row_idx, row in enumerate(lst_pixel):
        for col_idx, point in enumerate(row):   
            if not is_background(point, background_color) and \
                not checked[row_idx][col_idx]: 
                label += 1
                checked[row_idx][col_idx] = True
                find_whole_sprite(label_map, lst_pixel, checked, row_idx, 
                                    col_idx, label, background_color)
                sprites[label] = create_sprite(label, label_map)
    return (sprites, label_map)
