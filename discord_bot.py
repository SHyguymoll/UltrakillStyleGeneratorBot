import os
import generate_image
import discord
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

@tree.command(name = "generate_text", description = "Characters Supported: a-Z, 0-9, +, -, (, )\nSeparate strings with |") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction: discord.Interaction, name: str, string: str):
    make_img = generate_image.full_image(string.split("|"))

    act_name = "out_discord/" + name + ".png"
    text = str("Text: " + name)
    to_use = BytesIO()
    make_img.save(to_use, format='PNG')
    to_use.seek(0)

    file = discord.File(fp=to_use,filename=act_name)
    await interaction.response.send_message(content=text, file=file)
    file.close()

@client.event
async def on_ready():
    generate_image.load_characters("images/")
    await tree.sync()
    print(f'We have logged in as {client.user}')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


def read_token() -> str:
    with open("token.txt") as f:
        return f.readline()

client.run(read_token())
