# UltrakillStyleGeneratorBot

This is a bot which adds commands to make images that look like Style bonus from the game [Ultrakill.](devilmayquake.com)

# Requirements
/images (source of characters)

PIL (image stitching)
opencv-python (image recoloring via HSV)
sys (command line args)
enum (color enums)
os (directories, removing temp files (IN THE FUTURE))

# How to use locally
```python3 generate_image.py <outdir> <text> <color> [<text> <color>, ...]```

This will generate a transparent image with the texts and colors in question, named after the inputted text.