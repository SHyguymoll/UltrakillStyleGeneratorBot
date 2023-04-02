# UltrakillStyleGeneratorBot

This is a bot which adds commands to make images that look like Style bonuses from the game [Ultrakill.](devilmayquake.com)

# Requirements
/images (source of characters)

PIL (image stitching, character generating)

sys (command line args)

enum (color enums)

os (generating directories)

# How to use locally
```python3 generate_image.py <file out with local path> <text> [<text> , ...]```

`<text>`: a-z, A-Z, +, -, (, and ) are written. color can be specified using `_x`, where x is a number from 0 to 4 (currently). Number support will be added in the future.

Colors:

0. White
1. Orange
2. Green
3. Blue
4. Red
5. Gold


This will generate a transparent image with the texts and colors in question, named after the inputted text. Each block of text will be on its own line. The first block of text will be the style ranking (ala Anarchic, Savage, etc.)

# How to use on discord
[Add Ultrakill Style Generator#1983](https://discord.com/api/oauth2/authorize?client_id=939773647638392883&permissions=277025442816&scope=bot)