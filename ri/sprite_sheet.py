# Copyright (C) 2019 Intek Institute.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Intek Institute or one of its subsidiaries.  You shall not disclose
# this confidential information and shall use it only in accordance
# with the terms of the license agreement or other applicable
# agreement you entered into with Intek Institute.
#
# INTEK INSTITUTE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  INTEK
# INSTITUTE SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY
# LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS
# SOFTWARE OR ITS DERIVATIVES.

import argparse
import collections
import datetime
import random
import sys

from PIL import Image
from PIL import ImageDraw
import numpy


NEIGHBOR_PIXEL_RELATIVE_COORDINATES = ((-1, -1), (0, -1), (1, -1), (-1, 0))


class Sprite:
    def __init__(self, x1, y1, x2, y2):
        """

        :param top_left: Coordinates of the top-left corner.

        :param bottom_right: Coordinates of the right-most corner.
        """
        if x1 > x2 or y1 > y2:
            raise ValueError('Invalid coordinates')

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    @property
    def bottom_right(self):
        return self.__x2, self.__y2

    @property
    def top_left(self):
        return self.__x1, self.__y1


class SpriteSheet:
    # +---+---+---+
    # | ? | ? | ? |
    # +---+---+---+
    # | ? | X |
    # +---+---+
    NEIGHBOR_PIXEL_RELATIVE_COORDINATES = ((-1, -1), (0, -1), (1, -1), (-1, 0))

    def __init__(self, image, transparent_color=None):
        self.__image = image
        self.__transparent_color = transparent_color

        self.__sprites = {}
        # Dictionary of sprites connected to each other.
        self.__sprites_links = {}

    def __link_sprites(self, id1, id2):
        """
        Link the two sprites, and all the other sprites connected to them.

        :param id1:

        :param id2:
        """
        sprite_indices = self.__sprites_links[id1] + self.__sprites_links[id2]
        for sprite_index in sprite_indices:
            self.__sprites_links[sprite_index] = sprite_indices

    def detect_sprites(self, transparent_color=None):
        # Determine the transparent color if not specified by the caller.
        if transparent_color is None:
            transparent_color = find_most_common_color(self.__image)

        print(transparent_color)

        # Convert the image into an array for faster access.
        image_pixels = numpy.asarray(self.__image)

        # Build the mask of the image used to store the sprite index for each
        # pixel of the given image.  The image mask is initially empty.
        image_width, image_height = self.__image.size
        image_mask = numpy.asarray([[0] * image_width] * image_height)

        # Start sprite index with `1`; the value `0` for the sprite index of a
        # pixel in the image mask means that this pixel doesn't belongs to any
        # sprite (e.g., this is a transparent pixel).
        sprite_index = 1

        for y in range(image_height):
            for x in range(image_width):
                if tuple(image_pixels[y][x]) != transparent_color:  # @todo: convert `transparent_color` to a numpy.ndarray

                    pixel_sprite_index = 0
                    for dx, dy in SpriteSheet.NEIGHBOR_PIXEL_RELATIVE_COORDINATES:
                        # Check whether a neighbor pixel belongs to a sprite.
                        if 0 <= x + dx < image_width and y + dy >= 0 and image_mask[y + dy][x + dx] > 0:
                            # If the current pixel has been already associated to a sprite, check
                            # whether the neighbor pixel belongs to this same sprite, and if not,
                            # merge those two sprites together.
                            if pixel_sprite_index and pixel_sprite_index != image_mask[y + dy][x + dx] \
                                    and image_mask[y + dy][x + dx] not in self.__sprites_links[pixel_sprite_index]:
                                self.__link_sprites(pixel_sprite_index, image_mask[y + dy][x + dx])

                            pixel_sprite_index = image_mask[y + dy][x + dx]

                    image_mask[y][x] = pixel_sprite_index

                    if pixel_sprite_index == 0:
                        image_mask[y][x] = sprite_index
                        self.__sprites_links[sprite_index] = [sprite_index]
                        sprite_index += 1

        return image_mask, self.__sprites_links



    def detect_most_common_color(self):
        """
        Return the color that is the most common in the given image.


        :param image: A `PIL.Image` object.


        :return: A tuple or an integer representing the color that is the most
            common in the given image.
        """
        pixels = numpy.asarray(self.__image)

        # Check whether the value of pixels is composed of multiple components
        # (e.g., RGB, RGBA, CMYK, YCbCr, etc.)
        is_multiple_components_color = len(pixels[0][0]) > 1

        # Count the number of times a pixel value is common in the given image.
        colors_count = {}
        for y in range(len(pixels)):
            for x in range(len(pixels[y])):
                # For image defined with multiple component color pixel, convert the
                # numpy data type (not hashable) representing the pixel value to its
                # tuple version (hashable).  This is a lot faster than converting the
                # pixel value to an integer with:
                #
                #     sum([c << i for i, c in enumerate(pixels[y][x])])
                color = tuple(pixels[y][x]) if is_multiple_components_color else pixels[y][x]
                colors_count[color] = colors_count.get(color, 0) + 1

        # Sort pixel value usages by decreasing order to retrieve the most common
        # pixel value.
        sorted_colors_count = sorted(colors_count.items(), key=lambda x: x[1], reverse=True)
        most_common_color, most_common_color_count = sorted_colors_count[0]

        return most_common_color





# def main():
#     arguments = parse_arguments()
#
#     image = Image.open(arguments.file_path_name)
#     detect_sprites(image)
#
#
# def parse_arguments():
#     """
#     Convert argument strings to objects and assign them as attributes of
#     the namespace.
#
#
#     @return: an instance ``argparse.Namespace`` corresponding to the
#         populated namespace.
#     """
#     parser = argparse.ArgumentParser(description='Sprite Detection')
#     parser.add_argument(
#         '-f', '--file',
#         dest='file_path_name',
#         metavar='FILE',
#         required=True,
#         help='specify the absolute name and path of the sprite sheet image file.')
#
#     return parser.parse_args()
#
#
# # if __name__ == '__main__':
# #     main()
#
#
# def build_sprites_mask_image(file_path_name, image_mask, sprites_links, unified=False, background_color=None):
#     if not background_color:
#         background_color = (255, 255, 255)
#
#     sprites_color = dict()
#
#     if unified:
#         for sprites_indices in sprites_links.values():
#             primary_sprite_index = sprites_indices[0]
#             if primary_sprite_index not in sprites_color:
#                 sprites_color[primary_sprite_index] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#
#         pixels = numpy.asarray(
#             [[sprites_color[sprites_links[c][0]] if c else (255, 255, 255) for c in row] for row in image_mask],
#             dtype=numpy.uint8)
#
#     else:
#         sprites_color[0] = (255, 255, 255)
#
#         for k in sprites_links.keys():
#             sprites_color[k] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#
#         pixels = numpy.asarray(
#             [[sprites_color[c] for c in row] for row in image_mask],
#             dtype=numpy.uint8)
#
#     Image.fromarray(pixels, 'RGB').save(file_path_name)
#
#
# #
# #
# # image = Image.open('/Users/dcaune/Devel/intek-mission-sprite_detection/metal_slug_sprite_sheet.png')
# # image_mask, sprites_links = SpriteSheet.detect_sprites(image)
# # build_sprites_mask_image('/Users/dcaune/Downloads/metal_slug_sprite_sheet_mask.png', image_mask, sprites_links)
# #
# #
# # sprite_sheet = SpriteSheet(image)
# # start_time = datetime.datetime.now()
# # image_mask, sprites_links = sprite_sheet.detect_sprites()
# # end_time = datetime.datetime.now()
# # execution_time = end_time - start_time
# #
# # execution_time
# # sprite_sheet.sprite_merging_time
# # execution_time - sprite_sheet.sprite_merging_time
# #
# # build_sprites_mask_image('/Users/dcaune/Devel/intek-mission-sprite_detection/islands_split_sprites_mask_.png', image_mask, sprites_links)
# # build_sprites_mask_image('/Users/dcaune/Devel/intek-mission-sprite_detection/islands_unified_sprites_mask_.png', image_mask, sprites_links, unified=True)
# #
# #
# # image = Image.open('/Users/dcaune/Devel/intek-mission-sprite_detection/qr_code.png')
# # image_mask, sprites_links = SpriteSheet.detect_sprites(image)
# #
# # build_sprites_mask_image('/Users/dcaune/Devel/intek-mission-sprite_detection/qr_code_decomposed_mask.png', image_mask, sprites_links)
# # build_sprites_mask_image('/Users/dcaune/Devel/intek-mission-sprite_detection/qr_code_unified_mask.png', image_mask, sprites_links, unified=True)


def find_most_common_color(image):
    """
    Return the color that is the most common in the given image.


    :param image: A `PIL.Image` object.


    :return: An integer or a tuple of integers (one for each band red, green,
        blue, and possibly alpha) representing the color that is the most
        common in the given image.
    """
    if image.mode not in ('L', 'RGB', 'RGBA'):
        raise ValueError(f"'The image mode '{image.mode}' is not supported")

    if image.mode == 'L':
        # Retrieve the list of colors used in this image.
        #
        # @note: Because this method is limited to a maximum number of colors
        #     (256), this method can only be used for non-RGB image (grayscale).
        colors_count = image.getcolors()

        # Sort pixel value usages by decreasing order to retrieve the most common
        # pixel value.
        sorted_colors_count = sorted(colors_count, key=lambda color_count: color_count[0], reverse=True)
        most_common_color_count, most_common_color = sorted_colors_count[0]

    else:
        # Count the number of times each unique pixel value is used in the
        # image.
        #
        # The numpy array of a PIL image, composed of multiple bands, is a 3D
        # array: an array of rows of this image, a sub-array of columns for this
        # row, and a sub-array of the band values of the pixel for this column
        # and this row.
        #
        # We need to flatten this array to a 2D array: an array of band values
        # of each pixel of this image.
        #
        # @note: We could have used the following similar code, but it's 30%
        #    slower (more likely the time to reshape the initial array).
        #
        #    ```python
        #    image_width, image_height = image.size
        #    flatten_colors = numpy.asarray(image) \
        #        .flatten() \
        #        .reshape((image_width * image_height, len(image.getbands())))
        #    pixel_counter = collections.Counter(zip(*flatten_colors))
        #    ```

        # Split this image into individual bands; for example, splitting an "RGB"
        # image creates three new images each containing a copy of one of the
        # original bands (red, green, blue). Then build a list of numpy arrays of
        # these image bands with flatten values.
        color_channels = [
            numpy.asarray(image_band).flatten()
            for image_band in image.split()]

        # Recompose pixel colors with its respective components taken from each
        # image band.
        flatten_colors = zip(*color_channels)

        # Count the number of times each unique color is used in the image and
        # retrieve the most common color.
        pixel_counter = collections.Counter(flatten_colors)

        most_common_color_counts = pixel_counter.most_common(1)
        most_common_color, most_common_color_count = most_common_color_counts[0]

    return most_common_color



def detect_sprites(image, transparent_color=None):
    def __link_sprites(id1, id2):
        """
        Link the two sprites, and all the other sprites connected to them.

        :param id1:

        :param id2:
        """
        sprite_indices = sprites_links[id1] + sprites_links[id2]
        for sprite_index in sprite_indices:
            sprites_links[sprite_index] = sprite_indices

    def __merge_sprite_links():
        sprites_primary_index = {}
        for sprite_index, linked_sprites_indices in sprites_links.items():
            sprites_primary_index[sprite_index] = linked_sprites_indices[0]

        unified_image_mask = [
            [color and sprites_primary_index[color] for color in row]
            for row in image_mask]

        foo = collections.defaultdict(list)
        for y, row in enumerate(unified_image_mask):
            for x, sprite_index in enumerate(row):
                foo[sprite_index].append((x, y))

        sprites = {}

        for sprite_index in foo:
            if sprite_index:
                x1 = y1 = sys.maxsize
                x2 = y2 = 0
                for x, y in foo[sprite_index]:
                    if x < x1: x1 = x
                    if x > x2: x2 = x
                    if y < y1: y1 = y
                    if y > y2: y2 = y
                sprites[sprite_index] = Sprite(x1, y1, x2, y2)

        return unified_image_mask, sprites


    # Determine the transparent color if not specified by the caller.
    if transparent_color is None:
        transparent_color = find_most_common_color(image)

    # Convert the image into an array for faster access.
    image_pixels = numpy.asarray(image)

    # Build the mask of the image used to store the sprite index for each
    # pixel of the given image.  The image mask is initially empty.
    image_width, image_height = image.size
    image_mask = numpy.asarray([[0] * image_width] * image_height)

    # Start sprite index with `1`; the value `0` for the sprite index of a
    # pixel in the image mask means that this pixel doesn't belongs to any
    # sprite (e.g., this is a transparent pixel).
    sprite_index = 1

    sprites_links = {}

    for y in range(image_height):
        for x in range(image_width):
            if tuple(image_pixels[y][x]) != transparent_color:  # @todo: convert `transparent_color` to a numpy.ndarray

                pixel_sprite_index = 0
                for dx, dy in NEIGHBOR_PIXEL_RELATIVE_COORDINATES:
                    # Check whether a neighbor pixel belongs to a sprite.
                    if 0 <= x + dx < image_width and y + dy >= 0 and image_mask[y + dy][x + dx] > 0:
                        # If the current pixel has been already associated to a sprite, check
                        # whether the neighbor pixel belongs to this same sprite, and if not,
                        # merge those two sprites together.
                        if pixel_sprite_index and pixel_sprite_index != image_mask[y + dy][x + dx] \
                                and image_mask[y + dy][x + dx] not in sprites_links[pixel_sprite_index]:
                            __link_sprites(pixel_sprite_index, image_mask[y + dy][x + dx])

                        pixel_sprite_index = image_mask[y + dy][x + dx]

                image_mask[y][x] = pixel_sprite_index

                if pixel_sprite_index == 0:
                    image_mask[y][x] = sprite_index
                    sprites_links[sprite_index] = [sprite_index]
                    sprite_index += 1

    return __merge_sprite_links()





def save_mask_image(file_path_name, image_mask, background_color=None, display_bounding_box=False, sprites=None):
    sprite_indices = set([
        color
        for row in image_mask
        for color in row])

    sprites_color = {
        0: background_color and (255, 255, 255)
    }

    for sprite_index in sprite_indices:
        sprites_color[sprite_index] = (random.randint(64, 200), random.randint(64, 200), random.randint(64, 200))

    pixels = numpy.asarray([
        [sprites_color[c] if c else (255, 255, 255) for c in row]
        for row in image_mask],
        dtype=numpy.uint8)

    image = Image.fromarray(pixels, 'RGB')

    if display_bounding_box:
        draw = ImageDraw.Draw(image)

        for sprite_index in sprites:
            sprite = sprites[sprite_index]
            color = sprites_color[sprite_index]
            color += (128,)
            draw.rectangle((sprite.top_left, sprite.bottom_right), outline=color, width=1)

    image.save(file_path_name)


image = Image.open('/Users/dcaune/Devel/intek-mission-sprite_detection/optimized_sprite_sheet.png')
image_mask, sprites = detect_sprites(image)
save_mask_image('/Users/dcaune/foo.png', image_mask, display_bounding_box=True, sprites=sprites)
