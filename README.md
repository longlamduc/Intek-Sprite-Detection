# 2D Sprite Detection

## Sprite

A [**sprite**](<(<https://en.wikipedia.org/wiki/Sprite_(computer_graphics)>) is a small [**raster graphic**](https://en.wikipedia.org/wiki/Raster_graphics) (a **bitmap**) that represents an object such as a character, a vehicle, a projectile, etc.

![Metal Slug ](metal_slug_sprite_large.png)

Sprites are a popular way to create large, complex scenes as you can manipulate each sprite separately from the rest of the scene. This allows for greater control over how the scene is rendered, as well as over how the players can interact with the scene.

Sprites are mainly used in 2D video games, such as [Shoot'em up](https://en.wikipedia.org/wiki/Shoot_%27em_up) in which the hero combats a large number of enemies by shooting at them while dodging their fire:

| [Cannon Fodder](<https://en.wikipedia.org/wiki/Cannon_Fodder_(video_game)>) | [Commando](<https://en.wikipedia.org/wiki/Commando_(video_game)>) | [Metal Slug](https://en.wikipedia.org/wiki/Metal_Slug) |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------ |
| ![Cannon Fodder](2d_video_game_cannon_fodder.jpg)                           | ![Commando](2d_video_game_commando.jpg)                           | ![Metal Slug](2d_video_game_metal_slug.png)            |

## Sprite Animation

Several sprites, representing a same object, can be rendered in quick succession to give the illusion of movement of this object (**animation**).

For example, the animation of the hero Marco Rossi (Metal Slug), running with a gun, is composed of 9 sprites:

![Metal Slug Sprite Running with a Gun](metal_slug_sprites_running_with_gun.png)

## Sprite Sheets

It is not uncommon for games to have tens to hundreds of sprites. Loading each of these as an individual image would consume a lot of memory and processing power. To help manage sprites and avoid using so many images, many games use **sprite sheets** (also known as **image sprites**).

A sprite sheet consists of multiple sprites in one image. In other words, sprite sheets pack multiple sprites into a single picture. Using sprite sheet, video game developers create sprite sheet animation representing one or several animation sequences while only loading a single file:

![Metal Slug Sprites](metal_slug_sprite_sheet_large.png)

## Sprite Bounding Box

A frame (**bounding box**) can be used to delimit the sprite in the sprite sheet. This bounding box is defined with two 2D points `top_left` and the `bottom_right`, which their respective coordinates `x` and `y` are relative to the top-left corner of the sprite sheet's image.

For example:

![Shape Bounding Boxes](metal_slug_sprite_detection_bounding_boxes.png)

## Sprite Mask

The mask of a sprite defines the 2D shape of the sprite. For example, the sprite sheet [`metal_slug_sprite_standing_stance_large.png`](metal_slug_sprite_standing_stance_large.png) contains the 3 following sprites:

![Metal Slug Standing Stance](metal_slug_sprite_standing_stance_large.png)

The masks of these sprites are respectively:

![](metal_slug_sprite_detection_coloring.png)

## Optimized Sprite Sheets

Sprites could be evenly placed in the sprite sheet according to their bounding box. The disadvantage is that this method of placement wastes a lot of memory because of all the additional transparency of each sprite, especially when sprites have different width and height.

The developers are aware of the wasted memory and started to optimize the space in the sprite sheets. Sprites are placed close to each others, depending on their shape. The bounding box of a sprite may intersect the bounding box of another sprite, but the shape of this sprite is always separated from the shape of any other sprites with at least 1 transparent pixel.

![Optimized Sprite Sheet](optimized_sprite_sheet.png)

This space optimization is even more efficient when some big sprites have concave shape (i.e., shape that curves inward):

| Scene with 2 Sprites    | Sprite Sheet                                 | Sprite Masks                                      |
| ----------------------- | -------------------------------------------- | ------------------------------------------------- |
| ![Islands](islands.png) | ![Islands Sprite Sheet](islands_sprites.png) | ![Islands Sprite Masks](islands_sprite_masks.png) |

# Waypoint: Write a class `Sprite`

Write a class `Sprite` that contains the following attributes:

- `top_left`: A 2D point that indicates the top-left position of the bounding box of the shape in the image;

- `bottom_right`: A 2D point that indicates the bottom-most position of the bounding box of the shape in the image;

- `mask_color`: An integer representing the RGB value of this sprite in the mask image.

# Waypoint: Write a class `SpriteSheet`

# Waypoint: Detect the Sprites in a Sprite Sheet Picture

We would like to detect all the sprites packed in a single picture. For example, providing the following image [`metal_slug_standing_stance.png`](./metal_slug_standing_stance.png):

Write a function `detect_sprites` that takes an argument `image` (an object [`Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html)) and that returns an object `SpriteSheet`.

An object `SpriteSheet`

- A list of objects `Sprite` corresponding to all the sprites that have been detected;

- An object [`Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html), corresponding to the masks of the detected sprites.

An object `Sprite` contains the following attributes:

- `top_left`: A 2D point that indicates the top-left position of the bounding box of the shape in the image;

- `bottom_right`: A 2D point that indicates the bottom-most position of the bounding box of the shape in the image;

- `mask_color`: An integer representing the RGB value of this sprite in the mask image.

The function `detect_shapes` accepts an optional argument `transparent_color` (an integer if the image format is grayscale, or a tuple `(red, green, blue)` if the image format is `RGB`) that identifies the transparent color of the image. The function ignores any pixels of the image with this color.

If this argument `transparent_color` is not passed, the function determines the transparent color of the image as follows:

1. The image, such as a PNG file, has an [alpha channel](<https://en.wikipedia.org/wiki/Transparency_(graphic)>): the function ignores all the pixels of the image which alpha component is `255`;

2. The image has no alpha channel: the function identifies the color the mostly used in the image as the transparent color.

For example:

```python
>>> sprite_sheet = detect_sprites('./metal_slug_sprite_standing_stance.png')
>>> len(shapes)
3
>>> first_shape = shapes[0]
>>> first_shape.top_left.x, first_shape.top_left.y
4, 2
>>> first_shape.bottom_right.x, first_shape.bottom_right.y
33, 39
```
