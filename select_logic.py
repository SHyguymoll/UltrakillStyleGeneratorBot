from enum import Enum

class TColor(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    BLUE = 3
    RED = 4
    GOLD = 5

def pick_color(color: TColor):
    if color == TColor.WHITE:
        return (255, 255, 255, 255)
    elif color == TColor.ORANGE:
        return (255, 170, 0, 255)
    elif color == TColor.GREEN:
        return (22, 255, 29, 255)
    elif color == TColor.BLUE:
        return (39, 255, 236, 255)
    elif color == TColor.RED:
        return (255, 0, 0, 255)
    elif color == TColor.GOLD:
        return (243, 211, 0)
    else: #another fallback because why not
        return (255, 255, 255, 255)

def select_color(val: int):
    if val == 0:
        return TColor.WHITE
    elif val == 1:
        return TColor.ORANGE
    elif val == 2:
        return TColor.GREEN
    elif val == 3:
        return TColor.BLUE
    elif val == 4:
        return TColor.RED
    elif val == 5:
        return TColor.GOLD
    else: #invalid color index, fallback to white
        return TColor.WHITE

def select_character(char_dict: dict, char: str, head: bool): #needs to return array
    if char == "+":
        return [char_dict["PLUS"][head], char_dict["SPACE"][head], char_dict["SPACE"][head], char_dict["SPACE"][head]]
    elif char == "-":
        return [char_dict["MINUS"][head], char_dict["SPACE"][head], char_dict["SPACE"][head], char_dict["SPACE"][head]]
    elif char == "(":
        return [char_dict["LEFT_BRACKET"][head]]
    elif char == ")":
        return [char_dict["RIGHT_BRACKET"][head]]
    elif char == " ":
        return [char_dict["SPACE"][head]]
    else:
        return [char_dict[char.upper()][head]]