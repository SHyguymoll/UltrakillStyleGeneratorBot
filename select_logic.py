from enum import Enum

class TColor(Enum):
    WHITE = 0
    ORANGE = 1
    GREEN = 2
    BLUE = 3
    RED = 4
    GOLD = 5
    CUSTOM = 6

def ishex(string: str) -> bool:
    for charac in string: #safeguard against invalid hex strings
        if not charac.isdigit() and not charac.upper() in ["A", "B", "C", "D", "E", "F"]:
            return False
    return True

def pick_color(color: TColor, string: str):
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
        case TColor.CUSTOM:
            if len(string) < 6: #hex codes must be 6 symbols long
                return (255, 255, 255, 255)
            if not ishex(string): #safeguard against invalid hex strings
                return (255, 255, 255, 255)
            return (
                int(string[0:2], base=16),
                int(string[2:4], base=16),
                int(string[4:6], base=16),
                255
            )

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
        case 6:
            return TColor.CUSTOM
        case _: #invalid color index, fallback to white
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
    elif char.isalpha() or char.isnumeric():
        return [char_dict[char.upper()][head]]
    else: #skip invalid characters
        return [char_dict["SPACE"][head]]