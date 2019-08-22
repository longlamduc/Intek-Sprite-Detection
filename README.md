# 2D Shape Detection

## Sprite

A [**sprite**](<(<https://en.wikipedia.org/wiki/Sprite_(computer_graphics)>) is a small bitmap that represents an object such as a character, a vehicle, a projectile, etc.

![Metal Slug ](metal_slug_sprite_color_medium.png)

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

A sprite sheet consists of multiple sprites in one image. In other words, sprite sheets pack multiple sprites into a single picture. Using sprite sheet, video game developers create sprite sheet animation representing one or several animation sequences while only loading a single file.

We provide hereafter an example of the sprite sheet of Metal Slug 1:

![Metal Slug Sprites](metal_slug_sprite_sheet_large.png)

# Waypoint 1:

We would like to detect all the 2D shapes packed in a single picture.

For example, providing the following image [`metal_slug_standing_stance.png`](./metal_slug_standing_stance.png):

![Metal Slug Standing Stance](metal_slug_sprite_standing_stance.png)

we would like to detect the following three sprites:

![](metal_slug_sprite_detection_coloring.png)

Write a function `detect_shapes` that takes an argument `image` (an object [`Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html)) and that returns two values:

- An object [`Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html), corresponding to the masks of the detected sprites;

- A list of objects `Sprite`

The function `detect_shapes` accepts an optional argument `transparent_color` (an integer if the image format is grayscale, or a tuple `(red, green, blue)` if the image format is `RGB`) that identifies the transparent color of the image. The function ignores any pixels of the image with this color.

If this argument `transparent_color` is not passed, the function determines the transparent color of the image as follows:

1. The image, such as a PNG file, has an [alpha channel](<https://en.wikipedia.org/wiki/Transparency_(graphic)>): the function ignores all the pixels of the image which alpha component is `255`;

2. The image has no alpha channel: the function identifies the color the mostly used in the image as the transparent color.
