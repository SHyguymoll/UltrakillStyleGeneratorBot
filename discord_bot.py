from generate_image import *
import discord
import re
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

def convertPILimgToBytes(PILimg: Image.Image) -> BytesIO:
    BytesObject = BytesIO()
    PILimg.save(BytesObject, format='PNG')
    BytesObject.seek(0)
    return BytesObject

async def validate_string(input_string: str) -> tuple[str, dict[str, bytes]]:
    print(input_string)
    emoji_search = input_string.split(":")
    link_search = input_string.split("://")
    if len(link_search) > 2: #links are not allowed
        return "invalid text"
    print(emoji_search)
    emoji_start = False
    new_string = ""
    emojis = {}
    for check in emoji_search:
        if not emoji_start: #this is the text preceding an emoji, don't look for an emoji here but save it
            emoji_start = True
            new_string += check
            continue

        emoji_try = discord.utils.get(client.emojis, name=check)

        if emoji_try is discord.Emoji:
            emoji_data = await emoji_try.read()
            new_string += f"<{check}>"
            emojis[check] = emoji_data

        emoji_start = False
    print(new_string)
    return (new_string, emojis)
    #return (input_string, emojis)

@tree.command(name = "generate_text", description ="Characters Supported: a-Z, 0-9, +, -, (, ) || Separate strings with |")
async def generate(interaction: discord.Interaction, name: str, string: str, silent: bool):
    valid_string, emojis = await validate_string(string)
    final_image = convertPILimgToBytes(full_image(valid_string.split("|"), True, emojis))
    act_name = name + ".png"
    text = str("Text: " + name)
    file = discord.File(fp=final_image,filename=act_name)
    if not silent:
        await interaction.response.send_message(content=text, file=file)
    else:
        await interaction.response.send_message(file=file)
    file.close()

@tree.command(name="help", description="shows help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(ephemeral=True, content="""
How to use this bot:
name: what the image will be titled
string: a specially formatted string which will be used to make the image.
This bot supports a-Z, 0-9, +, -, (, and ).
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
