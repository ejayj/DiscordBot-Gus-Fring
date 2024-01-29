import discord
import responses
from discord import app_commands
from discord.ext import commands

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

#logs messages sent in channel.
async def send_message(message, user_message, is_private): #async function for gathering messages and returning correct response
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
def run_discord_bot():
    TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'
    
    client = MyClient()
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
    @client.tree.command()
    @app_commands.describe(name="Type any name here!")
    async def hello(interaction: discord.Integration, name: str): #await interaction.response.send_message(f"Hello {name}!") #for an ephemeral message so only the user sees it, we can do:
        """Say Hello!"""
        await interaction.response.send_message(f"Hello {name}!", ephemeral=True)
    
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
        await interaction.response.send_message(f'{first} + {second}  = {first + second}', ephemeral=True)
        
    @client.tree.command()
    async def privatechat(interaction: discord.Integration, message: str): #await interaction.response.send_message(f"Hello {name}!") #for an ephemeral message so only the user sees it, we can do:
        """Request a private chat!"""
        await interaction.response.send_message(f"Hello! To start a private chat, type '$!help'", ephemeral=True)

    @client.event
    async def on_message(message): #captures channel logs
        if message.author == client.user:
            return
        
        username = str(message.author)#whoever is writing
        user_message = str(message.content) #gets message content
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')
        
        if user_message[0] == '$' and user_message[1] == '!': #if user types ? before a message, bot will interact
            user_message = user_message[1:] #this removes the '?' and processes message as normal
            await send_message(message, user_message, is_private=True)
            
    client.run(TOKEN)
    
    
    