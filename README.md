# UltrakillStyleGeneratorBot

This is a bot which adds commands to make images that look like Style bonuses from the game [Ultrakill.](https://store.steampowered.com/app/1229490/ULTRAKILL/)

# Requirements
/images (source of characters)

PIL (image stitching, character generating)

sys (command line args)

enum (color enums)

os (generating directories)

# How to use locally
```python3 generate_image.py <file out with local path> <text> [<text> , ...]```

`<text>`: a-Z, 0-9, +, -, (, and ) are written. color can be specified using `_x`, where x is a number from 0 to 5 (currently).

Colors:

0. White
1. Orange
2. Green
3. Blue
4. Red
5. Gold
6. Custom (input a 6 symbol hex code (without the leading #) after the 6 to specify the color)


This will generate a transparent image with the texts and colors in question, named after the inputted text. Each block of text will be on its own line. The first block of text will be the style ranking (ala Anarchic, Savage, etc.)

Example:

```python3 generate_image.py "out/Interesting_Style.png" "5ULTRAKILL" "2+are you" "3tell_0ing me" "689596ba shrimp" "3fried this rice"```

![](https://github.com/SHyguymoll/UltrakillStyleGeneratorBot/blob/main/Interesting_Style.png?raw=true)

# How to use on discord
[Add Ultrakill Style Generator#1983](https://discord.com/api/oauth2/authorize?client_id=939773647638392883&permissions=277025442816&scope=bot)

Example (note: bot needs to be online for this to work):

```/generate_text name:Interesting Style! string:5ULTRAKILL|2+are you|3tell_0ing me|689596ba shrimp|3fried this rice```

This will make the same image as running it locally, but as an embed on discord.
