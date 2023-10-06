import asyncio
import discord
from discord import app_commands, message
from dotenv import load_dotenv
from discord.ext import tasks
import random
import db
import os

cmd_map = {
    'send_treater': 'trick or treat...',
    'trick': 'haha, send a trick!',
    'treat': 'yippee, send a treat!',
    'commands': 'List avaialble commands and their descriptions',
}

intents = discord.Intents.default()
intents.message_content = True  # tODO: figure out what this line does
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

treaters_array = []

load_dotenv()
# jonah server = 936546533007044628, dts = 274306544017997835
# TREATER_ACTIVE = False


# start up
@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

    with open("urls.txt") as url_file:
        for line in url_file.readlines():
            treaters_array.append(line.rstrip('\n'))

    game = discord.Game("SPOOKY")
    await client.change_presence(activity=game)

    await tree.sync(guild=discord.Object(os.environ.get('GUILD_ID')))
    global TREATER_ACTIVE
    TREATER_ACTIVE = False

    print("ready!")
    await start_night()


@client.event
async def start_night():
    global TREATER_ACTIVE
    if not TREATER_ACTIVE:
        # Decrease this interval for testing.
        embed = discord.Embed(title="It's Halloween night!",
                              description="Friends will start trick-or-treating soon.")
        await client.get_channel(int(os.environ.get('CHANNEL_ID'))).send(embed=embed)
        await asyncio.sleep(10)
        send_trick_or_treater.start()


@tasks.loop(seconds=5.0)
async def send_trick_or_treater():
    embed = discord.Embed(title="A trick or treater is at the door!",
                          description="Open the door and greet them with /treat or /treat")
    embed.set_image(url=treaters_array[random.randrange(0, 40)])
    print("Hello")
    await client.get_channel(int(os.environ.get('CHANNEL_ID'))).send(embed=embed)

    global TREATER_ACTIVE
    TREATER_ACTIVE = True
    send_trick_or_treater.change_interval(seconds=random.randint(15, 30))


@tree.command(name="treat", description="Answer the door with a sweet treat if a friend is there", guild=discord.Object(os.environ.get('GUILD_ID')))
async def treat_command(interaction):
    if db.check_table(interaction.user.name) == None:
        db.add_user(interaction.user.name)
    global TREATER_ACTIVE
    if TREATER_ACTIVE:
        TREATER_ACTIVE = False
        db.update_score(interaction.user.name, "treat")
        embed = discord.Embed(
            title=f"Congrats! 🎉", description=f'{interaction.user.mention}, You gave our friend a treat!')
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Sorry ☹️", description=f'{interaction.user.mention}, there are no friends at the door')
        await interaction.response.send_message(embed=embed)


@tree.command(name="trick", description="commit a hate crime against the guest!", guild=discord.Object(os.environ.get('GUILD_ID')))
async def trick_command(interaction):
    if db.check_table(interaction.user.name) == None:
        db.add_user(interaction.user.name)
    global TREATER_ACTIVE
    if TREATER_ACTIVE:
        TREATER_ACTIVE = False
        db.update_score(interaction.user.name, "trick")
        embed = discord.Embed(
            title=f'Hehehehe!', description=f'{interaction.user.mention}, you just tricked your guest')
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Sorry", description=f'{interaction.user.mention}, there are no friends at the door')
        await interaction.response.send_message(embed=embed)


@tree.command(name="score", description="check your scores", guild=discord.Object(os.environ.get('GUILD_ID')))
async def score_command(interaction):
    if db.check_table(interaction.user.name) == None:
        await ctx.author.send("Your name is not on the leaderboard!")
    else:
        trick, treat = db.get_score(interaction.user.name)
        await interaction.response.send_message(f"{interaction.user.mention}, Your trick score is {trick} and your treat score is {treat}", ephemeral=True)


if __name__ == '__main__':
    load_dotenv()
    db.create_tables()
    client.run(os.environ.get('BOT_TOKEN'))
