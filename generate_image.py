from PIL import Image
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

def generate_image(text_string: str, header: bool = False) -> Image.Image:
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
        for letter in string:
            for char in select_character(characters, letter, header): #handles + and - which come with spaces
                if current_color == TColor.CUSTOM:
                    final = merge_hori(final, generate_character(char, custom_color))
                else:
                    final = merge_hori(final, generate_character(char, pick_color(current_color, char)))
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
        imgs.append(generate_image(str[ind], True if ind != 0 else False))
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
