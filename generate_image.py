from PIL import Image
from sys import argv
from enum import Enum
from os import makedirs, path
 
class TColor(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    BLUE = 3
    RED = 4
    GOLD = 5

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

def pick_color(color: TColor):
    match color:
        case TColor.WHITE:
            return (255, 255, 255, 255)
        case TColor.ORANGE:
            return (255, 170, 0, 255)
        case TColor.GREEN:
            return (22, 255, 29, 255)
        case TColor.BLUE:
            return (39, 255, 236, 255)
        case TColor.RED:
            return (255, 0, 0, 255)
        case TColor.GOLD:
            return (243, 211, 0)

def generate_character(character_mask: Image.Image, color: TColor) -> Image.Image:
    char = Image.new("RGBA", character_mask.size, pick_color(color))
    char.putalpha(character_mask)
    return char

def generate_image(text_string: str, header: bool = False) -> Image.Image:
    interpret_string = text_string.split("_")
    current_color = TColor.RED
    final = Image.new('RGBA', (0, 0))
    for string in interpret_string:
        if len(string) == 0: #ignore empty splits
            continue
        if string[0].isdigit: #checking if the first character is a number
            match int(string[0]):
                case 0:
                    current_color = TColor.WHITE
                case 1:
                    current_color = TColor.ORANGE
                case 2:
                    current_color = TColor.GREEN
                case 3:
                    current_color = TColor.BLUE
                case 4:
                    current_color = TColor.RED
                case 5:
                    current_color = TColor.GOLD
                case _: #invalid color index, fallback to white
                    current_color = TColor.WHITE
            string = string[1:] #remove the number as we've used it up
        for ind, letter in enumerate(string):
            match letter:
                case "+":
                    final = merge_hori(final,generate_character(characters["PLUS"][header], current_color))
                    if ind == 0: #add separation from plus
                        for _i in range(3):
                            final = merge_hori(final,generate_character(characters["SPACE"][header], TColor.WHITE))
                case "-":
                    final = merge_hori(final,generate_character(characters["MINUS"][header], current_color))
                    if ind == 0: #ditto for minus
                        for _i in range(3):
                            final = merge_hori(final,generate_character(characters["SPACE"][header], TColor.WHITE))
                case "(":
                    final = merge_hori(final,generate_character(characters["LEFT_BRACKET"][header], current_color))
                case ")":
                    final = merge_hori(final,generate_character(characters["RIGHT_BRACKET"][header], current_color))
                case " ":
                    final = merge_hori(final,generate_character(characters["SPACE"][header], TColor.WHITE))
                case _:
                    final = merge_hori(final,generate_character(characters[letter.upper()][header], current_color))
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
    comp_image.save(filename)
    comp_image.close()
