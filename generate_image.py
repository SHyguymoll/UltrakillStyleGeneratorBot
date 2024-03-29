import io
from PIL import Image, ImageColor, ImageFont, ImageDraw
from pilmoji import Pilmoji
from sys import argv
from os import makedirs, path
from select_logic import *

char_array = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","PLUS","MINUS","LEFT_BRACKET","RIGHT_BRACKET","SPACE"]

characters = {}

def load_characters(dir: str):
    for letter in char_array:
        characters[letter] = []
        try:
            characters[letter].append(Image.open(dir + "header/" + letter + ".png").getchannel("A"))
        except IOError:
            print("could not load header character " + letter)
            characters[letter].append(Image.new('RGBA', (0, 0)))
        try:
            characters[letter].append(Image.open(dir + "single/" + letter + ".png").getchannel("A"))
        except IOError:
            print("could not load single character " + letter)
            characters[letter].append(Image.new('RGBA', (0, 0)))

def generate_character(character_mask: Image.Image, color: tuple[int]) -> Image.Image:
    char = Image.new("RGBA", character_mask.size, color)
    char.putalpha(character_mask)
    return char

def get_text_dimensions(text_string: str, font: ImageFont.FreeTypeFont):
    # https://stackoverflow.com/a/46220683/9263761
    _ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

NO_COLOR = ImageColor.getrgb("#FFFFFF00")
BLACK = (0, 0, 0)

SINGLE_SIZE = (29,29)
HEADER_SIZE = (75,75)

def draw_unicode_emoji(string: str, single: bool):
    font = ImageFont.truetype('arial.ttf', 80)
    dimensions = get_text_dimensions(string, font)
    dimensions = Pilmoji(Image.new('RGBA', (0,0), NO_COLOR)).getsize(string, font)
    with Image.new('RGBA', dimensions, NO_COLOR) as img:
        with Pilmoji(img) as pilmoji:
            pilmoji.text(xy=(0, 0), text=string, fill=BLACK, font=font)
        if not single:
            return img.resize(HEADER_SIZE, Image.Resampling.BILINEAR)
        else:
            return img.resize(SINGLE_SIZE, Image.Resampling.NEAREST)

def generate_emoji(data: bytes | str, single: bool) -> Image.Image:
    if data == b"delete_me":
        return Image.new('RGBA', (0,0)).resize(
                SINGLE_SIZE if single else HEADER_SIZE,
                Image.Resampling.NEAREST if single else Image.Resampling.BILINEAR
        )
    if isinstance(data, bytes):
        return Image.open(io.BytesIO(data)).resize(
                SINGLE_SIZE if single else HEADER_SIZE,
                Image.Resampling.NEAREST if single else Image.Resampling.BILINEAR
        )
    if isinstance(data, str):
        return draw_unicode_emoji(data, single)

def generate_string(string: str, header: bool, current_color: TColor, custom_color: tuple[int]):
    final = Image.new('RGBA', (0, 0))
    for letter in string:
        char = select_character(characters, letter, header)
        if current_color == TColor.CUSTOM:
            final = merge_hori(final, generate_character(char, custom_color))
        else:
            final = merge_hori(final, generate_character(char, pick_color(current_color, char)))
    return final

def generate_image(text_string: str, header: bool, discord_mode: bool, discord_emojis: dict[str, bytes]) -> Image.Image:
    interpret_string = text_string.split("_")
    current_color = TColor.WHITE
    custom_color = (255, 255, 255, 255)
    final = Image.new('RGBA', (0, 0))
    for string in interpret_string:
        if len(string) == 0: #ignore empty splits
            continue
        if string[0].isdigit(): #checking if the first character is a number
                current_color = select_color(int(string[0]))
                string = string[1:] #remove the number as we've used it up
                if current_color == TColor.CUSTOM:
                    custom_color = pick_color(TColor.CUSTOM, string[0:6])
                    string = string[6:]
        if string[0] == "+": #checking if first real character is +
            string = "+   " + string[1:]
        if string[0] == "-": #ditto for -
            string = "-   " + string[1:]
        if discord_mode: #handle like a discord message with emojis
            discord_strings = string.split("<")
            if len(discord_strings) == 1: #this string has no emojis, treat it like a normal string
                final = merge_hori(final, generate_string(string, header, current_color, custom_color))
            else: #this string has emojis, split and refer to the dictionary
                for dis_string in discord_strings:
                    splitted = dis_string.split(">", 1)
                    if len(splitted) == 1: #this portion of the string has no emojis at all
                        final = merge_hori(final, generate_string(splitted[0], header, current_color, custom_color))
                    else: #the first item is an emoji reference, the second is normal text
                        final = merge_hori(final, generate_emoji(discord_emojis[splitted[0]], header))
                        final = merge_hori(final, generate_string(splitted[1], header, current_color, custom_color))

        else: #handle like a normal string
            final = generate_string(string, header, current_color, custom_color)
    return final

def merge_hori(im1: Image.Image, im2: Image.Image) -> Image.Image:
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    return im

def merge_vert(im1: Image.Image, im2: Image.Image) -> Image.Image:
    w = max(im1.size[0], im2.size[0])
    h = im1.size[1] + im2.size[1]
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (0, im1.size[1]))
    return im

def full_image(str: list, discord_mode: bool = False, discord_emojis: dict[str, bytes] = {}) -> Image.Image:
    imgs = []
    for ind in range(len(str)):
        imgs.append(generate_image(str[ind], True if ind != 0 else False, discord_mode, discord_emojis))
    comp_image = Image.new('RGBA', (0, 0))
    for img in imgs:
        comp_image = merge_vert(comp_image, img)
    return comp_image

if __name__ == "__main__":
    load_characters("images/")
    filename = argv[1]
    dir = filename[::-1].split("/", 1)[1][::-1] + "/" #this returns just the leading path to the actual file
    if not path.exists(dir):
        makedirs(dir)
    comp_image = full_image(argv[2:])
    comp_image.show()
    option = input("save?")
    if option.lower() in ["y", "yes"]:
        comp_image.save(filename)
    comp_image.close()
