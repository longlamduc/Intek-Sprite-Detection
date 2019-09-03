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
    """
    Represent the identification and the position of a sprite packed in a
    picture with other sprites.

    A sprite is identified with a unique label (a strictly positive
    integer).

    The location of a sprite is defined with a bounding box (top-left and
    bottom-right) of the contour of the sprite.
    """
    def __init__(self, label, x1, y1, x2, y2):
        """
        Build a new `Sprite` object.

        The coordinates of the top-left and bottom-right corners of the sprite
        are related to the top-left corner of the picture this sprite is
        packed in.


        :param label: Label of this sprite. This label MUST be unique among
            all the sprites packed in a picture.

        :param x1: Abscissa of the top-left corner.

        :param y1: Ordinate of the top-left corner of the bounding box of this
            sprite.

        :param x2: Abscissa of the bottom-right corner of the bounding box of
            this sprite.

        :param y2: Ordinate of the bottom-left corner of the bounding box of
            this sprite.


        :raise ValueError: If the specified coordinates of the sprite's
            bounding box are invalid.  These coordinates MUST all be positive
            integer values; the coordinates of the top-left corner MUST be on
            the top or the left of the coordinates of the bottom-right corner.
        """
        if not isinstance(label, int) or label < 0:
            raise ValueError('Invalid coordinates')

        if not isinstance(x1, int) or not isinstance(y1, int) or \
           not isinstance(x2, int) or not isinstance(y2, int) or \
           x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x1 > x2 or y1 > y2:
            raise ValueError('Invalid coordinates')

        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    @property
    def bottom_right(self):
        return self.__x2, self.__y2

    @property
    def height(self):
        return self.__y2 - self.__y1 + 1

    @property
    def label(self):
        return self.__label

    @property
    def width(self):
        return self.__x2 - self.__x1 + 1

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

        # Convert the image into an array for faster access.
        image_pixels = numpy.asarray(self.__image)

        # Build the mask of the image used to store the sprite label for each
        # pixel of the given image.  The image mask is initially empty.
        image_width, image_height = self.__image.size
        image_mask = numpy.asarray([[0] * image_width] * image_height)

        # Start sprite label with `1`; the value `0` for the sprite label of a
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


def find_sprites(image, transparent_color=None):
    def __link_labels(label1, label2):
        """
        Link the two specified labels that identify connected parts of a same
        sprite.

        :param label1: A first label.

        :param label2: An second label equivalent to the first label passed to
            this function.
        """
        sprite_indices = linked_labels[label1] + linked_labels[label2]
        for sprite_index in sprite_indices:
            linked_labels[sprite_index] = sprite_indices

    def __merge_linked_labels():
        """
        Merge the equivalence labels together and unify all the connected
        fragments of a sprite to one sprite.


        :return: A tuple `(sprites, labels)` where:

            * `sprites`: A collection of key-value pairs (a dictionary) where each
              key-value pair maps the key (the label of a sprite) to its associated
              value (a `Sprite` object).  Each connected fragment of a sprite has
              been unified to one sprite.

            * `labels`: A 2D array of integers of equal dimension (width and height)
              as the original image where the sprites are packed in. This array
              maps each pixel of the original image to the label of the sprite this
              pixel corresponds to, or `0` if this pixel doesn't belong to a sprite
              (e.g., transparent color).
        """
        # Reduce each group of equivalence labels (each referencing connected
        # parts of a sprite) to one label only, the first in the list.
        primary_labels = {}
        for label, equivalence_labels in linked_labels.items():
            primary_labels[label] = equivalence_labels[0]

        # Create a new a 2D array of integers that maps each pixel of the to
        # the unified label of the sprite this pixel corresponds to, or `0` if
        # this pixel doesn't belong to a sprite (e.g., transparent color).
        unified_labels = [
            [label and primary_labels[label] for label in row]
            for row in pixel_labels]

        # Determine the list of pixels mapped to each unique label.
        label_pixels_coordinates = collections.defaultdict(list)
        for y, row in enumerate(unified_labels):
            for x, label in enumerate(row):
                label_pixels_coordinates[label].append((x, y))

        # Build the list of sprites (which connected parts have been reunified)
        # and calculate their respective bounding box.
        sprites = {}

        for label in label_pixels_coordinates:
            x1 = y1 = sys.maxsize
            x2 = y2 = 0

            for x, y in label_pixels_coordinates[label]:
                if x < x1: x1 = x
                if x > x2: x2 = x
                if y < y1: y1 = y
                if y > y2: y2 = y

            sprites[label] = Sprite(label, x1, y1, x2, y2)

        return sprites, unified_labels

    # Determine the transparent color if not specified by the caller.
    if transparent_color is None:
        transparent_color = find_most_common_color(image)

    # Convert the image into an array for faster access.
    pixels = numpy.asarray(image)

    # Create a 2D array of integers of equal dimension (width and height) as
    # the image passed to the function. This array maps each pixel of the to
    # the label of the sprite this pixel corresponds to, or `0` if this
    # pixel doesn't belong to a sprite (e.g., transparent color).
    image_width, image_height = image.size
    pixel_labels = numpy.asarray([[0] * image_width] * image_height)

    # Generator of label identifiers to map with pixels that are part of a
    # sprite (e.g., pixel that are not considered as transparent, that do
    # not belong to the background color).
    current_label = 0

    # Table of label equivalence (a dictionary) to keep note of which labels
    # refer to the same sprite when two parts of a sprite eventually connect.
    # If a pixel has multiple neighbors with different labels, the algorithm
    # assigns for that pixel the first label found and indicate that all
    # the other ones are equivalent. The filled table contains every label
    # (the key) in the image and the labels (the associated value) from
    # their surrounding neighbors too.
    linked_labels = {}

    for y in range(image_height):
        for x in range(image_width):
            if tuple(pixels[y][x]) != transparent_color:  # @todo: convert `transparent_color` to a numpy.ndarray
                # Label associated to this pixel. Initially no label.
                pixel_label = 0

                for dx, dy in NEIGHBOR_PIXEL_RELATIVE_COORDINATES:
                    # Check whether a neighbor pixel belongs to a sprite.
                    if 0 <= x + dx < image_width and y + dy >= 0 and pixel_labels[y + dy][x + dx] > 0:
                        # If the current pixel has been already associated to a label, check
                        # whether the neighbor pixel has the same label, and if not, link these
                        # labels and their equivalent labels all together.
                        if pixel_label and pixel_label != pixel_labels[y + dy][x + dx] and \
                           pixel_labels[y + dy][x + dx] not in linked_labels[pixel_label]:
                            __link_labels(pixel_label, pixel_labels[y + dy][x + dx])

                        pixel_label = pixel_labels[y + dy][x + dx]

                # If the pixel is not connected to a neighbor pixel, generate a new
                # label. Map the pixel to the associated label.
                if pixel_label == 0:
                    current_label += 1
                    pixel_labels[y][x] = current_label
                    linked_labels[current_label] = [current_label]

                pixel_labels[y][x] = pixel_label

    return __merge_linked_labels()


def create_sprite_labels_image(sprites, label_matrix, background_color=None):
    """
    Create a new image, drawing the masks of the sprites at the exact same
    position that the sprites were in the original image.

    The function draws each sprite mask with a random uniform color (one
    color per sprite mask). The function also draws a rectangle (bounding
    box) around each sprite mask, of the same color used for drawing the
    sprite mask.


    :param sprites: A collection of key-value pairs (a dictionary) where
        each key-value pair maps the key (the label of a sprite) to its
        associated value (a `Sprite` object).

    :param label_matrix: A 2D array of integers of equal dimension (width
        and height) as the original image where the sprites are packed in.
        The `label_matrix` array maps each pixel of the image passed to
        the function to the label of the sprite this pixel corresponds to,
        or `0` if this pixel doesn't belong to a sprite (e.g., transparent
        color).

    :param background_color: Either a tuple `(R, G, B)` or a tuple
        `(R, G, B, A)`) that identifies the color to use as the background
        of the image to create. If this argument is not passed to the
        function, the default value `(255, 255, 255)`.


    :return: An `Image` object.


    :raise ValueError: if the specified background color is not a tuple
        `(R, G, B)`, neither a tuple `(R, G, B, A)`.
    """
    if background_color and (not isinstance(background_color, tuple) or not 3 <= len(background_color) <= 4):
        raise ValueError('Invalid background color')

    if background_color is None:
        background_color = (255, 255, 255)

    # @todo: simplify with the list of Sprites object that MUST include the sprite label.
    sprite_labels = set([
        label
        for row in label_matrix
        for label in row])

    # Randomly generate RGB colors for each sprite label using the specified
    # color (or White, if not defined) for the background.
    sprite_label_colors = {0: background_color}

    for label in list(sprite_labels)[1:]: # @todo: background color should not be in the sprite labels!
        sprite_label_colors[label] = tuple([random.randint(64, 200) for c in range(len(background_color))])

    # Build the image with the sprite label's color.
    pixels = numpy.asarray([
        [sprite_label_colors[label] for label in row]
        for row in label_matrix],
        dtype=numpy.uint8)

    image = Image.fromarray(pixels, 'RGB' if len(background_color) == 3 else 'RGBA')

    # Draw the bounding boxes surrounding the sprites.
    draw = ImageDraw.Draw(image)

    for label in sprites:
        sprite = sprites[label]
        color = sprite_label_colors[label]
        draw.rectangle((sprite.top_left, sprite.bottom_right), outline=color, width=1)

    return image



image = Image.open('/Users/dcaune/Devel/intek-mission-sprite_detection/islands.png')
sprites, labels = find_sprites(image)
sprite_label_image = create_sprite_labels_image(sprites, labels)
import pprint
pprint.pprint(labels, width=120)
sprite_label_image = create_sprite_labels_image(sprites, labels)
sprite_label_image.save('/Users/dcaune/islands.png')

sprite_label_image = create_sprite_labels_image(sprites, labels, background_color=(0, 0, 0, 0))
sprite_label_image.save('/Users/dcaune/optimized_sprite_sheet_bounding_box_transparent_background.png')

