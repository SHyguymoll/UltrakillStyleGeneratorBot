from enum import Enum

class TColor(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    BLUE = 3
    RED = 4
    GOLD = 5

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

def select_color(val: int):
    match val:
        case 0:
            return TColor.WHITE
        case 1:
            return TColor.ORANGE
        case 2:
            return TColor.GREEN
        case 3:
            return TColor.BLUE
        case 4:
            return TColor.RED
        case 5:
            return TColor.GOLD
        case _: #invalid color index, fallback to white
            return TColor.WHITE

def select_character(char_dict: dict, char: str, head: bool): #needs to return array
    match char:
        case "+":
            return [char_dict["PLUS"][head], char_dict["SPACE"][head], char_dict["SPACE"][head], char_dict["SPACE"][head]]
        case "-":
            return [char_dict["MINUS"][head], char_dict["SPACE"][head], char_dict["SPACE"][head], char_dict["SPACE"][head]]
        case "(":
            return [char_dict["LEFT_BRACKET"][head]]
        case ")":
            return [char_dict["RIGHT_BRACKET"][head]]
        case " ":
            return [char_dict["SPACE"][head]]
        case _:
            return [char_dict[char.upper()][head]]