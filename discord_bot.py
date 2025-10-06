from generate_image import *
import discord
from collections import namedtuple, deque
from io import BytesIO
import re
import logging

logging.basicConfig(
    filename="bot.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

def convertPILimgToBytes(PILimg: Image.Image) -> BytesIO:
    BytesObject = BytesIO()
    PILimg.save(BytesObject, format='PNG')
    BytesObject.seek(0)
    return BytesObject

def surround_unicode(string: str) -> tuple[str, dict]:
    new_string = string
    positions = []
    emojis_early = {}
    start = 0
    pen_down = False
    for ind, char in enumerate(string):
        if ord(char) > 126:
            if not pen_down:
                start = ind
                pen_down = True
        else:
            if pen_down:
                positions.append((start, ind))
                emojis_early[string[start:ind]] = string[start:ind]
                pen_down = False
    if pen_down:
        positions.append((start, len(string)))
        emojis_early[string[start:len(string)]] = string[start:len(string)]
        pen_down = False
    for left, right in positions[::-1]:
        new_string = new_string[0:right] + ">" + new_string[right:]
        new_string = new_string[0:left] + "<" + new_string[left:]
    return (new_string, emojis_early)

async def emoji_clean(string: str, name_pattern: str, split_pattern: str, current_dict: dict, guild_id: int) -> tuple[str, dict]:
    emoji_candidates = re.findall(name_pattern, string)
    emoji_queue = deque()
    new_string = ""
    for cand in emoji_candidates:
        emoji_queue.append(cand)
        guild = client.get_guild(guild_id)
        em_try = discord.utils.find(lambda m: m.name == cand, guild.emojis)
        if isinstance(em_try, discord.Emoji):
            emoji_data = await em_try.read()
            current_dict[cand] = emoji_data
        else:
            current_dict[cand] = b"delete_me"
    split_strings = re.split(split_pattern, string)
    new_string += split_strings.pop(0)
    while emoji_queue:
        new_string += f"<{emoji_queue.popleft()}>"
        new_string += split_strings.pop(0)
    return new_string, current_dict

async def validate_string(input_string: str, guild_id: int) -> tuple[str, dict]:
    if re.search(r"https?://", input_string): #links are not allowed
        logging.warning(f"{input_string} has a link, not on my watch")
        return "invalid text"
    
    new_string, emojis = surround_unicode(input_string) #unicode emoji

    new_string, emojis = await emoji_clean(new_string, r"<a?:(?P<name>.+?):.+?>", r"<a?:.+?:.+?>", emojis, guild_id) #custom emoji
    new_string, emojis = await emoji_clean(new_string, r":(?P<name>[^<>]+?):", r":[^<>]+?:", emojis, guild_id) #unautocorrected custom emoji
    
    return (new_string, emojis)

@tree.command(name = "generate_text", description ="Characters Supported: a-Z, 0-9, +, -, (, ) || Separate strings with |")
async def generate(interaction: discord.Interaction, name: str, string: str, silent: bool):
    logging.info(f"Recieved string {string} from user {interaction.user.name}{(" in guild " + interaction.guild.name) if interaction.guild is not None else ""}")
    valid_string, emojis = await validate_string(string, interaction.guild_id)
    final_image = convertPILimgToBytes(full_image(valid_string.split("|"), True, emojis))
    act_name = name + ".png"
    logging.info(f"image {act_name} successfully generated, sending over Discord...")
    text = str("Text: " + name)
    file = discord.File(fp=final_image,filename=act_name)
    if not silent:
        await interaction.response.send_message(content=text, file=file)
    else:
        await interaction.response.send_message(file=file)
    file.close()
    logging.info(f"image {act_name} successfully sent!")

@tree.command(name="help", description="shows help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(ephemeral=True, content="""
How to use this bot:
name: what the image will be titled
string: a specially formatted string which will be used to make the image.
This bot supports a-Z, 0-9, +, -, (, and ). It also supports emojis, but for server-based emojis, the bot must be present there.
Separate strings with |.
Start each line with a number from 0-6 to define its color. You can change the color on the fly with _x, where x is a number from 0-6.
The colors, in order, are White, Orange, Green, Blue, Red, Gold, and Custom.
When specifying a custom color, the next 6 characters from the number will be treated as a hex code, from 000000 to FFFFFF.
Check the github (https://github.com/SHyguymoll/UltrakillStyleGeneratorBot/) for more info.

Example of proper usage:
`/generate_text Interesting Style! 5ULTRAKILL|2+are you|3tell_0ing me|689596ba shrimp|3fried this rice`""")


@client.event
async def on_ready():
    load_characters("images/")
    await tree.sync()
    print(f'We have logged in as {client.user}, it is safe to background')

def read_token() -> str:
    with open("token.txt") as f:
        tok = f.readline().split(" - ", 1)
        print(tok[0])
        return tok[1]

client.run(read_token())
