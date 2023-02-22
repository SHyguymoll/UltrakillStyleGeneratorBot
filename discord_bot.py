import generate_image
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

@tree.command(name = "generate_text", description = "Characters Supported: a-Z, +, -, (, )") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction, string:str, color:str):
    generate_image.generate_image(string, generate_image.TColor(int(color))).save(string)
    await interaction.response.send_message("Text: " + string, embed=open(string))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

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

