from PIL import Image, ImageColor, ImageFont, ImageDraw
from sys import argv
from os import makedirs, path
from select_logic import *

def load_characters(lower_fontname: str, upper_fontname: str):
    global font_style, font_header
    font_style = ImageFont.truetype(lower_fontname, 28)
    font_header = ImageFont.truetype(upper_fontname, 72)

def generate_character(character_mask: Image.Image, color: TColor) -> Image.Image:
    char = Image.new("RGBA", character_mask.size, pick_color(color))
    char.putalpha(character_mask)
    return char

NO_COLOR = ImageColor.getrgb("#FFFFFF00")

def write_text(text: str, is_header: bool, color: TColor) -> Image.Image:
    if is_header:
        header_bbox = font_header.getbbox(text=text, anchor="ld")
        img_size = (header_bbox[2]-header_bbox[0], header_bbox[3]-header_bbox[1])
        img = Image.new('RGBA', img_size, NO_COLOR)
        draw = ImageDraw.Draw(img)
        draw.text(xy=(0, img_size[1]), text=text, fill=pick_color(color), anchor="ld")
        return img
    else:
        style_bbox = font_style.getbbox(text=text, anchor="ld")
        img_size = (style_bbox[2]-style_bbox[0], style_bbox[3]-style_bbox[1])
        img = Image.new('RGBA', img_size, NO_COLOR)
        draw = ImageDraw.Draw(img)
        draw.fontmode = 1
        draw.text(xy=(0, img_size[1]), text=text, fill=pick_color(color), anchor="ld")
        return img

def generate_image(text_string: str, header: bool = False) -> Image.Image:
    interpret_string = text_string.split("_")
    current_color = TColor.WHITE
    final = Image.new('RGBA', (0, 0))
    for ind, string in enumerate(interpret_string):
        if len(string) == 0: #ignore empty splits
            continue
        if string[0].isdigit(): #checking if the first character is a number
            current_color = select_color(int(string[0]))
            string = string[1:] #remove the number as we've used it up
        if len(string) == 0: #after removal, the string might be empty, so return an empty image
            continue
        if header: #header, don't make any changes to the string
            final = merge_hori(final, write_text(string, True, current_color))
        else:
            if ind == 0 and string[0] == "+": #pluses come with spaces when at the start of the line
                string = "+   " + string[1:]
            if ind == 0 and string[0] == "-": #same with minuses
                string = "-   " + string[1:]
            final = merge_hori(final, write_text(string, False, current_color))
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

def full_image(str: list) -> Image.Image:
    imgs = []
    for ind in range(len(str)):
        imgs.append(generate_image(str[ind], True if ind == 0 else False))
    comp_image = Image.new('RGBA', (0, 0))
    for img in imgs:
        comp_image = merge_vert(comp_image, img)
    return comp_image

if __name__ == "__main__":
    load_characters("fonts/VCR_OSD_MONO_1.001.ttf", "fonts/Akkordeon-Eight.ttf")
    filename = argv[1]
    dir = filename[::-1].split("/", 1)[1][::-1] + "/" #this returns just the leading path to the actual file
    if not path.exists(dir):
        makedirs(dir)
    comp_image = full_image(argv[2:])
    comp_image.save(filename)
    comp_image.close()
