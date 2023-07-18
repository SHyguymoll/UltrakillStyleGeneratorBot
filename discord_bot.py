from generate_image import *
import discord
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

@tree.command(name = "generate_text", description ="Characters Supported: a-Z, 0-9, +, -, (, ) || Separate strings with |")
async def generate(interaction: discord.Interaction, name: str, string: str):
    final_image = convertPILimgToBytes(full_image(string.split("|")))
    act_name = name + ".png"
    text = str("Text: " + name)
    file = discord.File(fp=final_image,filename=act_name)
    await interaction.response.send_message(content=text, file=file)
    file.close()

@tree.command(name="help", description="shows help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(content="""
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
        return f.readline()

client.run(read_token())
