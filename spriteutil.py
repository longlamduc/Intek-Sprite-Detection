#!/usr/bin/python3

from PIL import Image
import numpy as np
import random
import sys


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


class SpriteSheet():
    """Container of all Image Sprite Detection Method
    
    Raises:
        FileNotFoundError: When file path is not found
    """
    def __init__(self, fd, background_color=None):
        try:
            self.image = Image.open(fd)
        except FileNotFoundError:
            raise FileNotFoundError("No such file or directory")
        except Exception as e:
            if "Image" in str(e):
                self.image = fd
            else:
                raise Exception("This is not Image object or Image File Path")
        if not background_color and self.image.mode != 'RGBA':
            background_color = self.find_most_common_color(self.image)
        self.__background_color = background_color
    
    @property
    def background_color(self):
        return self.__background_color

    @staticmethod
    def find_most_common_color(img):
        """Find the most commonly used color in the image
        
        Arguments:
            img {Image} -- PIL Image object
        
        Returns:
            tuple or int -- The most commly used color of image, tuple or int based on type
        """
        colors = img.getcolors(maxcolors=img.width*img.height)
        return max(colors, key=lambda item: item[0])[1]

    def __is_background(self, point):
        """Check if an image pixel is background or not
        
        Arguments:
            point {tuple} -- Color of the pixel
            background_color {tuple} -- Color of the image backgrounf
        
        Returns:
            boolean -- Pixel is background or not
        """
        background = self.background_color
        mode = self.image.mode
        if not background and mode == 'RGBA':
            if point[3] == 0:
                return True
            else: 
                return False
        if mode not in ['RGB', 'RGBA'] and point == background:
            return True
        elif mode not in ['RGB', 'RGBA']: 
            return False
        if list(point) == list(background):
            return True
        else:
            return False
        


    def __create_sprite(self, label, label_map):
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


    def __find_whole_sprite(self, label_map, lst_pixel, checked, r_idx, c_idx, label):
        """Check out whole sprite from specified spite pixel
        
        Arguments:
            label_map {2d list} -- List corresponding to sprite label in image
            lst_pixel {2d list} -- List of all pixel in the image
            checked {2d list} -- List of checked on in the label_map
            r_idx {int} -- Row index of found pixel
            c_idx {int} -- Col index of found pixel
            label {int} -- Label of the new sprite
        """
        background_color = self.background_color
        way = [(r_idx, c_idx)]
        while len(way) > 0:
            row, col = way.pop(0)
            label_map[row][col] = label 
            for x, y in [(row - 1, col), (row + 1, col),
                        (row, col - 1), (row, col + 1)]:
                if 0 <= x <= len(lst_pixel) - 1 and \
                    0 <= y <= len(lst_pixel[0]) - 1 and \
                    not checked[x][y] and \
                    not self.__is_background(lst_pixel[row][col]):
                    checked[x][y] = True
                    way.append((x, y))


    def find_sprites(self):
        """Get an image as argument and then find all sprites in that image 
        by checking each pixel's color
        
        Arguments:
            image {Image} -- Image to find sprites
        
        Returns:
            tuple -- Dictionary of sprite information and label_map of 
                corresponding sprites found
        """
        image = self.image
        lst_pixel = np.asarray(image)
        checked = [[False for col in row] for row in lst_pixel]
        label = 0 
        sprites = {}
        label_map = [[0 for col in row] for row in lst_pixel]
        background_color = self.__background_color
        for row_idx, row in enumerate(lst_pixel):
            for col_idx, point in enumerate(row):   
                if not self.__is_background(point) and \
                    not checked[row_idx][col_idx]: 
                    label += 1
                    checked[row_idx][col_idx] = True
                    self.__find_whole_sprite(label_map, lst_pixel, checked, 
                                                row_idx, col_idx, label)
                    sprites[label] = self.__create_sprite(label, label_map)
        return (sprites, label_map)


    def create_sprite_labels_image(self):
        """Create an image containing mask for all sprite based on label_map
        
        Arguments:
            sprites {dictionary} -- Container of all Sprite object
            label_map {2d list} -- Label_map of image
        
        Keyword Arguments:
            background_color {tuple} -- Background color of new image (default: {None}) 
        
        Returns:
            Image -- Image of all sprite mask
        """
        background_color = self.background_color
        if not background_color and not isinstance(background_color, int):
            mode = 'RGBA'
        elif isinstance(background_color, tuple) and len(background_color) == 4:
            mode = 'RGBA'
        else: 
            mode = 'RGB'
        print(mode)
        sprites, label_map = self.find_sprites()
        image_size = (len(label_map[0]), len(label_map))
        mask = Image.new(mode, image_size, background_color)
        sprite_colors = {'0': background_color}
        for label in sprites.keys():
            while True:
                red = random.randint(0, 255)
                green = random.randint(0, 255)
                blue = random.randint(0, 255)
                if not (red, green, blue) in [sprite_colors[key] 
                        for key in sprite_colors.keys()]:
                    if mode == 'RGBA':
                        sprite_colors[label] = (red, green, blue, 255)
                    else:
                        sprite_colors[label] =  (red, green, blue)
                    break 
        width, height = mask.size
        for x in range(width):
            for y in range(height):
                if label_map[y][x] != 0:
                    mask.putpixel((x, y), sprite_colors[label_map[y][x]])
        for label in sprites.keys():
            sprite = sprites[label]
            for x in range(sprite.top_left[0], sprite.bottom_right[0] + 1):
                mask.putpixel((sprite.bottom_right[1], x), sprite_colors[label])
                mask.putpixel((sprite.top_left[1], x), sprite_colors[label])
            for x in range(sprite.top_left[1], sprite.bottom_right[1] + 1):
                mask.putpixel((x, sprite.top_left[0]), sprite_colors[label])
                mask.putpixel((x, sprite.bottom_right[0]), sprite_colors[label])
        return mask
