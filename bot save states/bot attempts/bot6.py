import discord
from discord import app_commands
from discord.ext import commands

from typing import Literal, Union, NamedTuple
from enum import Enum

# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

# tree = app_commands.CommandTree(client)

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.tree.copy_global_to()
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        
client = MyClient()

@client.event
async def on_ready():
    # synced = await client.tree.sync()
    # print(f"Synced {len(synced)} command(s)")
    print(f'{client.user} is now running!')

# @tree.command(name = "hello", description = "Say Hello!")
# async def self(interaction: discord.Integration, name: str):
#     #await interaction.response.send_message(f"Hello {name}!")
#     #for an ephemeral message so only the user sees it, we can do:
    
#     await interaction.response.send_message(f"Hello {name}!", ephemeral=True)

@client.tree.command()
@app_commands.describe(first='The first number to add', second='The second number to add')
async def add(
    interaction: discord.Interaction,
    # This makes it so the first parameter can only be between 0 to 100.
    first: app_commands.Range[int, 0, 100],
    # This makes it so the second parameter must be over 0, with no maximum limit.
    second: app_commands.Range[int, 0, None],
):
    """Adds two numbers together"""
    await interaction.response.send_message(f'{first} + {second} = {first + second}', ephemeral=True)
# class myFlags(commands.FlagConverter):
#     reason: str
    
# @tree.command(name = "hello", description = "Say Hello!")
# async def self(interaction: discord.Integration, name: str, flags: myFlags):
#     #await interaction.response.send_message(f"Hello {name}!")
#     #for an ephemeral message so only the user sees it, we can do:
    
#     await interaction.response.send_message(f"Hello {name} and {flags.reason}!", ephemeral=True)



TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'
client.run(TOKEN)
