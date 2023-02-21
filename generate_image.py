from PIL import Image
from sys import argv
import cv2
from enum import Enum
from os import makedirs, path
 
class TColor(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    BLUE = 3
    RED = 4

characters = {}
char_array = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","PLUS","MINUS","LEFT_BRACKET","RIGHT_BRACKET","SPACE"]

def load_characters(dir: str):
    for letter in char_array:
        try:
            characters[letter] = Image.open(dir + letter + ".png")
        except IOError:
            print("could not load character " + letter)
            characters[letter] = Image.new('RGBA', (0, 0))

def generate_image(text_string: str, color: int):
    final = Image.new('RGBA', (0, 0))
    for letter in text_string:
        match letter:
            case "+":
                final = merge_hori(final,characters["PLUS"])
            case "-":
                final = merge_hori(final,characters["MINUS"])
            case "(":
                final = merge_hori(final,characters["LEFT_BRACKET"])
            case ")":
                final = merge_hori(final,characters["RIGHT_BRACKET"])
            case " ":
                final = merge_hori(final,characters["SPACE"])
            case _:
                final = merge_hori(final,characters[letter.upper()])
    final.save("temp.png")
    final.close()
    recolor("temp.png","temp.png",color)
    return Image.open("temp.png")

def merge_hori(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    return im

def merge_vert(im1, im2):
    w = max(im1.size[0], im2.size[0])
    h = im1.size[1] + im2.size[1]
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (0, im1.size[1]))
    return im

#TODO: Add WHITE color mode
def recolor(filein: str, fileout: str, mode: TColor):
    save_alpha = Image.open(filein).getchannel("A")
    im = cv2.imread(filein)
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV_FULL)
    hchannel = hsv[:, :, 0]
    match mode:
        case TColor.WHITE:
            pass #don't know what to do here yet
        case TColor.ORANGE:
            hchannel = 12 + hchannel
        case TColor.GREEN: 
            hchannel = 52 + hchannel
        case TColor.BLUE:
            hchannel = 90 + hchannel
        case TColor.RED:
            hchannel = 0 + hchannel #do nothing, it is already red
    hsv[:, :, 0] = hchannel
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite(fileout, rgb)
    do_it = Image.open(fileout)
    do_it.putalpha(save_alpha)
    do_it.save(fileout)

#TODO: figure out removing temp.png
if __name__ == "__main__":
    load_characters("images/")
    imgs = []
    filename = argv[1]
    if not path.exists(filename):
        makedirs(filename)
    strings = argv[2::2]
    color = argv[3::2]
    for ind in range(len(strings)):
        imgs.append(generate_image(strings[ind], TColor(int(color[ind]))))
        #remove("temp.png")
        filename += strings[ind]
    filename += ".png"
    comp_image = Image.new('RGBA', (0, 0))
    for img in imgs:
        comp_image = merge_vert(comp_image, img)
    comp_image.save(filename)
    
