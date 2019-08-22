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

|                                               |                                               |                                               |                                               |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| ![](metal_slug_sprite_detection_01_large.png) | ![](metal_slug_sprite_detection_02_large.png) | ![](metal_slug_sprite_detection_03_large.png) | ![](metal_slug_sprite_detection_04_large.png) |
| ![](metal_slug_sprite_detection_05_large.png) | ![](metal_slug_sprite_detection_06_large.png) | ![](metal_slug_sprite_detection_07_large.png) | ![](metal_slug_sprite_detection_08_large.png) |

Write a function `detect_sprite` that takes an argument `image` (an object [`Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html)) and that returns two values:

- An object [`Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html), corresponding to the masks of the detected sprites;

- A list of objects `Sprite`
